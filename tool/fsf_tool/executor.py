from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import javalang
import z3

from .errors import UnsupportedJavaError
from .expression import ExpressionEngine, make_symbol, normalize_type, type_to_string, z3_text
from .java_frontend import JavaProgram, expression_source
from .models import FSFSpec


class _Break(Exception):
    pass


class _Continue(Exception):
    pass


class _Return(Exception):
    pass


class _BoundReached(Exception):
    pass


@dataclass(slots=True)
class ConcolicExecution:
    test_case: dict[str, Any]
    path_conditions: list[Any] = field(default_factory=list)
    trace: list[str] = field(default_factory=list)
    symbolic_env: dict[str, Any] = field(default_factory=dict)
    concrete_env: dict[str, Any] = field(default_factory=dict)
    variable_types: dict[str, str] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    concrete_outputs: dict[str, Any] = field(default_factory=dict)
    loop_iterations: int = 0
    truncated: bool = False
    exception: str | None = None

    @property
    def path_condition(self) -> Any:
        return z3.And(*self.path_conditions) if self.path_conditions else z3.BoolVal(True)


class ConcolicExecutor:
    def __init__(self, program: JavaProgram, spec: FSFSpec, input_symbols: dict[str, Any] | None = None) -> None:
        self.program = program
        self.spec = spec
        self.input_symbols = input_symbols or {name: make_symbol(name, variable.type) for name, variable in spec.inputs.items()}

    def execute(self, test_case: dict[str, Any]) -> ConcolicExecution:
        types = {name: variable.type for name, variable in self.spec.inputs.items()}
        result = ConcolicExecution(
            test_case=dict(test_case),
            symbolic_env=dict(self.input_symbols),
            concrete_env=dict(test_case),
            variable_types=types,
        )
        try:
            self._statements(self.program.method.body or [], result)
        except _Return:
            pass
        except _BoundReached:
            result.truncated = True
        except UnsupportedJavaError as exc:
            result.exception = "unsupported: " + str(exc)
        except Exception as exc:
            result.exception = f"{type(exc).__name__}: {exc}"
        return result

    def _engines(self, state: ConcolicExecution) -> tuple[ExpressionEngine, ExpressionEngine]:
        return ExpressionEngine(state.variable_types), ExpressionEngine(state.variable_types)

    def _evaluate(self, expression: Any, state: ConcolicExecution) -> tuple[Any, Any]:
        symbolic, concrete = self._engines(state)
        return symbolic.evaluate(expression, state.symbolic_env), concrete.evaluate(expression, state.concrete_env)

    def _statements(self, statements: list[Any], state: ConcolicExecution) -> None:
        for statement in statements:
            self._statement(statement, state)

    def _body(self, node: Any, state: ConcolicExecution) -> None:
        if node is None:
            return
        if isinstance(node, javalang.tree.BlockStatement):
            self._statements(node.statements, state)
        else:
            self._statement(node, state)

    def _statement(self, node: Any, state: ConcolicExecution) -> None:
        if isinstance(node, javalang.tree.BlockStatement):
            self._statements(node.statements, state)
            return
        if isinstance(node, javalang.tree.LocalVariableDeclaration):
            kind = type_to_string(node.type)
            for declarator in node.declarators:
                state.variable_types[declarator.name] = kind
                if declarator.initializer is None:
                    sym, con = self._default(kind), self._default(kind)
                else:
                    sym, con = self._evaluate(declarator.initializer, state)
                self._assign(declarator.name, sym, con, state)
                state.trace.append(f"assign {declarator.name} = {expression_source(declarator.initializer) if declarator.initializer else self._default(kind)}")
            return
        if isinstance(node, javalang.tree.StatementExpression):
            self._statement_expression(node.expression, state)
            return
        if isinstance(node, javalang.tree.IfStatement):
            sym, con = self._evaluate(node.condition, state)
            decision = bool(con)
            state.path_conditions.append(sym if decision else z3.Not(sym))
            state.trace.append(f"branch {expression_source(node.condition)} -> {str(decision).lower()}")
            self._body(node.then_statement if decision else node.else_statement, state)
            return
        if isinstance(node, javalang.tree.WhileStatement):
            self._while(node.condition, node.body, state)
            return
        if isinstance(node, javalang.tree.DoStatement):
            while True:
                self._bounded_iteration(state)
                try:
                    self._body(node.body, state)
                except _Continue:
                    pass
                except _Break:
                    break
                sym, con = self._evaluate(node.condition, state)
                decision = bool(con)
                state.path_conditions.append(sym if decision else z3.Not(sym))
                state.trace.append(f"do-while {expression_source(node.condition)} -> {str(decision).lower()}")
                if not decision:
                    break
            return
        if isinstance(node, javalang.tree.ForStatement):
            self._for(node, state)
            return
        if isinstance(node, javalang.tree.ReturnStatement):
            if node.expression is not None:
                sym, con = self._evaluate(node.expression, state)
                state.outputs["return_value"] = sym
                state.concrete_outputs["return_value"] = con
                state.trace.append(f"return {expression_source(node.expression)}")
            for name, spec in self.spec.outputs.items():
                source = spec.source or ("return" if name == "return_value" else name)
                if source != "return" and source in state.symbolic_env:
                    state.outputs[name] = state.symbolic_env[source]
                    state.concrete_outputs[name] = state.concrete_env[source]
            raise _Return
        if isinstance(node, javalang.tree.BreakStatement):
            state.trace.append("break")
            raise _Break
        if isinstance(node, javalang.tree.ContinueStatement):
            state.trace.append("continue")
            raise _Continue
        if isinstance(node, javalang.tree.ThrowStatement):
            state.exception = "throw " + expression_source(node.expression)
            state.trace.append(state.exception)
            raise _Return
        if isinstance(node, javalang.tree.SwitchStatement):
            self._switch(node, state)
            return
        if isinstance(node, javalang.tree.EmptyStatement):
            return
        raise UnsupportedJavaError(f"Unsupported statement in concolic executor: {type(node).__name__}")

    def _statement_expression(self, expression: Any, state: ConcolicExecution) -> None:
        if isinstance(expression, javalang.tree.Assignment):
            if not isinstance(expression.expressionl, javalang.tree.MemberReference):
                raise UnsupportedJavaError("Only scalar variable assignment is supported")
            name = expression.expressionl.member
            rhs_sym, rhs_con = self._evaluate(expression.value, state)
            if expression.type == "=":
                sym, con = rhs_sym, rhs_con
            else:
                current_sym = state.symbolic_env[name]
                current_con = state.concrete_env[name]
                operator = expression.type[:-1]
                from .expression import _apply_binary

                sym = _apply_binary(operator, current_sym, rhs_sym)
                con = _apply_binary(operator, current_con, rhs_con)
            self._assign(name, sym, con, state)
            state.trace.append(f"assign {expression_source(expression)}")
            return
        if isinstance(expression, javalang.tree.MemberReference):
            operators = (expression.prefix_operators or []) + (expression.postfix_operators or [])
            if any(op in {"++", "--"} for op in operators):
                delta = -1 if "--" in operators else 1
                name = expression.member
                self._assign(name, state.symbolic_env[name] + delta, state.concrete_env[name] + delta, state)
                state.trace.append(f"assign {expression_source(expression)}")
                return
        if isinstance(expression, javalang.tree.MethodInvocation):
            # Print/log calls are identity statements in the paper's derivation rules.
            if expression.qualifier in {"System.out", "System.err"} or expression.member in {"print", "println", "printf"}:
                state.trace.append("identity " + expression_source(expression))
                return
        # Evaluate pure expressions so unsupported calls are surfaced.
        self._evaluate(expression, state)
        state.trace.append("identity " + expression_source(expression))

    def _while(self, condition: Any, body: Any, state: ConcolicExecution) -> None:
        while True:
            sym, con = self._evaluate(condition, state)
            decision = bool(con)
            state.path_conditions.append(sym if decision else z3.Not(sym))
            state.trace.append(f"while {expression_source(condition)} -> {str(decision).lower()}")
            if not decision:
                return
            self._bounded_iteration(state)
            try:
                self._body(body, state)
            except _Continue:
                continue
            except _Break:
                return

    def _for(self, node: Any, state: ConcolicExecution) -> None:
        control = node.control
        if isinstance(control, javalang.tree.EnhancedForControl):
            raise UnsupportedJavaError("Enhanced for loops are not supported by the scalar executor")
        initializers = [control.init] if isinstance(control.init, javalang.tree.VariableDeclaration) else (control.init or [])
        for init in initializers:
            if isinstance(init, javalang.tree.VariableDeclaration):
                kind = type_to_string(init.type)
                for declarator in init.declarators:
                    state.variable_types[declarator.name] = kind
                    sym, con = self._evaluate(declarator.initializer, state) if declarator.initializer else (self._default(kind), self._default(kind))
                    self._assign(declarator.name, sym, con, state)
            else:
                self._statement_expression(init, state)
        while True:
            if control.condition is not None:
                sym, con = self._evaluate(control.condition, state)
                decision = bool(con)
                state.path_conditions.append(sym if decision else z3.Not(sym))
                state.trace.append(f"for {expression_source(control.condition)} -> {str(decision).lower()}")
                if not decision:
                    return
            self._bounded_iteration(state)
            try:
                self._body(node.body, state)
            except _Continue:
                pass
            except _Break:
                return
            for update in control.update or []:
                self._statement_expression(update, state)

    def _switch(self, node: Any, state: ConcolicExecution) -> None:
        selector_sym, selector_con = self._evaluate(node.expression, state)
        selected = None
        preceding: list[Any] = []
        default_case = None
        for case in node.cases:
            if not case.case:
                default_case = case
                continue
            for label in case.case:
                label_sym, label_con = self._evaluate(label, state)
                condition = selector_sym == label_sym
                if selector_con == label_con and selected is None:
                    selected = case
                    state.path_conditions.extend(z3.Not(item) for item in preceding)
                    state.path_conditions.append(condition)
                    break
                preceding.append(condition)
            if selected is not None:
                break
        if selected is None:
            selected = default_case
            state.path_conditions.extend(z3.Not(item) for item in preceding)
        state.trace.append(f"switch {expression_source(node.expression)}")
        if selected:
            try:
                self._statements(selected.statements, state)
            except _Break:
                pass

    def _bounded_iteration(self, state: ConcolicExecution) -> None:
        state.loop_iterations += 1
        if state.loop_iterations > self.spec.config.max_loop_iterations:
            state.truncated = True
            raise _BoundReached

    def _assign(self, name: str, symbolic: Any, concrete: Any, state: ConcolicExecution) -> None:
        kind = normalize_type(state.variable_types.get(name, "int"))
        if kind in {"byte", "short", "int", "long", "char"} and isinstance(concrete, int):
            bits = 64 if kind == "long" else 32
            concrete %= 1 << bits
            if kind != "char" and concrete >= 1 << (bits - 1):
                concrete -= 1 << bits
        state.symbolic_env[name] = symbolic
        state.concrete_env[name] = concrete

    @staticmethod
    def _default(kind: str) -> Any:
        kind = normalize_type(kind)
        if kind == "boolean":
            return False
        if kind in {"float", "double"}:
            return 0.0
        return 0
