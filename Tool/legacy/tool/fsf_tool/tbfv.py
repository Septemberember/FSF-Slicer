from __future__ import annotations

import time
from typing import Any

import z3

from .executor import ConcolicExecutor
from .expression import ExpressionEngine, domain_constraint, make_symbol, model_as_dict, model_value, parse_expression, z3_text
from .java_frontend import JavaProgram
from .models import FSFSpec, FunctionalScenario, Judgment, PathRecord, ScenarioResult


class TBFVEngine:
    """Test-guided concolic path enumeration and FSF verification."""

    def __init__(self, program: JavaProgram, spec: FSFSpec) -> None:
        self.program = program
        self.spec = spec
        self.input_symbols = {name: make_symbol(name, variable.type) for name, variable in spec.inputs.items()}
        self.input_types = {name: variable.type for name, variable in spec.inputs.items()}
        self.output_symbols = {name: make_symbol(name, variable.type) for name, variable in spec.outputs.items()}
        self.domain = domain_constraint(self.input_symbols, spec.inputs, spec.config)
        output_bounds = []
        for name, variable in spec.outputs.items():
            if variable.minimum is not None:
                output_bounds.append(self.output_symbols[name] >= variable.minimum)
            if variable.maximum is not None:
                output_bounds.append(self.output_symbols[name] <= variable.maximum)
        self.output_domain = z3.And(*output_bounds) if output_bounds else z3.BoolVal(True)
        self.expression = ExpressionEngine({**self.input_types, **{name: var.type for name, var in spec.outputs.items()}})
        self.executor = ConcolicExecutor(program, spec, self.input_symbols)

    def verify(self, scenario: FunctionalScenario) -> ScenarioResult:
        started = time.perf_counter()
        testing = self.expression.evaluate(parse_expression(scenario.testing_condition), self.input_symbols)
        paths: list[PathRecord] = []
        path_formulas: list[Any] = []
        completed_formulas: list[Any] = []
        seen: set[str] = set()
        warnings: list[str] = []
        exploration_exhausted = False

        for index in range(1, self.spec.config.max_paths + 1):
            solver = self._solver()
            exclusions = z3.Not(z3.Or(*path_formulas)) if path_formulas else z3.BoolVal(True)
            solver.add(self.domain, testing, exclusions)
            check = solver.check()
            if check == z3.unsat:
                exploration_exhausted = True
                break
            if check == z3.unknown:
                warnings.append("Z3 returned unknown while generating the next test case.")
                break
            test_case = model_as_dict(solver.model(), self.input_symbols, self.spec.inputs)
            execution = self.executor.execute(test_case)
            path_condition = z3.simplify(execution.path_condition)
            key = path_condition.sexpr()
            if key in seen:
                warnings.append("A duplicate symbolic path was produced; exploration stopped to avoid cycling.")
                break
            seen.add(key)
            path_formulas.append(path_condition)
            if not execution.truncated and not (execution.exception or "").startswith("unsupported:"):
                completed_formulas.append(path_condition)
            paths.append(
                PathRecord(
                    index=index,
                    test_case=test_case,
                    path_condition=path_condition,
                    path_condition_text=z3_text(path_condition),
                    outputs=dict(execution.outputs),
                    output_text={name: z3_text(value) for name, value in execution.outputs.items()},
                    trace=list(execution.trace),
                    loop_iterations=execution.loop_iterations,
                    truncated=execution.truncated,
                    exception=execution.exception,
                )
            )

        coverage_solver = self._solver()
        covered = z3.Or(*completed_formulas) if completed_formulas else z3.BoolVal(False)
        coverage_solver.add(self.domain, testing, z3.Not(covered))
        coverage_check = coverage_solver.check()
        full_coverage = coverage_check == z3.unsat
        coverage = "complete" if full_coverage else ("unknown" if coverage_check == z3.unknown else "partial")
        if not exploration_exhausted and not full_coverage and len(paths) >= self.spec.config.max_paths:
            warnings.append(f"Path limit {self.spec.config.max_paths} reached; global judgments are not claimed.")
        if any(path.truncated for path in paths):
            warnings.append("At least one execution reached the loop bound; results are local to explored bounded paths.")

        soundness = self._soundness(scenario, testing, paths, full_coverage)
        completeness = self._completeness(scenario, testing, paths, full_coverage)
        elapsed = (time.perf_counter() - started) * 1000
        return ScenarioResult(scenario.id, soundness, completeness, coverage, paths, warnings, elapsed)

    def _soundness(self, scenario: FunctionalScenario, testing: Any, paths: list[PathRecord], full_coverage: bool) -> Judgment:
        for path in paths:
            if path.exception:
                if path.exception.startswith("unsupported:"):
                    return Judgment("inconclusive", path.exception)
                return Judgment("unsound", "An explored input caused an exception or unsupported execution.", path.test_case)
            if path.truncated:
                continue
            if not all(name in path.outputs for name in self.spec.outputs):
                return Judgment("inconclusive", "The configured outputs were not available on every explored path.")
            env = {**self.input_symbols, **path.outputs}
            defining = self.expression.evaluate(parse_expression(scenario.defining_condition), env)
            solver = self._solver()
            solver.add(self.domain, testing, path.path_condition, z3.Not(defining))
            result = solver.check()
            if result == z3.sat:
                return Judgment(
                    "unsound",
                    "T ∧ C_i does not imply D(f_i(x)/y).",
                    model_as_dict(solver.model(), self.input_symbols, self.spec.inputs),
                )
            if result == z3.unknown:
                return Judgment("inconclusive", "Z3 could not decide a path soundness obligation.")
        if full_coverage:
            return Judgment("sound", "Every covered path satisfies D and T is fully covered by the derived path conditions.")
        return Judgment("locally_sound", "Every explored path satisfies D, but the path conditions do not cover all of T.")

    def _completeness(self, scenario: FunctionalScenario, testing: Any, paths: list[PathRecord], full_coverage: bool) -> Judgment:
        usable = [path for path in paths if not path.exception and not path.truncated and all(name in path.outputs for name in self.spec.outputs)]
        if not usable:
            return Judgment("inconclusive", "No completed execution path is available for completeness checking.")
        d_env = {**self.input_symbols, **self.output_symbols}
        defining = self.expression.evaluate(parse_expression(scenario.defining_condition), d_env)
        inputs = list(self.input_symbols.values())
        specified_outputs = z3.And(self.output_domain, z3.Exists(inputs, z3.And(self.domain, testing, defining)))
        reachability_terms: list[Any] = []
        for path in usable:
            equalities = [self.output_symbols[name] == path.outputs[name] for name in self.spec.outputs]
            reachability_terms.append(z3.Exists(inputs, z3.And(self.domain, testing, path.path_condition, *equalities)))
        reachable_outputs = z3.Or(*reachability_terms)
        solver = self._solver()
        solver.add(specified_outputs, z3.Not(reachable_outputs))
        result = solver.check()
        if result == z3.unsat:
            return Judgment("complete", "Every output allowed by ∃x(T ∧ D) is reachable on an explored path.")
        if result == z3.unknown:
            return Judgment("inconclusive", "Z3 could not decide the quantified completeness obligation.")
        counterexample = {
            name: model_value(solver.model(), symbol, self.spec.outputs[name].type)
            for name, symbol in self.output_symbols.items()
        }
        if full_coverage:
            return Judgment("incomplete", "An output allowed by D is unreachable although T is fully path-covered.", counterexample)
        return Judgment("locally_complete", "An allowed output is not reached in the explored paths, but T is only partially covered.", counterexample)

    def _solver(self) -> z3.Solver:
        solver = z3.Solver()
        solver.set(timeout=self.spec.config.solver_timeout_ms)
        return solver
