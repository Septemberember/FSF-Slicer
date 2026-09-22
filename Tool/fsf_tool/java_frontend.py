from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import javalang

from .errors import JavaParseError, UnsupportedJavaError
from .expression import type_to_string
from .java_parser import parse_compilation_unit


@dataclass(slots=True)
class JavaProgram:
    path: Path
    source: str
    tree: Any
    class_decl: Any
    method: Any

    @property
    def class_name(self) -> str:
        return self.class_decl.name

    @property
    def method_name(self) -> str:
        return self.method.name

    @property
    def parameters(self) -> dict[str, str]:
        return {parameter.name: type_to_string(parameter.type) for parameter in self.method.parameters}

    @property
    def return_type(self) -> str:
        return type_to_string(self.method.return_type)


def parse_java(path: str | Path, method_name: str | None = None) -> JavaProgram:
    source_path = Path(path)
    source = source_path.read_text(encoding="utf-8")
    try:
        tree = parse_compilation_unit(source)
    except Exception as exc:
        detail = getattr(exc, 'description', None) or str(exc)
        at = getattr(exc, 'at', None)
        raise JavaParseError(f"Cannot parse {source_path}: {detail}" + (f' at {at}' if at else '')) from exc
    classes = [item for item in tree.types if isinstance(item, (javalang.tree.ClassDeclaration, javalang.tree.EnumDeclaration))]
    if not classes:
        raise JavaParseError(f"No Java class found in {source_path}")
    class_decl = classes[0]
    methods = list(class_decl.methods)
    if method_name:
        matches = [method for method in methods if method.name == method_name]
        if not matches:
            raise JavaParseError(f"Method '{method_name}' not found in {source_path}")
        if len(matches) != 1:
            raise JavaParseError(f"Ambiguous overloaded method '{method_name}'; provide a source with one matching declaration.")
        method = matches[0]
    else:
        candidates = [m for m in methods if m.name != "main" and "static" in (m.modifiers or set())]
        method = candidates[0] if candidates else (methods[0] if methods else None)
    if method is None:
        raise JavaParseError(f"No method found in {source_path}")
    return JavaProgram(source_path, source, tree, class_decl, method)


def expression_source(node: Any) -> str:
    if node is None:
        return ""
    prefix = " ".join(getattr(node, "prefix_operators", None) or [])
    postfix = "".join(getattr(node, "postfix_operators", None) or [])
    selectors = "".join(selector_source(item) for item in (getattr(node, "selectors", None) or []))
    if isinstance(node, javalang.tree.Literal):
        return f"{prefix}{node.value}{selectors}{postfix}"
    if isinstance(node, javalang.tree.MemberReference):
        base = f"{node.qualifier}." if node.qualifier else ""
        return f"{prefix}{base}{node.member}{selectors}{postfix}"
    if isinstance(node, javalang.tree.BinaryOperation):
        return f"{prefix}({expression_source(node.operandl)} {node.operator} {expression_source(node.operandr)}){postfix}"
    if isinstance(node, javalang.tree.TernaryExpression):
        return f"{prefix}({expression_source(node.condition)} ? {expression_source(node.if_true)} : {expression_source(node.if_false)}){postfix}"
    if isinstance(node, javalang.tree.Assignment):
        return f"{expression_source(node.expressionl)} {node.type} {expression_source(node.value)}"
    if isinstance(node, javalang.tree.Cast):
        return f"{prefix}(({type_to_string(node.type)}) {expression_source(node.expression)}){postfix}"
    if isinstance(node, javalang.tree.MethodInvocation):
        qualifier = f"{node.qualifier}." if node.qualifier else ""
        args = ", ".join(expression_source(arg) for arg in node.arguments)
        type_args = ""
        if node.type_arguments:
            type_args = "<" + ", ".join(type_to_string(item.type) for item in node.type_arguments) + ">"
        return f"{prefix}{qualifier}{type_args}{node.member}({args}){selectors}{postfix}"
    if isinstance(node, javalang.tree.ClassCreator):
        args = ", ".join(expression_source(arg) for arg in node.arguments)
        return f"new {type_to_string(node.type)}({args}){selectors}"
    if isinstance(node, javalang.tree.ArrayCreator):
        dimensions = "".join(f"[{expression_source(dim)}]" if dim else "[]" for dim in node.dimensions)
        initializer = initializer_source(node.initializer) if node.initializer else ""
        return f"new {type_to_string(node.type)}{dimensions}{initializer}"
    if isinstance(node, javalang.tree.ArrayInitializer):
        return initializer_source(node)
    if isinstance(node, javalang.tree.This):
        qualifier = f"{node.qualifier}." if node.qualifier else ""
        return f"{qualifier}this{selectors}"
    if isinstance(node, javalang.tree.LambdaExpression):
        params = ", ".join(getattr(p, "name", expression_source(p)) for p in node.parameters)
        body = expression_source(node.body) if not isinstance(node.body, list) else "{ /* lambda body */ }"
        return f"({params}) -> {body}"
    raise UnsupportedJavaError(f"Cannot emit expression node {type(node).__name__}")


def selector_source(node: Any) -> str:
    if isinstance(node, javalang.tree.ArraySelector):
        return f"[{expression_source(node.index)}]"
    if isinstance(node, javalang.tree.MethodInvocation):
        args = ", ".join(expression_source(arg) for arg in node.arguments)
        return f".{node.member}({args})"
    if isinstance(node, javalang.tree.MemberReference):
        return f".{node.member}"
    raise UnsupportedJavaError(f"Cannot emit selector {type(node).__name__}")


def initializer_source(node: Any) -> str:
    return "{" + ", ".join(expression_source(item) for item in node.initializers) + "}"


def _mods(modifiers: Iterable[str] | None) -> str:
    ordered = [item for item in ["public", "protected", "private", "abstract", "static", "final", "synchronized", "native"] if item in (modifiers or set())]
    return (" ".join(ordered) + " ") if ordered else ""


class JavaEmitter:
    def __init__(
        self,
        program: JavaProgram,
        keep_ids: set[int] | None = None,
        node_ids: dict[int, int] | None = None,
        pruned_branches: dict[int, bool] | None = None,
    ) -> None:
        self.program = program
        self.keep_ids = keep_ids
        self.node_ids = node_ids or {}
        self.pruned_branches = pruned_branches or {}

    def emit(self) -> str:
        # Preserve the compilation unit, including annotations, helper methods,
        # constructors, nested types and imports; replace only the selected body.
        source = self.program.source
        offsets = [0]
        for line in source.splitlines(keepends=True):
            offsets.append(offsets[-1] + len(line))
        def offset(position):
            return offsets[position.line - 1] + position.column - 1
        start = offset(self.program.method.position)
        tokens = [t for t in javalang.tokenizer.tokenize(source) if offset(t.position) >= start]
        method_name = next(i for i, token in enumerate(tokens[:-1]) if token.value == self.program.method.name and tokens[i+1].value == '(')
        cursor, parentheses = method_name + 2, 1
        while parentheses:
            token = tokens[cursor]
            if isinstance(token, javalang.tokenizer.Separator):
                parentheses += (token.value == '(') - (token.value == ')')
            cursor += 1
        opening = next(i for i in range(cursor, len(tokens)) if tokens[i].value == '{')
        depth = 1
        closing = opening + 1
        while depth:
            token = tokens[closing]
            if isinstance(token, javalang.tokenizer.Separator):
                depth += (token.value == '{') - (token.value == '}')
            if depth: closing += 1
        body = []
        for statement in self.program.method.body or []:
            body.extend(self._statement(statement, 2, True))
            if self._guaranteed_terminates(statement): break
        return source[:offset(tokens[opening].position)+1] + '\n' + '\n'.join(body) + '\n    ' + source[offset(tokens[closing].position):]

    def _keep(self, node: Any, sliced: bool) -> bool:
        if not sliced or self.keep_ids is None:
            return True
        node_id = self.node_ids.get(id(node))
        return node_id is not None and node_id in self.keep_ids

    def _statement(self, node: Any, indent: int, sliced: bool) -> list[str]:
        if node is None:
            return []
        if isinstance(node, javalang.tree.BlockStatement):
            lines = [self._i(indent) + "{"]
            for child in node.statements:
                lines.extend(self._statement(child, indent + 1, sliced))
                if sliced and self._guaranteed_terminates(child):
                    break
            lines.append(self._i(indent) + "}")
            return lines
        if isinstance(node, javalang.tree.IfStatement):
            decision = self.pruned_branches.get(id(node)) if sliced else None
            if decision is not None:
                selected = node.then_statement if decision else node.else_statement
                if selected is None:
                    return []
                if not isinstance(selected, javalang.tree.BlockStatement):
                    return self._statement(selected, indent, sliced)
                scoped = any(isinstance(child, (javalang.tree.LocalVariableDeclaration, javalang.tree.ClassDeclaration)) for child in selected.statements)
                lines = [self._i(indent) + '{'] if scoped else []
                for child in selected.statements:
                    lines.extend(self._statement(child, indent + int(scoped), sliced))
                    if self._guaranteed_terminates(child): break
                return lines + ([self._i(indent) + '}'] if scoped else [])
            if not self._keep(node, sliced):
                return []
            lines = [self._i(indent) + f"if ({expression_source(node.condition)}) {{"]
            lines.extend(self._body(node.then_statement, indent + 1, sliced))
            lines.append(self._i(indent) + "}")
            if node.else_statement is not None:
                lines[-1] += " else {"
                lines.extend(self._body(node.else_statement, indent + 1, sliced))
                lines.append(self._i(indent) + "}")
            return lines
        if isinstance(node, javalang.tree.WhileStatement):
            if not self._keep(node, sliced):
                return []
            lines = [self._i(indent) + f"while ({expression_source(node.condition)}) {{"]
            lines.extend(self._body(node.body, indent + 1, sliced))
            lines.append(self._i(indent) + "}")
            return lines
        if isinstance(node, javalang.tree.DoStatement):
            if not self._keep(node, sliced):
                return []
            lines = [self._i(indent) + "do {"]
            lines.extend(self._body(node.body, indent + 1, sliced))
            lines.append(self._i(indent) + f"}} while ({expression_source(node.condition)});")
            return lines
        if isinstance(node, javalang.tree.ForStatement):
            if not self._keep(node, sliced):
                return []
            control = for_control_source(node.control)
            lines = [self._i(indent) + f"for ({control}) {{"]
            lines.extend(self._body(node.body, indent + 1, sliced))
            lines.append(self._i(indent) + "}")
            return lines
        if isinstance(node, javalang.tree.SwitchStatement):
            if not self._keep(node, sliced):
                return []
            lines = [self._i(indent) + f"switch ({expression_source(node.expression)}) {{"]
            for case in node.cases:
                label = "default" if not case.case else "case " + ", ".join(expression_source(item) for item in case.case)
                lines.append(self._i(indent + 1) + label + ":")
                for child in case.statements:
                    lines.extend(self._statement(child, indent + 2, sliced))
            lines.append(self._i(indent) + "}")
            return lines
        if not self._keep(node, sliced):
            return []
        pad = self._i(indent)
        if isinstance(node, javalang.tree.LocalVariableDeclaration):
            items = []
            for decl in node.declarators:
                item = decl.name
                if decl.initializer is not None:
                    item += " = " + expression_source(decl.initializer)
                items.append(item)
            return [pad + f"{_mods(node.modifiers)}{type_to_string(node.type)} {', '.join(items)};"]
        if isinstance(node, javalang.tree.StatementExpression):
            return [pad + expression_source(node.expression) + ";"]
        if isinstance(node, javalang.tree.ReturnStatement):
            return [pad + "return" + (" " + expression_source(node.expression) if node.expression is not None else "") + ";"]
        if isinstance(node, javalang.tree.BreakStatement):
            return [pad + "break" + (" " + node.goto if node.goto else "") + ";"]
        if isinstance(node, javalang.tree.ContinueStatement):
            return [pad + "continue" + (" " + node.goto if node.goto else "") + ";"]
        if isinstance(node, javalang.tree.ThrowStatement):
            return [pad + "throw " + expression_source(node.expression) + ";"]
        if type(node) is javalang.tree.Statement:
            return [pad + ";"]
        raise UnsupportedJavaError(f"Cannot emit statement node {type(node).__name__}")

    def _body(self, node: Any, indent: int, sliced: bool) -> list[str]:
        if isinstance(node, javalang.tree.BlockStatement):
            lines: list[str] = []
            for child in node.statements:
                lines.extend(self._statement(child, indent, sliced))
                if sliced and self._guaranteed_terminates(child):
                    break
            return lines
        return self._statement(node, indent, sliced)

    def _guaranteed_terminates(self, node: Any) -> bool:
        if isinstance(node, (javalang.tree.ReturnStatement, javalang.tree.ThrowStatement)):
            return self._keep(node, True)
        if isinstance(node, javalang.tree.BlockStatement):
            return any(self._guaranteed_terminates(child) for child in node.statements)
        if isinstance(node, javalang.tree.IfStatement):
            decision = self.pruned_branches.get(id(node))
            if decision is not None:
                return self._guaranteed_terminates(node.then_statement if decision else node.else_statement)
            return node.else_statement is not None and self._guaranteed_terminates(node.then_statement) and self._guaranteed_terminates(node.else_statement)
        return False

    @staticmethod
    def _i(level: int) -> str:
        return "    " * level


def variable_declaration_source(node: Any) -> str:
    items = []
    for decl in node.declarators:
        item = decl.name
        if decl.initializer is not None:
            item += " = " + expression_source(decl.initializer)
        items.append(item)
    return f"{type_to_string(node.type)} {', '.join(items)}"


def for_control_source(control: Any) -> str:
    if isinstance(control, javalang.tree.EnhancedForControl):
        return f"{variable_declaration_source(control.var)} : {expression_source(control.iterable)}"
    init = [control.init] if isinstance(control.init, javalang.tree.VariableDeclaration) else (control.init or [])
    init_text = []
    for item in init:
        init_text.append(variable_declaration_source(item) if isinstance(item, javalang.tree.VariableDeclaration) else expression_source(item))
    condition = expression_source(control.condition) if control.condition else ""
    update = ", ".join(expression_source(item) for item in (control.update or []))
    return f"{', '.join(init_text)}; {condition}; {update}"
