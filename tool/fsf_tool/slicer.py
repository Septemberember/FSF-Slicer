from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import javalang
import z3

from .expression import ExpressionEngine, domain_constraint, make_symbol, parse_expression
from .java_frontend import JavaEmitter, JavaProgram, parse_java
from .models import FSFSpec, FunctionalScenario
from .pdg import PDGBuilder, ProgramDependenceGraph


@dataclass(slots=True)
class ProgramMetrics:
    loc: int
    executable_statements: int
    cyclomatic_complexity: int

    def as_dict(self) -> dict[str, int]:
        return {
            "loc": self.loc,
            "executable_statements": self.executable_statements,
            "cyclomatic_complexity": self.cyclomatic_complexity,
        }


@dataclass(slots=True)
class SliceResult:
    scenario_id: str
    source: str
    output_path: Path | None
    kept_node_ids: set[int]
    removed_node_ids: set[int]
    pruned_branches: dict[int, bool]
    original_metrics: ProgramMetrics
    slice_metrics: ProgramMetrics
    compile_ok: bool | None = None
    compile_message: str = ""
    warnings: list[str] = field(default_factory=list)


class FSFGuidedSlicer:
    def __init__(self, program: JavaProgram, spec: FSFSpec) -> None:
        self.program = program
        self.spec = spec
        output_sources = {name: variable.source or ("return" if name == "return_value" else name) for name, variable in spec.outputs.items()}
        self.pdg: ProgramDependenceGraph = PDGBuilder(program, output_sources).build()
        self.symbols = {name: make_symbol(name, variable.type) for name, variable in spec.inputs.items()}
        self.domain = domain_constraint(self.symbols, spec.inputs, spec.config)
        self.engine = ExpressionEngine({name: variable.type for name, variable in spec.inputs.items()})

    def slice(self, scenario: FunctionalScenario, output_dir: str | Path | None = None) -> SliceResult:
        input_vars = self._scenario_inputs(scenario)
        output_vars = self._scenario_outputs(scenario)
        forward_starts = {self.pdg.parameter_nodes[name] for name in input_vars if name in self.pdg.parameter_nodes}
        export_starts: set[int] = set()
        for name in output_vars:
            export_starts |= self.pdg.export_nodes.get(name, set())
        if not export_starts:
            export_starts |= self.pdg.export_nodes.get("return_value", set())
        forward = self.pdg.forward_slice(forward_starts) if forward_starts else set(self.pdg.nodes)
        backward = self.pdg.backward_slice(export_starts)
        core = forward & backward
        if not core:
            core = backward
        closure = self.pdg.backward_slice(core) | core
        # Control nodes are required for executable reconstruction; pseudo parameter nodes are not emitted.
        emitted_ids = {node_id for node_id in closure if not self.pdg.nodes[node_id].pseudo}
        pruned = self._prune_branches(scenario)
        emitter = JavaEmitter(self.program, emitted_ids, self.pdg.node_ids, pruned)
        source = emitter.emit()
        output_path = None
        if output_dir is not None:
            folder = Path(output_dir)
            folder.mkdir(parents=True, exist_ok=True)
            output_path = folder / f"{self.program.class_name}_{scenario.id}_Slice.java"
            # Java requires the file name to match a public class. Use a scenario subfolder and original file name.
            scenario_folder = folder / scenario.id
            scenario_folder.mkdir(parents=True, exist_ok=True)
            output_path = scenario_folder / f"{self.program.class_name}.java"
            output_path.write_text(source, encoding="utf-8")
        original = metrics_for_source(self.program.source, self.program.method_name)
        sliced = metrics_for_source(source, self.program.method_name)
        all_emitted = {node_id for node_id, node in self.pdg.nodes.items() if not node.pseudo}
        return SliceResult(
            scenario_id=scenario.id,
            source=source,
            output_path=output_path,
            kept_node_ids=emitted_ids,
            removed_node_ids=all_emitted - emitted_ids,
            pruned_branches=pruned,
            original_metrics=original,
            slice_metrics=sliced,
        )

    def _scenario_inputs(self, scenario: FunctionalScenario) -> set[str]:
        from .expression import expression_variables

        return (expression_variables(scenario.testing_condition) | expression_variables(scenario.defining_condition)) & set(self.spec.inputs)

    def _scenario_outputs(self, scenario: FunctionalScenario) -> set[str]:
        from .expression import expression_variables

        return expression_variables(scenario.defining_condition) & set(self.spec.outputs)

    def _prune_branches(self, scenario: FunctionalScenario) -> dict[int, bool]:
        decisions: dict[int, bool] = {}
        try:
            testing = self.engine.evaluate(parse_expression(scenario.testing_condition), self.symbols)
        except Exception:
            return decisions
        input_names = set(self.symbols)
        for node in self.program.method.body or []:
            self._prune_walk(node, testing, input_names, decisions)
        return decisions

    def _prune_walk(self, node: Any, testing: Any, input_names: set[str], decisions: dict[int, bool]) -> None:
        from .expression import collect_uses

        if node is None:
            return
        if isinstance(node, javalang.tree.BlockStatement):
            for child in node.statements:
                self._prune_walk(child, testing, input_names, decisions)
            return
        if isinstance(node, javalang.tree.IfStatement):
            if collect_uses(node.condition) <= input_names:
                try:
                    condition = self.engine.evaluate(node.condition, self.symbols)
                    true_solver = z3.Solver()
                    false_solver = z3.Solver()
                    for solver in (true_solver, false_solver):
                        solver.set(timeout=self.spec.config.solver_timeout_ms)
                    true_solver.add(self.domain, testing, condition)
                    false_solver.add(self.domain, testing, z3.Not(condition))
                    true_sat = true_solver.check()
                    false_sat = false_solver.check()
                    if true_sat == z3.unsat:
                        decisions[id(node)] = False
                    elif false_sat == z3.unsat:
                        decisions[id(node)] = True
                except Exception:
                    pass
            self._prune_walk(node.then_statement, testing, input_names, decisions)
            self._prune_walk(node.else_statement, testing, input_names, decisions)
        elif isinstance(node, (javalang.tree.WhileStatement, javalang.tree.DoStatement, javalang.tree.ForStatement)):
            self._prune_walk(node.body, testing, input_names, decisions)


def compile_slice(result: SliceResult, javac: str = "javac") -> SliceResult:
    if result.output_path is None:
        result.compile_ok = None
        result.compile_message = "Slice was not written to disk."
        return result
    try:
        process = subprocess.run(
            [javac, "-d", str(result.output_path.parent), str(result.output_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        result.compile_ok = process.returncode == 0
        result.compile_message = (process.stdout + process.stderr).strip()
    except Exception as exc:
        result.compile_ok = False
        result.compile_message = str(exc)
    return result


def metrics_for_source(source: str, method_name: str | None = None) -> ProgramMetrics:
    loc = sum(1 for line in source.splitlines() if line.strip() and not line.strip().startswith("//"))
    try:
        temp = Path("__memory__.java")
        tree = javalang.parse.parse(source)
        methods = [method for _, method in tree.filter(javalang.tree.MethodDeclaration)]
        if method_name:
            methods = [method for method in methods if method.name == method_name] or methods
        method = methods[0]
        statements = 0
        complexity = 1
        branch_types = (
            javalang.tree.IfStatement,
            javalang.tree.WhileStatement,
            javalang.tree.DoStatement,
            javalang.tree.ForStatement,
            javalang.tree.CatchClause,
        )
        executable_types = (
            javalang.tree.LocalVariableDeclaration,
            javalang.tree.StatementExpression,
            javalang.tree.ReturnStatement,
            javalang.tree.ThrowStatement,
            javalang.tree.BreakStatement,
            javalang.tree.ContinueStatement,
        )
        for _, node in method:
            if isinstance(node, executable_types):
                statements += 1
            if isinstance(node, branch_types):
                complexity += 1
            if isinstance(node, javalang.tree.BinaryOperation) and node.operator in {"&&", "||"}:
                complexity += 1
            if isinstance(node, javalang.tree.SwitchStatementCase) and node.case:
                complexity += 1
        return ProgramMetrics(loc, statements, complexity)
    except Exception:
        return ProgramMetrics(loc, 0, 0)
