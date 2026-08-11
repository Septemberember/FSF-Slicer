import z3

from fsf_tool.expression import ExpressionEngine, make_symbol


def test_java_expression_translation():
    x = make_symbol("x", "int")
    engine = ExpressionEngine({"x": "int"})
    expr = engine.evaluate_text("x > 0 && x % 2 == 0", {"x": x})
    solver = z3.Solver()
    solver.add(expr, x == 4)
    assert solver.check() == z3.sat
    solver = z3.Solver()
    solver.add(expr, x == 3)
    assert solver.check() == z3.unsat


def test_java_negative_remainder():
    engine = ExpressionEngine({"x": "int"})
    assert engine.evaluate_text("x % 3", {"x": -5}) == -2

