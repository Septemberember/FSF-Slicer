"""Check paper table labels against independent JVM execution and output sets."""
from pathlib import Path
import shutil
import subprocess

import pytest
import yaml
import z3

from fsf_tool.models import FunctionalScenario, VariableSpec
from fsf_tool.pipeline import analyze
from fsf_tool.tbfv import TBFVEngine
from test_regressions import fixture

ROOT = Path(__file__).resolve().parents[1]
LOWER = '((return_value - 1) * (return_value - 1) * return_value * return_value) / 4'
UPPER = '(return_value * return_value * (return_value + 1) * (return_value + 1)) / 4'
OPERATORS = [('<', '<='), ('<=', '<='), ('<', '<'), ('<=', '<')]


@pytest.fixture(scope='module')
def jvm_cube_outputs(tmp_path_factory):
    if not shutil.which('javac') or not shutil.which('java'):
        pytest.skip('JDK required for independent oracle')
    directory = tmp_path_factory.mktemp('cube-oracle')
    oracle = directory / 'CubeOracle.java'
    oracle.write_text('''public class CubeOracle {
        public static void main(String[] args) {
            for (int x = 1; x <= 800; x++)
                System.out.println(UserInputProgram.smallestCubeSumIndex(x));
        }
    }''')
    subprocess.run(['javac', '-proc:none', '-d', str(directory),
                    str(ROOT / 'examples/UserInputProgram.java'), str(oracle)],
                   capture_output=True, text=True, check=True, timeout=30)
    result = subprocess.run(['java', '-cp', str(directory), 'CubeOracle'],
                            capture_output=True, text=True, check=True, timeout=30)
    values = list(map(int, result.stdout.splitlines()))
    assert len(values) == 800
    return dict(enumerate(values, 1))


def allows(row, x, n):
    # Independent mathematics; no symbolic evaluator or verifier-generated labels.
    low, high = sum(j**3 for j in range(1, n)), sum(j**3 for j in range(1, n + 1))
    return (low < x if row in (1, 3) else low <= x) and (x <= high if row in (1, 2) else x < high)


@pytest.mark.parametrize('upper_bound', [500, 784, 800])
@pytest.mark.parametrize('row', [1, 2, 3, 4])
def test_table1_against_jvm(tmp_path, jvm_cube_outputs, upper_bound, row):
    raw = yaml.safe_load((ROOT / 'examples/cube_sum.fsf.yaml').read_text())
    raw['inputs']['x']['max'] = upper_bound
    lower, upper = OPERATORS[row - 1]
    raw['scenarios'][1]['D'] = f'{LOWER} {lower} x && x {upper} {UPPER}'
    fsf = tmp_path / 'row.yaml'
    fsf.write_text(yaml.safe_dump(raw))
    result = analyze(ROOT / 'examples/UserInputProgram.java', fsf, tmp_path / 'out')
    actual = {x: n for x, n in jvm_cube_outputs.items() if x <= upper_bound}
    # For x<=800, n<=0 cannot satisfy a row and n>=10 has lower bound>=2025.
    desired = {n for n in range(1, 10) if any(allows(row, x, n) for x in actual)}
    unreachable = desired - set(actual.values())
    expected_sound = 'sound' if all(allows(row, x, n) for x, n in actual.items()) else 'unsound'
    expected_complete = 'incomplete' if unreachable else 'complete'
    for side in ('original_results', 'sliced_results'):
        observed = result[side]['T_positive']
        assert observed['coverage'] == 'complete'
        assert observed['soundness']['status'] == expected_sound
        assert observed['completeness']['status'] == expected_complete
        assert len(observed['paths']) == len(set(actual.values()))
        if unreachable:
            assert observed['completeness']['counterexample']['return_value'] in unreachable
        if expected_sound == 'unsound':
            x = observed['soundness']['counterexample']['x']
            assert not allows(row, x, actual[x])
        assert sum(s['test_generation_checks'] for s in result[side].values()) == (11 if upper_bound == 800 else 10)
    assert result['comparison']['T_positive']['behavior']['status'] == 'equivalent'


def bounded_fixture(tmp_path, body='return x;', d='return_value == 1-x', config=None):
    java, fsf, program, spec = fixture(tmp_path, body,
        inputs={'x': {'type': 'int', 'min': 0, 'max': 1}}, d=d, config=config)
    spec.outputs['return_value'].minimum = 0
    spec.outputs['return_value'].maximum = 2
    return program, spec


def test_finite_completeness_uses_independent_input_witnesses(tmp_path, monkeypatch):
    program, spec = bounded_fixture(tmp_path)
    original = TBFVEngine._solver
    class QuantifierFreeSolver:
        def __init__(self, solver): self.solver = solver
        def __getattr__(self, name): return getattr(self.solver, name)
        def add(self, *formulas):
            def check(node):
                assert not z3.is_quantifier(node), 'Finite output check must not rely on quantified solving'
                for child in node.children(): check(child)
            for formula in formulas:
                if isinstance(formula, z3.AstRef): check(formula)
            self.solver.add(*formulas)
    monkeypatch.setattr(TBFVEngine, '_solver', lambda self: QuantifierFreeSolver(original(self)))
    result = TBFVEngine(program, spec).verify(spec.scenarios[0])
    assert result.soundness.status == 'unsound'
    assert result.completeness.status == 'complete'


def test_finite_completeness_checks_output_tuples(tmp_path):
    program, spec = bounded_fixture(tmp_path, 'int a=x; int b=x; return a;')
    spec.outputs = {'a': VariableSpec('a', 'int', 0, 1, 'a'),
                    'b': VariableSpec('b', 'int', 0, 1, 'b')}
    scenario = FunctionalScenario('s', 'true', 'a >= 0 && a <= 1 && b >= 0 && b <= 1')
    result = TBFVEngine(program, spec).verify(scenario)
    assert result.completeness.status == 'incomplete'
    cex = result.completeness.counterexample
    assert cex['a'] != cex['b']


@pytest.mark.parametrize('config,body', [
    ({'max_paths': 1}, 'if(x==0) return 0; return 1;'),
    ({'max_loop_iterations': 1}, 'while(true) {} return 1;'),
])
def test_finite_domain_does_not_make_missing_coverage_a_proof(tmp_path, config, body):
    program, spec = bounded_fixture(tmp_path, body, d='return_value == 2', config=config)
    result = TBFVEngine(program, spec).verify(spec.scenarios[0])
    assert result.coverage != 'complete'
    assert result.completeness.status == 'inconclusive'


def test_finite_solver_unknown_stays_inconclusive(tmp_path, monkeypatch):
    program, spec = bounded_fixture(tmp_path)
    engine = TBFVEngine(program, spec)
    original = engine.verify(spec.scenarios[0])
    class Unknown:
        def add(self, *args): pass
        def set(self, **kwargs): pass
        def check(self): return z3.unknown
        def reason_unknown(self): return 'test timeout'
    monkeypatch.setattr(engine, '_solver', lambda: Unknown())
    from fsf_tool.expression import parse_expression
    result = engine._completeness(spec.scenarios[0], parse_expression(spec.scenarios[0].defining_condition),
                                  z3.BoolVal(True), original.paths, True, {'return_value'})
    assert result.status == 'inconclusive'
    assert 'test timeout' in result.reason


def test_unbounded_long_output_does_not_enumerate_or_overflow(tmp_path):
    _, _, program, spec = fixture(tmp_path, 'return 1L;', returns='long', d='return_value == 1L')
    result = TBFVEngine(program, spec).verify(spec.scenarios[0])
    assert result.completeness.status == 'complete'
