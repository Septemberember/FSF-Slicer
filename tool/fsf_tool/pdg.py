from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import javalang

from .expression import collect_uses
from .java_frontend import JavaProgram, expression_source


@dataclass(slots=True)
class PDGNode:
    id: int
    ast: Any
    kind: str
    line: int | None
    text: str
    defs: set[str] = field(default_factory=set)
    uses: set[str] = field(default_factory=set)
    control_parents: set[int] = field(default_factory=set)
    pseudo: bool = False


@dataclass(slots=True)
class ProgramDependenceGraph:
    nodes: dict[int, PDGNode]
    edges: dict[int, set[int]]
    reverse_edges: dict[int, set[int]]
    node_ids: dict[int, int]
    parameter_nodes: dict[str, int]
    export_nodes: dict[str, set[int]]

    def forward_slice(self, starts: set[int]) -> set[int]:
        return self._reach(starts, self.edges)

    def backward_slice(self, starts: set[int]) -> set[int]:
        return self._reach(starts, self.reverse_edges)

    @staticmethod
    def _reach(starts: set[int], adjacency: dict[int, set[int]]) -> set[int]:
        seen = set(starts)
        stack = list(starts)
        while stack:
            current = stack.pop()
            for nxt in adjacency.get(current, set()):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen


class PDGBuilder:
    def __init__(self, program: JavaProgram, outputs: dict[str, str]) -> None:
        self.program = program
        self.outputs = outputs
        self.nodes: dict[int, PDGNode] = {}
        self.node_ids: dict[int, int] = {}
        self.parameter_nodes: dict[str, int] = {}
        self.export_nodes: dict[str, set[int]] = {name: set() for name in outputs}
        self._next = 1

    def build(self) -> ProgramDependenceGraph:
        for name in self.program.parameters:
            node_id = self._add(None, "parameter", None, f"parameter {name}", {name}, set(), set(), pseudo=True)
            self.parameter_nodes[name] = node_id
        self._walk_many(self.program.method.body or [], set())

        edges: dict[int, set[int]] = {node_id: set() for node_id in self.nodes}
        reverse: dict[int, set[int]] = {node_id: set() for node_id in self.nodes}
        definitions: dict[str, set[int]] = {}
        for node in self.nodes.values():
            for name in node.defs:
                definitions.setdefault(name, set()).add(node.id)
        for node in self.nodes.values():
            for parent in node.control_parents:
                self._edge(parent, node.id, edges, reverse)
            for name in node.uses:
                for source in definitions.get(name, set()):
                    if source != node.id:
                        self._edge(source, node.id, edges, reverse)
        return ProgramDependenceGraph(
            nodes=self.nodes,
            edges=edges,
            reverse_edges=reverse,
            node_ids=self.node_ids,
            parameter_nodes=self.parameter_nodes,
            export_nodes=self.export_nodes,
        )

    @staticmethod
    def _edge(source: int, target: int, edges: dict[int, set[int]], reverse: dict[int, set[int]]) -> None:
        edges[source].add(target)
        reverse[target].add(source)

    def _add(
        self,
        ast_node: Any,
        kind: str,
        line: int | None,
        text: str,
        defs: set[str],
        uses: set[str],
        controls: set[int],
        pseudo: bool = False,
    ) -> int:
        node_id = self._next
        self._next += 1
        self.nodes[node_id] = PDGNode(node_id, ast_node, kind, line, text, defs, uses, set(controls), pseudo)
        if ast_node is not None:
            self.node_ids[id(ast_node)] = node_id
        return node_id

    def _walk_many(self, statements: list[Any], controls: set[int]) -> None:
        for statement in statements:
            self._walk(statement, controls)

    def _walk(self, node: Any, controls: set[int]) -> None:
        if node is None:
            return
        if isinstance(node, javalang.tree.BlockStatement):
            self._walk_many(node.statements, controls)
            return
        defs, uses, text = statement_def_use(node)
        line = getattr(getattr(node, "position", None), "line", None)
        node_id = self._add(node, type(node).__name__, line, text, defs, uses, controls)
        if isinstance(node, javalang.tree.ReturnStatement):
            for output, source in self.outputs.items():
                if source == "return" or output == "return_value":
                    self.export_nodes.setdefault(output, set()).add(node_id)
        for output, source in self.outputs.items():
            if source != "return" and source in defs:
                self.export_nodes.setdefault(output, set()).add(node_id)
        nested_controls = controls | {node_id}
        if isinstance(node, javalang.tree.IfStatement):
            self._walk(node.then_statement, nested_controls)
            self._walk(node.else_statement, nested_controls)
        elif isinstance(node, (javalang.tree.WhileStatement, javalang.tree.DoStatement, javalang.tree.ForStatement)):
            self._walk(node.body, nested_controls)
        elif isinstance(node, javalang.tree.SwitchStatement):
            for case in node.cases:
                self._walk_many(case.statements, nested_controls)
        elif isinstance(node, javalang.tree.TryStatement):
            self._walk_many(node.block, nested_controls)
            for catch in node.catches:
                self._walk_many(catch.block, nested_controls)
            self._walk_many(node.finally_block or [], nested_controls)


def statement_def_use(node: Any) -> tuple[set[str], set[str], str]:
    defs: set[str] = set()
    uses: set[str] = set()
    text = type(node).__name__
    if isinstance(node, javalang.tree.LocalVariableDeclaration):
        items = []
        for declarator in node.declarators:
            defs.add(declarator.name)
            uses |= collect_uses(declarator.initializer)
            items.append(declarator.name)
        text = "declare " + ", ".join(items)
    elif isinstance(node, javalang.tree.StatementExpression):
        expression = node.expression
        text = expression_source(expression)
        if isinstance(expression, javalang.tree.Assignment):
            target = _assignment_target(expression.expressionl)
            if target:
                defs.add(target)
                if expression.type != "=":
                    uses.add(target)
            uses |= collect_uses(expression.value)
        elif isinstance(expression, javalang.tree.MemberReference) and any(op in {"++", "--"} for op in (expression.prefix_operators or []) + (expression.postfix_operators or [])):
            defs.add(expression.member)
            uses.add(expression.member)
        else:
            uses |= collect_uses(expression)
    elif isinstance(node, javalang.tree.ReturnStatement):
        defs.add("return_value")
        uses |= collect_uses(node.expression)
        text = "return " + expression_source(node.expression)
    elif isinstance(node, javalang.tree.IfStatement):
        uses |= collect_uses(node.condition)
        text = "if " + expression_source(node.condition)
    elif isinstance(node, (javalang.tree.WhileStatement, javalang.tree.DoStatement)):
        uses |= collect_uses(node.condition)
        text = "loop " + expression_source(node.condition)
    elif isinstance(node, javalang.tree.ForStatement):
        control = node.control
        if isinstance(control, javalang.tree.EnhancedForControl):
            defs |= {decl.name for decl in control.var.declarators}
            uses |= collect_uses(control.iterable)
        else:
            initializers = [control.init] if isinstance(control.init, javalang.tree.VariableDeclaration) else (control.init or [])
            for init in initializers:
                if isinstance(init, javalang.tree.VariableDeclaration):
                    for decl in init.declarators:
                        defs.add(decl.name)
                        uses |= collect_uses(decl.initializer)
                else:
                    uses |= collect_uses(init)
            uses |= collect_uses(control.condition)
            for update in control.update or []:
                uses |= collect_uses(update)
                if isinstance(update, javalang.tree.MemberReference):
                    defs.add(update.member)
        text = "for"
    elif isinstance(node, javalang.tree.SwitchStatement):
        uses |= collect_uses(node.expression)
        text = "switch " + expression_source(node.expression)
    elif isinstance(node, javalang.tree.ThrowStatement):
        uses |= collect_uses(node.expression)
        text = "throw " + expression_source(node.expression)
    else:
        uses |= collect_uses(node)
    return defs, uses - defs if not isinstance(node, javalang.tree.StatementExpression) else uses, text


def _assignment_target(node: Any) -> str | None:
    if isinstance(node, javalang.tree.MemberReference):
        return node.member
    return None
