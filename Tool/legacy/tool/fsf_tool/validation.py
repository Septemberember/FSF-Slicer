from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import z3

from .expression import ExpressionEngine, domain_constraint, expression_variables, make_symbol, model_as_dict, model_value, parse_expression
from .java_frontend import JavaProgram
from .models import FSFSpec, ValidationIssue, VariableSpec


@dataclass(slots=True)
class ValidationReport:
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)

    def add(self, severity: str, code: str, message: str, counterexample: dict[str, Any] | None = None) -> None:
        self.issues.append(ValidationIssue(severity, code, message, counterexample))


def reconcile_spec(program: JavaProgram, spec: FSFSpec) -> FSFSpec:
    if spec.method is None:
        spec.method = program.method_name
    if not spec.inputs:
        spec.inputs = {name: VariableSpec(name, kind) for name, kind in program.parameters.items()}
    if not spec.outputs:
        spec.outputs = {"return_value": VariableSpec("return_value", program.return_type, source="return")}
    return spec


def validate_fsf(program: JavaProgram, spec: FSFSpec) -> ValidationReport:
    report = ValidationReport()
    if spec.method != program.method_name:
        report.add("error", "METHOD_MISMATCH", f"FSF selects '{spec.method}', parsed method is '{program.method_name}'.")
    params = program.parameters
    if set(spec.inputs) != set(params):
        missing = sorted(set(params) - set(spec.inputs))
        extra = sorted(set(spec.inputs) - set(params))
        if missing:
            report.add("error", "MISSING_INPUTS", f"FSF is missing method inputs: {', '.join(missing)}")
        if extra:
            report.add("error", "UNKNOWN_INPUTS", f"FSF declares non-parameter inputs: {', '.join(extra)}")
    for name in set(params) & set(spec.inputs):
        if _normalize(params[name]) != _normalize(spec.inputs[name].type):
            report.add("error", "TYPE_MISMATCH", f"Input '{name}' is {params[name]} in Java but {spec.inputs[name].type} in FSF.")
    if "return_value" in spec.outputs and _normalize(spec.outputs["return_value"].type) != _normalize(program.return_type):
        report.add("error", "RETURN_TYPE_MISMATCH", f"Java returns {program.return_type}, FSF return_value is {spec.outputs['return_value'].type}.")

    try:
        input_symbols = {name: make_symbol(name, variable.type) for name, variable in spec.inputs.items()}
        output_symbols = {name: make_symbol(name, variable.type) for name, variable in spec.outputs.items()}
    except Exception as exc:
        report.add("error", "UNSUPPORTED_TYPE", str(exc))
        return report
    domain = domain_constraint(input_symbols, spec.inputs, spec.config)
    engine = ExpressionEngine({**{n: v.type for n, v in spec.inputs.items()}, **{n: v.type for n, v in spec.outputs.items()}})
    testing_expressions: list[Any] = []
    defining_expressions: list[Any] = []
    valid_scenarios: list[int] = []

    for index, scenario in enumerate(spec.scenarios):
        try:
            t_vars = expression_variables(scenario.testing_condition)
            d_vars = expression_variables(scenario.defining_condition)
            unknown = (t_vars | d_vars) - set(spec.inputs) - set(spec.outputs)
            if unknown:
                report.add("error", "UNKNOWN_VARIABLE", f"{scenario.id} uses unknown variables: {', '.join(sorted(unknown))}")
                continue
            bad_t = t_vars - set(spec.inputs)
            if bad_t:
                report.add("error", "OUTPUT_IN_T", f"{scenario.id}.T may contain only inputs; found: {', '.join(sorted(bad_t))}")
            if not (d_vars & set(spec.outputs)):
                report.add("error", "NO_OUTPUT_IN_D", f"{scenario.id}.D must constrain at least one configured output.")
            testing = engine.evaluate(parse_expression(scenario.testing_condition), input_symbols)
            defining = engine.evaluate(parse_expression(scenario.defining_condition), {**input_symbols, **output_symbols})
            solver = _solver(spec)
            solver.add(domain, testing)
            check = solver.check()
            if check == z3.unsat:
                report.add("error", "UNSAT_T", f"{scenario.id}.T is unsatisfiable in the configured input domain.")
            elif check == z3.unknown:
                report.add("warning", "UNKNOWN_T", f"Z3 could not decide satisfiability of {scenario.id}.T.")
            testing_expressions.append(testing)
            defining_expressions.append(defining)
            valid_scenarios.append(index)
        except Exception as exc:
            report.add("error", "EXPRESSION_ERROR", f"{scenario.id}: {exc}")

    for left in range(len(testing_expressions)):
        for right in range(left + 1, len(testing_expressions)):
            solver = _solver(spec)
            solver.add(domain, testing_expressions[left], testing_expressions[right])
            if solver.check() == z3.sat:
                report.add(
                    "error",
                    "NON_EXCLUSIVE_T",
                    f"{spec.scenarios[valid_scenarios[left]].id}.T and {spec.scenarios[valid_scenarios[right]].id}.T overlap.",
                    model_as_dict(solver.model(), input_symbols, spec.inputs),
                )

    if testing_expressions:
        solver = _solver(spec)
        solver.add(domain, z3.Not(z3.Or(*testing_expressions)))
        result = solver.check()
        if result == z3.sat:
            report.add(
                "warning",
                "INCOMPLETE_INPUT_FAMILY",
                "The scenario testing conditions do not cover the configured input domain.",
                model_as_dict(solver.model(), input_symbols, spec.inputs),
            )
        elif result == z3.unknown:
            report.add("warning", "UNKNOWN_INPUT_COVERAGE", "Z3 could not decide FSF input-family completeness.")

    # Definition-level mutually exclusive outputs are a methodology prerequisite. Since D may use inputs,
    # this check existentially searches both input and output variables within the configured domain.
    for left in range(len(defining_expressions)):
        for right in range(left + 1, len(defining_expressions)):
            left_vars = expression_variables(spec.scenarios[valid_scenarios[left]].defining_condition)
            right_vars = expression_variables(spec.scenarios[valid_scenarios[right]].defining_condition)
            if (left_vars & set(spec.outputs)) != (right_vars & set(spec.outputs)):
                continue
            solver = _solver(spec)
            solver.add(domain, defining_expressions[left], defining_expressions[right])
            if solver.check() == z3.sat:
                example = {
                    **model_as_dict(solver.model(), input_symbols, spec.inputs),
                    **{name: model_value(solver.model(), symbol, spec.outputs[name].type) for name, symbol in output_symbols.items()},
                }
                report.add(
                    "warning",
                    "NON_EXCLUSIVE_D",
                    f"{spec.scenarios[valid_scenarios[left]].id}.D and {spec.scenarios[valid_scenarios[right]].id}.D can overlap.",
                    example,
                )
    return report


def _solver(spec: FSFSpec) -> z3.Solver:
    solver = z3.Solver()
    solver.set(timeout=spec.config.solver_timeout_ms)
    return solver


def _normalize(kind: str) -> str:
    return kind.replace("bool", "boolean").replace("java.lang.", "")
