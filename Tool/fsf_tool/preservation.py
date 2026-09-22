"""Relational equivalence over the original and sliced path summaries."""
import z3
from .expression import ExpressionEngine, expression_variables, model_as_dict
from .tbfv import TBFVEngine


def compare_judgments(original, sliced):
    if original is None:
        return 'not_compared'
    definite_sound = {'sound', 'unsound'}
    definite_complete = {'complete', 'incomplete'}
    if (original.soundness.status not in definite_sound or sliced.soundness.status not in definite_sound or
        original.completeness.status not in definite_complete or sliced.completeness.status not in definite_complete):
        return 'inconclusive'
    return 'agree' if (original.soundness.status, original.completeness.status) == (sliced.soundness.status, sliced.completeness.status) else 'disagree'


def check_preservation(program, spec, scenario, original, sliced):
    engine = TBFVEngine(program, spec)
    testing = ExpressionEngine(engine.types).evaluate_text(scenario.testing_condition, engine.input_symbols)
    names = expression_variables(scenario.defining_condition) & set(spec.outputs)
    checked = 0
    unresolved = False
    for a in original.paths:
        for b in sliced.paths:
            if a.truncated or b.truncated or (a.exception or '').startswith('unsupported:') or (b.exception or '').startswith('unsupported:'):
                unresolved = True
                continue
            if a.exception or b.exception:
                difference = a.exception != b.exception
            elif names <= set(a.outputs) and names <= set(b.outputs):
                difference = z3.Or(*[a.outputs[n] != b.outputs[n] for n in names])
            else:
                unresolved = True
                continue
            solver = engine._solver()
            solver.add(engine.domain, testing, a.path_condition, b.path_condition, difference)
            result = solver.check()
            checked += 1
            if result == z3.sat:
                return {'status': 'different', 'reason': 'Same-input observations differ.', 'counterexample': model_as_dict(solver.model(), engine.input_symbols, spec.inputs), 'path_pairs_checked': checked}
            if result == z3.unknown: unresolved = True
    proven = not unresolved and original.coverage == sliced.coverage == 'complete'
    return {'status': 'equivalent' if proven else 'inconclusive', 'reason': 'All scenario inputs have matching output/exception observations in the supported semantic model.' if proven else 'Coverage or solver results do not establish whole-domain equivalence.', 'counterexample': None, 'path_pairs_checked': checked}
