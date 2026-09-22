from __future__ import annotations
from dataclasses import dataclass, field
import javalang
import z3

from .expression import (ExpressionEngine, domain_constraint, expression_variables, make_symbol,
                         model_as_dict, normalize_type, output_constraint, effective_bounds, type_to_string)
from .java_frontend import JavaProgram
from .models import FSFSpec, ValidationIssue, VariableSpec


@dataclass
class ValidationReport:
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def valid(self): return not any(i.severity == 'error' for i in self.issues)

    def add(self, severity, code, message, counterexample=None):
        self.issues.append(ValidationIssue(severity, code, message, counterexample))


def reconcile_spec(program: JavaProgram, spec: FSFSpec):
    if spec.method is None: spec.method = program.method_name
    if not spec.inputs: spec.inputs = {n: VariableSpec(n, k) for n, k in program.parameters.items()}
    if not spec.outputs and program.return_type != 'void':
        spec.outputs = {'return_value': VariableSpec('return_value', program.return_type, source='return')}
    return spec


def validate_fsf(program, spec):
    report = ValidationReport()
    if spec.method != program.method_name:
        report.add('error', 'METHOD_MISMATCH', 'FSF method does not match the selected declaration.')
    if set(spec.inputs) != set(program.parameters):
        report.add('error', 'INPUT_MISMATCH', 'FSF inputs must name exactly the selected method parameters.')
    if set(spec.inputs) & set(spec.outputs):
        report.add('error', 'NAME_COLLISION', 'Input and output names must be distinct.')
    if len({s.id.casefold() for s in spec.scenarios}) != len(spec.scenarios):
        report.add('error', 'DUPLICATE_ID', 'Scenario IDs must be unique, ignoring case.')
    local_types = dict(program.parameters)
    for _, node in program.method:
        if isinstance(node, (javalang.tree.LocalVariableDeclaration, javalang.tree.VariableDeclaration)):
            for decl in node.declarators: local_types[decl.name] = type_to_string(node.type)
    for name, variable in spec.inputs.items():
        if name in program.parameters and normalize_type(variable.type) != normalize_type(program.parameters[name]):
            report.add('error', 'TYPE_MISMATCH', f'Input {name} has a different Java/FSF type.')
    for name, variable in spec.outputs.items():
        source = variable.source or ('return' if name == 'return_value' else name)
        actual = 'int' if source == 'exception' else program.return_type if source == 'return' else local_types.get(source)
        if actual is None or normalize_type(variable.type) != normalize_type(actual):
            report.add('error', 'OUTPUT_SOURCE_MISMATCH', f'Output {name} must refer to an existing source of the same type.')
    try:
        inputs = {n: make_symbol(n, v.type) for n, v in spec.inputs.items()}
        outputs = {n: make_symbol(n, v.type) for n, v in spec.outputs.items()}
        for name, var in spec.inputs.items():
            lo, hi = effective_bounds(var, spec.config)
            if lo is not None and lo > hi:
                report.add('error', 'EMPTY_DOMAIN', f'Effective bounds for {name} are empty.')
        domain = domain_constraint(inputs, spec.inputs, spec.config)
    except Exception as exc:
        report.add('error', 'UNSUPPORTED_TYPE', str(exc))
        return report
    types = {n: v.type for n, v in {**spec.inputs, **spec.outputs}.items()}
    valid = []
    for scenario in spec.scenarios:
        try:
            tvars, dvars = expression_variables(scenario.testing_condition), expression_variables(scenario.defining_condition)
            unknown = (tvars | dvars) - set(inputs) - set(outputs)
            if unknown:
                report.add('error', 'UNKNOWN_VARIABLE', f'{scenario.id}: {sorted(unknown)}')
                continue
            if tvars - set(inputs):
                report.add('error', 'OUTPUT_IN_T', f'{scenario.id}.T may use only inputs.')
                continue
            if not dvars & set(outputs):
                report.add('error', 'NO_OUTPUT_IN_D', f'{scenario.id}.D must constrain an output.')
            te, de = ExpressionEngine(types), ExpressionEngine(types)
            testing = te.evaluate_text(scenario.testing_condition, inputs)
            defining = de.evaluate_text(scenario.defining_condition, {**inputs, **outputs})
            if not (isinstance(testing, bool) or z3.is_bool(testing)) or not (isinstance(defining, bool) or z3.is_bool(defining)):
                report.add('error', 'NON_BOOLEAN_PREDICATE', f'{scenario.id}.T and D must be Boolean expressions.')
                continue
            for label, guard, region in [('T', te.guards, domain), ('D', de.guards, z3.And(domain, testing, output_constraint(outputs, spec.outputs)))]:
                if guard:
                    solver = _solver(spec)
                    solver.add(region, z3.Not(z3.And(*guard)))
                    result = solver.check()
                    if result != z3.unsat:
                        report.add('error', 'UNDEFINED_EXPRESSION' if result == z3.sat else 'UNKNOWN_DEFINEDNESS', f'{scenario.id}.{label} is not proved free of division/remainder by zero in its domain.')
            solver = _solver(spec)
            solver.add(domain, testing)
            result = solver.check()
            if result == z3.unsat: report.add('error', 'UNSAT_T', f'{scenario.id}.T is unsatisfiable in the configured domain.')
            elif result == z3.unknown: report.add('warning', 'UNKNOWN_T', f'{scenario.id}.T satisfiability is undecided: {solver.reason_unknown()}')
            valid.append((scenario, testing))
        except Exception as exc:
            report.add('error', 'EXPRESSION_ERROR', f'{scenario.id}: {exc}')
    for left, (ls, lt) in enumerate(valid):
        for rs, rt in valid[left + 1:]:
            solver = _solver(spec)
            solver.add(domain, lt, rt)
            result = solver.check()
            if result == z3.sat:
                report.add('error', 'NON_EXCLUSIVE_T', f'{ls.id}.T and {rs.id}.T overlap.', model_as_dict(solver.model(), inputs, spec.inputs))
            elif result == z3.unknown:
                report.add('warning', 'UNKNOWN_EXCLUSIVITY', f'Input exclusivity of {ls.id} and {rs.id} is undecided.')
    if valid:
        solver = _solver(spec)
        solver.add(domain, z3.Not(z3.Or(*[t for _, t in valid])))
        result = solver.check()
        if result == z3.sat:
            report.add('warning', 'INCOMPLETE_INPUT_FAMILY', 'Scenarios cover only part of the configured domain.', model_as_dict(solver.model(), inputs, spec.inputs))
        elif result == z3.unknown:
            report.add('warning', 'UNKNOWN_INPUT_COVERAGE', 'Scenario-family coverage is undecided.')
    return report


def _solver(spec):
    solver = z3.Solver()
    solver.set(timeout=spec.config.solver_timeout_ms, random_seed=spec.config.random_seed)
    return solver
