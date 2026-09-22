from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import javalang
import z3

from .expression import ExpressionEngine, domain_constraint, make_symbol, parse_expression
from .java_frontend import JavaEmitter, JavaProgram, parse_java
from .models import FSFSpec, FunctionalScenario
from .pdg import PDGBuilder, ProgramDependenceGraph
from .pruning import BranchPruner
from .support import support_issues
from .java_parser import parse_compilation_unit


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
    core_node_ids: set[int] = field(default_factory=set)
    pruning_proofs: list[dict] = field(default_factory=list)
    elapsed_ms: float = 0.0


class FSFGuidedSlicer:
    def __init__(self, program: JavaProgram, spec: FSFSpec) -> None:
        self.program = program
        self.spec = spec
        output_sources = {name: variable.source or ("return" if name == "return_value" else name) for name, variable in spec.outputs.items()}
        self.support_issues = support_issues(program)
        try:
            self.pdg = PDGBuilder(program, output_sources).build() if not self.support_issues else None
        except Exception as exc:
            self.support_issues.append(f"Conservative source retention: {exc}")
            self.pdg = None
        self.symbols = {name: make_symbol(name, variable.type) for name, variable in spec.inputs.items()}
        self.domain = domain_constraint(self.symbols, spec.inputs, spec.config)
        self.engine = ExpressionEngine({name: variable.type for name, variable in spec.inputs.items()})
        self.original_metrics = metrics_for_source(program.source, program.method_name)
        self.backward_cache = {}

    def slice(self, scenario: FunctionalScenario, output_dir: str | Path | None = None) -> SliceResult:
        started = time.perf_counter()
        if self.pdg is None:
            result = SliceResult(scenario.id, self.program.source, None, set(), set(), {}, self.original_metrics, self.original_metrics, warnings=list(self.support_issues))
            self._write(result, output_dir)
            return result
        input_vars = self._scenario_inputs(scenario)
        output_vars = self._scenario_outputs(scenario)
        forward_starts = {self.pdg.parameter_nodes[name] for name in input_vars if name in self.pdg.parameter_nodes}
        export_starts: set[int] = set()
        for name in output_vars:
            export_starts |= self.pdg.export_nodes.get(name, set())
        if not export_starts:
            export_starts |= self.pdg.export_nodes.get("return_value", set())
        forward = self.pdg.forward_slice(forward_starts)
        key = frozenset(export_starts)
        if key not in self.backward_cache:
            self.backward_cache[key] = self.pdg.backward_slice(export_starts)
        backward = self.backward_cache[key]
        core = forward & backward
        # Exports are mandatory, including constants and dependencies on inputs
        # absent from T/D. Preserve termination, abrupt control and side effects.
        seeds = core | export_starts
        for node_id, node in self.pdg.nodes.items():
            ast = node.ast
            if isinstance(ast, (javalang.tree.ReturnStatement, javalang.tree.ThrowStatement,
                                javalang.tree.BreakStatement, javalang.tree.ContinueStatement,
                                javalang.tree.WhileStatement, javalang.tree.DoStatement, javalang.tree.ForStatement)):
                seeds.add(node_id)
            if ast is not None and any(isinstance(child, (javalang.tree.MethodInvocation, javalang.tree.ClassCreator)) or
                    isinstance(child, javalang.tree.Assignment) and (not isinstance(ast, javalang.tree.StatementExpression) or child is not ast.expression or getattr(child.expressionl, 'qualifier', None) or getattr(child.expressionl, 'selectors', None) or child.type in {'/=', '%='}) or
                    isinstance(child, javalang.tree.BinaryOperation) and child.operator in {'/', '%'} or
                    bool(getattr(child, 'selectors', None)) or
                    any(op in {'++', '--'} for op in (getattr(child, 'prefix_operators', None) or []) + (getattr(child, 'postfix_operators', None) or []))
                    for _, child in ast):
                # Scalar assignments are handled by data dependencies; retain
                # compound assignments and embedded mutation conservatively.
                seeds.add(node_id)
        closure = self.pdg.backward_slice(seeds)
        if self.spec.config.slicing_mode in {'backward', 'conditioned'}:
            closure |= backward
        declarations = {}
        for i, node in self.pdg.nodes.items():
            if isinstance(node.ast, javalang.tree.LocalVariableDeclaration):
                for name in node.defs: declarations.setdefault(name, set()).add(i)
        while True:
            needed = set().union(*(self.pdg.nodes[i].uses | self.pdg.nodes[i].defs for i in closure)) if closure else set()
            expanded = self.pdg.backward_slice(closure | set().union(*(declarations.get(name, set()) for name in needed)))
            if expanded == closure: break
            closure = expanded
        # Control nodes are required for executable reconstruction; pseudo parameter nodes are not emitted.
        emitted_ids = {node_id for node_id in closure if not self.pdg.nodes[node_id].pseudo}
        pruner = BranchPruner(self.spec, self.symbols, self.domain)
        testing = self.engine.evaluate(parse_expression(scenario.testing_condition), self.symbols)
        pruned = {} if self.spec.config.slicing_mode == 'backward' else pruner.run(self.program.method.body or [], testing)
        emitter = JavaEmitter(self.program, emitted_ids, self.pdg.node_ids, pruned)
        warnings = []
        try:
            source = emitter.emit()
        except Exception as exc:
            source = self.program.source
            pruned = {}
            emitted_ids = {i for i, n in self.pdg.nodes.items() if not n.pseudo}
            warnings.append(f"Original source retained because reconstruction was unavailable: {exc}")
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
        original = self.original_metrics
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
            core_node_ids=core,
            pruning_proofs=pruner.proofs if pruned else [],
            elapsed_ms=(time.perf_counter() - started) * 1000,
            warnings=warnings,
        )

    def _write(self, result, output_dir):
        if output_dir is not None:
            folder = Path(output_dir) / result.scenario_id
            folder.mkdir(parents=True, exist_ok=True)
            result.output_path = folder / f'{self.program.class_name}.java'
            result.output_path.write_text(result.source, encoding='utf-8')

    def _scenario_inputs(self, scenario: FunctionalScenario) -> set[str]:
        from .expression import expression_variables

        return (expression_variables(scenario.testing_condition) | expression_variables(scenario.defining_condition)) & set(self.spec.inputs)

    def _scenario_outputs(self, scenario: FunctionalScenario) -> set[str]:
        from .expression import expression_variables

        return expression_variables(scenario.defining_condition) & set(self.spec.outputs)


def compile_slice(result: SliceResult, javac: str = "javac") -> SliceResult:
    if result.output_path is None:
        result.compile_ok = None
        result.compile_message = "Slice was not written to disk."
        return result
    try:
        process = subprocess.run(
            [javac, "-proc:none", "-encoding", "UTF-8", "-d", str(result.output_path.parent), str(result.output_path)],
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
    try:
        loc = len({token.position.line for token in javalang.tokenizer.tokenize(source)})
    except Exception:
        loc = sum(bool(line.strip()) for line in source.splitlines())
    try:
        tree = parse_compilation_unit(source)
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
