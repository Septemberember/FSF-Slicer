from pathlib import Path
import json
import subprocess
import pytest
import yaml
import z3

from fsf_tool.errors import FSFValidationError, ExpressionError
from fsf_tool.expression import ExpressionEngine, make_symbol, parse_expression
from fsf_tool.java_frontend import parse_java
from fsf_tool.models import FSFSpec, AnalysisConfig, VariableSpec
from fsf_tool.pipeline import analyze
from fsf_tool.executor import ConcolicExecutor
from fsf_tool.slicer import FSFGuidedSlicer, compile_slice
from fsf_tool.tbfv import TBFVEngine
from fsf_tool.validation import validate_fsf, reconcile_spec


def fixture(tmp_path, body, *, inputs=None, t='true', d='return_value == 1', config=None, returns='int'):
    java = tmp_path / 'Subject.java'
    inputs = inputs if inputs is not None else {'x': {'type': 'int', 'min': -3, 'max': 3}}
    params = ', '.join(f'{v["type"]} {n}' for n, v in inputs.items())
    java.write_text(f'public class Subject {{ public static {returns} run({params}) {{ {body} }} }}\n')
    fsf = tmp_path / 'spec.yaml'
    fsf.write_text(yaml.safe_dump({'method': 'run', 'inputs': inputs, 'outputs': {'return_value': {'type': returns, 'source': 'return'}}, 'scenarios': [{'id': 's', 'T': t, 'D': d}], 'analysis': {'solver_timeout_ms': 2000, **(config or {})}}))
    spec = FSFSpec.load(fsf)
    return java, fsf, parse_java(java, 'run'), spec


@pytest.mark.parametrize('expr,expected', [
    ('2147483647 + 1', -2147483648), ('(2147483647 + 1) < 0', True),
    ('-2147483648 / -1', -2147483648), ('-9223372036854775808L / 3L', -3074457345618258602),
    ('1 << 32', 1), ('1 << -1', -2147483648), ('-1 >>> 1', 2147483647),
    ('1L << 64', 1), ('(byte) 255', -1), ('(short) 65535', -1), ('(char) -1', 65535),
    ('0xFFFFFFFF', -1), ('0xFF', 255), ('0xDEAD', 57005), ('Math.abs(Integer.MIN_VALUE)', -2147483648),
    ('false && 1 / 0 > 0', False), ('true ? 7 : 1 / 0', 7), ('true ^ true', False),
])
def test_java_scalar_edges(expr, expected):
    assert ExpressionEngine({}).evaluate_text(expr, {}) == expected


def test_symbolic_mixed_width():
    e = ExpressionEngine({'x': 'int', 'y': 'long'})
    x, y = make_symbol('x', 'int'), make_symbol('y', 'long')
    val = e.evaluate_text('x + y', {'x': x, 'y': y})
    assert val.size() == 64
    assert z3.simplify(z3.substitute(val, (x, z3.BitVecVal(-1, 32)), (y, z3.BitVecVal(2, 64)))).as_long() == 1


@pytest.mark.parametrize('text', ['x > 0 garbage', 'x > 0; return true', 'x > 0;'])
def test_trailing_tokens_rejected(text):
    with pytest.raises(ExpressionError): parse_expression(text)


@pytest.mark.parametrize('body,t,d', [
    ('x = -x; if(x > 0) return 1; return 2;', 'x < 0', 'return_value == 1'),
    ('if(x > 0) return x; return 7;', 'true', 'return_value == (x > 0 ? x : 7)'),
    ('int y = 0; switch(x) { case 0: y=2; case 1: y+=3; break; default: y=7; } return y;', 'true', 'return_value == (x == 0 ? 5 : x == 1 ? 3 : 7)'),
    ('int y=0; while(x>0){ x--; if(x==1) break; y++; } return y;', 'true', 'return_value == (x==1 || x==3 ? 1 : 0)'),
    ('if(x != 0 && 6 / x > 0) return 1; return 0;', 'true', 'return_value == (x > 0 ? 1 : 0)'),
    ('int a=5; int unused=42; if(x>0) return x; return a;', 'true', 'return_value == (x > 0 ? x : 5)'),
    ('int y=0; do { y++; } while(y<2); return y;', 'true', 'return_value == 2'),
])
def test_whole_pipeline_regressions(tmp_path, body, t, d):
    java, fsf, _, _ = fixture(tmp_path, body, t=t, d=d)
    result = analyze(java, fsf, tmp_path/'out')
    s = result['sliced_results']['s']
    assert result['slices']['s']['compile_ok'], result['slices']['s']['compile_message']
    assert s['soundness']['status'] == 'sound', s
    assert s['completeness']['status'] == 'complete', s
    assert result['comparison']['s']['behavior']['status'] == 'equivalent'


def test_constant_output_and_unmentioned_input(tmp_path):
    inputs = {'x': {'type': 'int', 'min': 0, 'max': 1}, 'z': {'type': 'int', 'min': 0, 'max': 2}}
    java, fsf, _, _ = fixture(tmp_path, 'if(x==0) return 9; return z;', inputs=inputs, d='return_value >= 0')
    result = analyze(java, fsf, tmp_path/'out')
    assert result['comparison']['s']['behavior']['status'] == 'equivalent'
    assert result['sliced_results']['s']['soundness']['status'] == 'sound'


def test_division_exception_does_not_cover_normal_inputs(tmp_path):
    _, _, program, spec = fixture(tmp_path, 'return 1 / x;', d='return_value == 1 / x')
    result = TBFVEngine(program, spec).verify(spec.scenarios[0])
    assert result.soundness.status == 'unsound'
    assert result.coverage == 'complete'
    assert any(p.exception == 'java.lang.ArithmeticException' for p in result.paths)
    assert any(not p.exception for p in result.paths)


def test_no_false_local_completeness(tmp_path):
    _, _, program, spec = fixture(tmp_path, 'return x;', d='return_value == x || return_value == 99', config={'max_paths': 1})
    # Force partial coverage with a branch.
    program.source = program.source.replace('return x;', 'if(x>0) return x; return 0;')
    program.path.write_text(program.source)
    program = parse_java(program.path, 'run')
    result = TBFVEngine(program, spec).verify(spec.scenarios[0])
    assert result.coverage == 'partial'
    assert result.completeness.status == 'inconclusive'


def test_no_vacuous_local_soundness(tmp_path):
    _, _, program, spec = fixture(tmp_path, 'while(true) {} return 1;', config={'max_loop_iterations': 2})
    result = TBFVEngine(program, spec).verify(spec.scenarios[0])
    assert result.soundness.status == 'inconclusive'
    assert result.completeness.status == 'inconclusive'


def test_dead_throwing_statement_is_preserved(tmp_path):
    _, _, program, spec = fixture(tmp_path, 'int unused=10/x; return 1;')
    sliced = FSFGuidedSlicer(program, spec).slice(spec.scenarios[0], tmp_path/'out')
    assert '/ x' in sliced.source
    result = TBFVEngine(parse_java(sliced.output_path, 'run'), spec).verify(spec.scenarios[0])
    assert result.soundness.status == 'unsound'


def test_pure_dead_computation_removed(tmp_path):
    _, _, program, spec = fixture(tmp_path, 'int unused=x*3; int y=0; y=1; unused=7; return y;')
    sliced = FSFGuidedSlicer(program, spec).slice(spec.scenarios[0], tmp_path/'out')
    assert 'unused' not in sliced.source
    assert compile_slice(sliced).compile_ok


def test_compilation_failure_gates_judgment(tmp_path):
    java, fsf, _, _ = fixture(tmp_path, 'return missing;')
    result = analyze(java, fsf, tmp_path/'out')
    assert result['sliced_results']['s']['soundness']['status'] == 'inconclusive'
    assert result['original_compilation']['ok'] is False


def test_unsupported_call_not_classified_as_java_failure(tmp_path):
    _, _, program, spec = fixture(tmp_path, 'return Integer.bitCount(x);')
    result = TBFVEngine(program, spec).verify(spec.scenarios[0])
    assert result.soundness.status == 'inconclusive'
    assert result.coverage == 'partial'


def test_zero_input_method(tmp_path):
    _, _, program, spec = fixture(tmp_path, 'return 1;', inputs={})
    result = TBFVEngine(program, spec).verify(spec.scenarios[0])
    assert result.soundness.status == 'sound'
    assert result.completeness.status == 'complete'


@pytest.mark.parametrize('patch', [
    {'scenarios': [{'id': '../escape', 'T': 'true', 'D': 'return_value == 1'}]},
    {'analysis': {'max_paths': 0}}, {'analysis': {'max_path': 4}},
    {'analysis': {'compile_slices': 'false'}}, {'inputs': []},
    {'inputs': {'x': {'type': 'int', 'min': 2**31}}},
])
def test_invalid_schema(tmp_path, patch):
    _, fsf, _, _ = fixture(tmp_path, 'return 1;')
    data = yaml.safe_load(fsf.read_text()); data.update(patch); fsf.write_text(yaml.safe_dump(data))
    with pytest.raises(FSFValidationError): FSFSpec.load(fsf)


def test_duplicate_yaml_key(tmp_path):
    path = tmp_path/'bad.yaml'; path.write_text('method: a\nmethod: b\n')
    with pytest.raises(FSFValidationError): FSFSpec.load(path)


def test_force_invalid_cannot_prove(tmp_path):
    java, fsf, _, _ = fixture(tmp_path, 'return 1;', d='return_value')
    result = analyze(java, fsf, tmp_path/'out', force=True)
    assert result['sliced_results']['s']['soundness']['status'] == 'inconclusive'

@pytest.mark.parametrize('expr,expected', [('!(1 < 2)', False), ('-(2147483647 + 1)', -2147483648), ('~(2 + 3)', -6), ('!(true && false)', True)])
def test_prefix_on_compound_expression(expr, expected):
    assert ExpressionEngine({}).evaluate_text(expr, {}) == expected


def test_exception_scenario(tmp_path):
    java, fsf, _, _ = fixture(tmp_path, 'if(x==0) throw new ArithmeticException("zero"); return 6/x;', t='x == 0', d='failure == 1')
    raw = yaml.safe_load(fsf.read_text())
    raw['outputs']['failure'] = {'type': 'int', 'source': 'exception'}
    fsf.write_text(yaml.safe_dump(raw))
    result = analyze(java, fsf, tmp_path/'out')
    assert result['sliced_results']['s']['soundness']['status'] == 'sound'
    assert result['sliced_results']['s']['completeness']['status'] == 'complete'
    assert result['comparison']['s']['behavior']['status'] == 'equivalent'

@pytest.mark.parametrize('expr,expected', [('(-x)', -2), ('(-x)+1', -1), ('!(!true)', True), ('-(long)x', -2), ('-(-x)', 2)])
def test_parenthesis_and_cast_parser_operators(expr, expected):
    assert ExpressionEngine({'x':'int'}).evaluate_text(expr, {'x':2}) == expected


def test_cast_unary_survives_reconstruction(tmp_path):
    java, fsf, _, _ = fixture(tmp_path, 'return (int)(-(long)x);', d='return_value == -x')
    result=analyze(java,fsf,tmp_path/'out')
    assert result['sliced_results']['s']['soundness']['status'] == 'sound'
    source=Path(result['slices']['s']['output_path']).read_text()
    assert '-((long)' in source
    assert result['comparison']['s']['behavior']['status'] == 'equivalent'

def test_unicode_character_is_not_an_operator_alias():
    assert ExpressionEngine({}).evaluate_text("'∧'", {}) == 8743


@pytest.mark.parametrize('expr', ['true < false', '-true < 0', '+false == 0'])
def test_boolean_numeric_operators_rejected(expr):
    with pytest.raises(ExpressionError): ExpressionEngine({}).evaluate_text(expr, {})

def test_solver_unknown_never_establishes_proof(tmp_path, monkeypatch):
    _, _, program, spec = fixture(tmp_path, 'return x;', d='return_value == x')
    class Unknown:
        def add(self, *args): pass
        def check(self): return z3.unknown
        def reason_unknown(self): return 'test timeout'
    monkeypatch.setattr(TBFVEngine, '_solver', lambda self: Unknown())
    result=TBFVEngine(program,spec).verify(spec.scenarios[0])
    assert result.coverage == 'unknown'
    assert result.soundness.status == result.completeness.status == 'inconclusive'


def test_unsat_pruning_requires_a_proof(tmp_path, monkeypatch):
    from fsf_tool.pruning import BranchPruner
    _, _, program, spec=fixture(tmp_path, 'if(x>0) return 1; return 2;', t='x>0')
    monkeypatch.setattr(BranchPruner, 'impossible', lambda self, formula: False)
    sliced=FSFGuidedSlicer(program,spec).slice(spec.scenarios[0])
    assert not sliced.pruned_branches
    assert 'if (' in sliced.source


def test_return_alias_and_input_named_return_value(tmp_path):
    inputs={'return_value': {'type':'int','min':-2,'max':2}}
    java,fsf,_,_=fixture(tmp_path,'return x+1;')
    java.write_text(java.read_text().replace('int x', 'int return_value').replace('return x+1', 'return return_value+1'))
    raw=yaml.safe_load(fsf.read_text())
    raw['inputs']=inputs
    raw['outputs']={'answer':{'type':'int','source':'return'}}
    raw['scenarios'][0]['D']='answer == return_value + 1'
    fsf.write_text(yaml.safe_dump(raw))
    result=analyze(java,fsf,tmp_path/'out')
    assert result['sliced_results']['s']['soundness']['status'] == 'sound'
