"""Test-induced paths, coverage and output-set verification obligations."""
from __future__ import annotations
from itertools import product
import time
import z3

from .executor import ConcolicExecutor
from .expression import (ExpressionEngine, domain_constraint, make_symbol, model_as_dict,
                         model_value, parse_expression, z3_text, expression_variables, output_constraint)
from .java_frontend import JavaProgram
from .models import FSFSpec, FunctionalScenario, Judgment, PathRecord, ScenarioResult, TYPE_LIMITS
from .support import support_issues


MAX_ENUMERATED_OUTPUTS = 256


def exists(symbols, formula):
    return z3.Exists(symbols, formula) if symbols else formula


def inconclusive(scenario_id, reason):
    return ScenarioResult(scenario_id, Judgment('inconclusive', reason), Judgment('inconclusive', reason), 'unknown', [], [reason])


class TBFVEngine:
    def __init__(self, program: JavaProgram, spec: FSFSpec):
        self.program, self.spec = program, spec
        self.input_symbols = {n: make_symbol(n, v.type) for n, v in spec.inputs.items()}
        self.output_symbols = {n: make_symbol(n, v.type) for n, v in spec.outputs.items()}
        self.domain = domain_constraint(self.input_symbols, spec.inputs, spec.config)
        self.types = {n: v.type for n, v in {**spec.inputs, **spec.outputs}.items()}
        self.executor = ConcolicExecutor(program, spec, self.input_symbols)

    def verify(self, scenario: FunctionalScenario):
        started = time.perf_counter()
        issues = support_issues(self.program)
        if issues: return inconclusive(scenario.id, '; '.join(issues))
        engine = ExpressionEngine(self.types)
        try:
            testing = engine.evaluate_text(scenario.testing_condition, self.input_symbols)
            defined = parse_expression(scenario.defining_condition)
            output_names = expression_variables(defined) & set(self.spec.outputs)
        except Exception as exc:
            return inconclusive(scenario.id, f'Invalid or unsupported specification: {exc}')
        paths, completed, warnings = [], [], []
        generation_checks = 0
        generator = self._solver()
        generator.add(self.domain, testing, *engine.guards)
        seen = set()
        for index in range(1, self.spec.config.max_paths + 1):
            generation_checks += 1
            check = generator.check()
            if check == z3.unsat: break
            if check == z3.unknown:
                warnings.append('TEST_GENERATION_UNKNOWN: ' + generator.reason_unknown())
                break
            test = model_as_dict(generator.model(), self.input_symbols, self.spec.inputs)
            execution = self.executor.execute(test)
            condition = z3.simplify(execution.path_condition)
            key = condition.sexpr()
            if key in seen:
                warnings.append('DUPLICATE_PATH: execution did not refine the input region.')
                break
            # A path must contain its generating test; otherwise it cannot be trusted.
            if not z3.is_true(generator.model().eval(condition, model_completion=True)):
                warnings.append('PATH_MODEL_MISMATCH: derived condition excludes the generating test.')
                break
            seen.add(key)
            generator.add(z3.Not(condition))
            path = PathRecord(index, test, condition, z3_text(condition), dict(execution.outputs),
                              {n: z3_text(v) for n, v in execution.outputs.items()}, list(execution.trace),
                              execution.loop_iterations, execution.truncated, execution.exception)
            paths.append(path)
            if not execution.truncated and not (execution.exception or '').startswith('unsupported:') and (execution.exception or output_names <= set(execution.outputs)):
                completed.append(condition)
        coverage_solver = self._solver()
        coverage_solver.add(self.domain, testing, z3.Not(z3.Or(*completed)))
        coverage_check = coverage_solver.check()
        full = coverage_check == z3.unsat
        coverage = 'complete' if full else 'unknown' if coverage_check == z3.unknown else 'partial'
        if not full and len(paths) >= self.spec.config.max_paths:
            warnings.append(f'PATH_LIMIT: {self.spec.config.max_paths} paths.')
        if any(path.truncated for path in paths):
            warnings.append(f'LOOP_LIMIT: {self.spec.config.max_loop_iterations} total iterations per execution.')
        sound = self._soundness(scenario, defined, testing, paths, full, output_names)
        complete = self._completeness(scenario, defined, testing, paths, full, output_names)
        return ScenarioResult(scenario.id, sound, complete, coverage, paths, warnings,
                              (time.perf_counter() - started) * 1000, generation_checks)

    def _soundness(self, scenario, defining_ast, testing, paths, full, names):
        unresolved, usable = [], 0
        for path in paths:
            if path.truncated: continue
            if path.exception:
                if path.exception.startswith('unsupported:'):
                    unresolved.append(path.exception)
                    continue
                if not names <= set(path.outputs) or not any(self.spec.outputs[n].source == 'exception' for n in names):
                    return Judgment('unsound', 'A scenario input raises an exception instead of producing the specified outputs.', path.test_case)
            if not names <= set(path.outputs):
                unresolved.append('Configured outputs are unavailable at a normal exit.')
                continue
            usable += 1
            try:
                engine = ExpressionEngine(self.types)
                defining = engine.evaluate(defining_ast, {**self.input_symbols, **{n: path.outputs[n] for n in names}})
                outputs = {n: path.outputs[n] for n in names}
                bounds = output_constraint(outputs, self.spec.outputs)
                obligation = z3.And(defining, bounds, *engine.guards)
                solver = self._solver()
                solver.add(self.domain, testing, path.path_condition, z3.Not(obligation))
                check = solver.check()
                if check == z3.sat:
                    return Judgment('unsound', 'T ∧ C_i does not imply D(f_i(x)/y) and the declared output bounds.', model_as_dict(solver.model(), self.input_symbols, self.spec.inputs))
                if check == z3.unknown:
                    unresolved.append('SOUNDNESS_UNKNOWN: ' + solver.reason_unknown())
            except Exception as exc:
                unresolved.append(f'Unsupported soundness obligation: {exc}')
        if unresolved: return Judgment('inconclusive', '; '.join(dict.fromkeys(unresolved)))
        if not usable: return Judgment('inconclusive', 'No completed normal path establishes local soundness.')
        if full: return Judgment('sound', 'Every scenario input in the configured domain is covered, and every output satisfies D.')
        return Judgment('locally_sound', 'D holds on completed explored paths; scenario input coverage is partial.')

    def _completeness(self, scenario, defining_ast, testing, paths, full, names):
        usable = [p for p in paths if not (p.exception or '').startswith('unsupported:') and not p.truncated and names <= set(p.outputs) and (not p.exception or any(self.spec.outputs[n].source == 'exception' for n in names))]
        try:
            engine = ExpressionEngine(self.types)
            defining = engine.evaluate(defining_ast, {**self.input_symbols, **self.output_symbols})
            inputs = list(self.input_symbols.values())
            symbols = {n: self.output_symbols[n] for n in names}
            desired_relation = z3.And(self.domain, testing, defining,
                                      output_constraint(symbols, self.spec.outputs), *engine.guards)
            reached_relation = z3.Or(*[z3.And(self.domain, testing, p.path_condition,
                *[symbols[n] == p.outputs[n] for n in names]) for p in usable])
            finite = self._finite_completeness(symbols, desired_relation, reached_relation, full)
            if finite is not None:
                return finite
            desired = exists(inputs, desired_relation)
            reached = exists(inputs, reached_relation)
            solver = self._solver()
            solver.add(desired, z3.Not(reached))
            check = solver.check()
            if check == z3.unsat:
                return Judgment('complete', 'Every output in ∃x(domain ∧ T ∧ D) is reached on an explored path.')
            if check == z3.unknown:
                return Judgment('inconclusive', 'COMPLETENESS_UNKNOWN: ' + solver.reason_unknown())
            counterexample = {n: model_value(solver.model(), s, self.spec.outputs[n].type) for n, s in symbols.items()}
            if full:
                return Judgment('incomplete', 'Full input coverage establishes that a specified output is unreachable.', counterexample)
            return Judgment('inconclusive', 'An output has not been reached, but incomplete input coverage cannot establish incompleteness.', counterexample)
        except Exception as exc:
            return Judgment('inconclusive', f'Unsupported completeness obligation: {exc}')

    def _finite_completeness(self, symbols, desired, reached, full):
        """Decide output inclusion exactly when the declared output product is small.

        Each SAT query existentially searches its own input witness. Combining
        desired and reached in one query would incorrectly require the same input.
        Never replace declared output bounds with the outputs observed so far.
        """
        names, domains, count = sorted(symbols), [], 1
        for name in names:
            spec = self.spec.outputs[name]
            if spec.type in {'boolean', 'bool'}:
                domain = (False, True)
            else:
                limits = TYPE_LIMITS.get(spec.type)
                if limits is None:
                    return None
                low = limits[0] if spec.minimum is None else spec.minimum
                high = limits[1] if spec.maximum is None else spec.maximum
                # Python len(range(...)) can overflow for the full Java long range.
                count *= high - low + 1
                if count > MAX_ENUMERATED_OUTPUTS:
                    return None
                domain = range(low, high + 1)
            if spec.type in {'boolean', 'bool'}:
                count *= 2
            if count > MAX_ENUMERATED_OUTPUTS:
                return None
            domains.append(domain)

        deadline = time.monotonic() + self.spec.config.solver_timeout_ms / 1000
        for values in product(*domains):
            substitutions = [(symbols[name], z3.BoolVal(value) if z3.is_bool(symbols[name])
                              else z3.BitVecVal(value, symbols[name].size()))
                             for name, value in zip(names, values)]
            for label, relation in [('specification', desired), ('reachability', reached)]:
                remaining = int((deadline - time.monotonic()) * 1000)
                if remaining <= 0:
                    return Judgment('inconclusive', 'COMPLETENESS_UNKNOWN: finite output check timed out.')
                solver = self._solver()
                solver.set(timeout=remaining)
                solver.add(z3.simplify(z3.substitute(relation, *substitutions)))
                check = solver.check()
                if check == z3.unknown:
                    return Judgment('inconclusive', f'COMPLETENESS_UNKNOWN: {label}: ' + solver.reason_unknown())
                if label == 'specification' and check == z3.unsat:
                    break
                if label == 'reachability' and check == z3.unsat:
                    counterexample = dict(zip(names, values))
                    if full:
                        return Judgment('incomplete', 'Full input coverage establishes that a specified output is unreachable.', counterexample)
                    return Judgment('inconclusive', 'An output has not been reached, but incomplete input coverage cannot establish incompleteness.', counterexample)
        return Judgment('complete', 'Every output in the declared finite output domain allowed by ∃x(domain ∧ T ∧ D) is reached on an explored path.')

    def _solver(self):
        solver = z3.Solver()
        solver.set(timeout=self.spec.config.solver_timeout_ms, random_seed=self.spec.config.random_seed)
        return solver
