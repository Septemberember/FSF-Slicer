"""Differential tests against javac/java, independent of the symbolic evaluator."""
import random
import shutil
import subprocess
from pathlib import Path
import pytest
import z3
from fsf_tool.expression import ExpressionEngine, make_symbol
from fsf_tool.executor import ConcolicExecutor
from test_regressions import fixture

pytestmark = pytest.mark.skipif(not shutil.which('javac') or not shutil.which('java'), reason='JDK required for independent oracle')


def run_java(tmp_path, source):
    path = tmp_path/'Oracle.java'
    path.write_text(source)
    subprocess.run(['javac', '-proc:none', '-d', str(tmp_path), str(path)], capture_output=True, text=True, check=True, timeout=30)
    return subprocess.run(['java', '-cp', str(tmp_path), 'Oracle'], capture_output=True, text=True, check=True, timeout=30).stdout.splitlines()


def test_jvm_expression_oracle(tmp_path):
    expressions = [
        'x + y', 'x * y', 'x - y', '(x + y) < x', 'x << y', 'x >> y', 'x >>> y',
        '(long)x + y', '((long)x << 33) + y', '(long)(x * y)', 'x & y', 'x | y', 'x ^ y',
        'y == 0 ? 0 : x / y', 'y == 0 ? 0 : x % y',
        '(byte)(x + y)', '(short)(x + y)', '(char)(x + y)', 'Math.abs(x)', 'Math.min(x, y)',
        'Math.max(x, y)', '!(x < y)', '-(x + y)', '~(x * y)', 'y != 0 && x / y < 0',
        'x < 0 ? x : y', 'Long.MIN_VALUE / 3L', '0xDEAD + x',
        '(-x)', '-(-x)', '-(long)x', '!(!(x < y))', '(int)(-(long)x)',
    ]
    values = [-2147483648, -65, -1, 0, 1, 32, 2147483647]
    lines = ['public class Oracle { public static void main(String[] args) {', 'int[] values = {'+', '.join(str(v) for v in values)+'};', 'for(int x:values) for(int y:values) {']
    for expr in expressions:
        # Cast chars so the oracle prints the numeric value, not a code unit.
        wrapped = '(int)(' + expr + ')' if expr.startswith('(char)') else expr
        lines.append('System.out.println('+wrapped+');')
    actual = run_java(tmp_path, '\n'.join([*lines, '}}}']))
    index = 0
    engine = ExpressionEngine({'x': 'int', 'y': 'int'})
    symbols = {n: make_symbol(n, 'int') for n in ['x', 'y']}
    for x in values:
        for y in values:
            for expr in expressions:
                expected = actual[index]; index += 1
                concrete = engine.evaluate_text(expr, {'x': x, 'y': y})
                assert str(concrete).lower() == expected, (expr, x, y, concrete, expected)
                symbolic = engine.evaluate_text(expr, symbols)
                if isinstance(symbolic, z3.AstRef):
                    value = z3.simplify(z3.substitute(symbolic, (symbols['x'], z3.BitVecVal(x,32)), (symbols['y'],z3.BitVecVal(y,32))))
                    if z3.is_bv_value(value):
                        raw = value.as_long()
                        concrete = raw - (1 << value.size()) if raw >= (1 << (value.size()-1)) else raw
                    else: concrete = z3.is_true(value)
                else: concrete = symbolic
                assert str(concrete).lower() == expected, (expr, x, y, 'symbolic', concrete, expected)


@pytest.mark.parametrize('body', [
    'int s=0; for(int i=0; i<x; i++){ if(i==2) continue; s+=i; } return s;',
    'int s=0; do { s++; if(s==2) continue; x--; } while(x>0); return s;',
    'int s=0; switch(x){ case 0: s=1; case 1: s+=2; break; default: s=5; case 3: s+=7; } return s;',
    'x=-x; if(x>0) return 7; return 9;',
    'return x==0 ? 7 : (6/x);',
    'byte b=(byte)(x+127); b+=3; return b;',
    'long y=Long.MIN_VALUE; return (int)(y/3L + x);',
])
def test_executor_against_jvm(tmp_path, body):
    _, _, program, spec = fixture(tmp_path, body)
    source = 'public class Oracle { public static int f(int x) {'+body+'} public static void main(String[] a){for(int x=-3;x<=3;x++) System.out.println(f(x));}}'
    actual = run_java(tmp_path, source)
    executor = ConcolicExecutor(program, spec)
    for x, expected in zip(range(-3,4), actual):
        result = executor.execute({'x':x})
        assert result.exception is None, result.exception
        assert result.concrete_outputs['return_value'] == int(expected)

@pytest.mark.parametrize('body', [
    'int unused=x*4; int y=1; unused=17; return y;',
    'if(x<0) return 5; return x;',
    'int y=x; x=0; if(y<0) return 3; return x;',
    'int s=0; for(int i=0;i<x;i+=2) {s+=i;} return s;',
    'int i=0; for(i=0;i<x;i++) {} return i;',
    'int y=0; while(x>0){x--; if(x==1) break; y++;} return y;',
    'int y=0; do{x--;y++;}while(x>0); return y;',
    'if(x<0){int y=3;return y;}else{int y=4;return y;}',
    'int y=0; if(x>0)y=1; y=2; return y;',
    'int s=0; switch(x){case 0:s=2;case 1:s+=3;break;default:s=7;} return s;',
    'return (int)(-(long)x);',
    'return -(-x);',
])
def test_slices_against_jvm(tmp_path, body):
    from fsf_tool.slicer import FSFGuidedSlicer, compile_slice
    _, _, program, spec = fixture(tmp_path, body)
    sliced = FSFGuidedSlicer(program, spec).slice(spec.scenarios[0], tmp_path/'slice')
    assert compile_slice(sliced).compile_ok
    oracle = 'public class Oracle { public static void main(String[] a){for(int x=-3;x<=3;x++) System.out.println(Subject.run(x));}}'
    values=[]
    for label, source in [('original',program.source),('sliced',sliced.source)]:
        folder=tmp_path/label;folder.mkdir()
        (folder/'Subject.java').write_text(source)
        (folder/'Oracle.java').write_text(oracle)
        subprocess.run(['javac','-proc:none','-d',str(folder),str(folder/'Subject.java'),str(folder/'Oracle.java')],capture_output=True,text=True,check=True,timeout=30)
        values.append(subprocess.run(['java','-cp',str(folder),'Oracle'],capture_output=True,text=True,check=True,timeout=30).stdout)
    assert values[0] == values[1]
