from __future__ import annotations

import ast
import math
import re
from dataclasses import dataclass
from typing import Any, Mapping

import javalang
import z3

from .errors import ExpressionError, UnsupportedJavaError
from .models import AnalysisConfig, VariableSpec


INTEGER_TYPES = {"byte", "short", "int", "long", "char"}
REAL_TYPES = {"float", "double"}
BOOLEAN_TYPES = {"bool", "boolean"}


def normalize_type(type_name: str) -> str:
    value = type_name.replace("java.lang.", "").strip()
    return "boolean" if value == "bool" else value


def make_symbol(name: str, type_name: str) -> z3.ExprRef:
    kind = normalize_type(type_name)
    if kind == "boolean":
        return z3.Bool(name)
    if kind == "long":
        return z3.BitVec(name, 64)
    if kind in {"byte", "short", "int", "char"}:
        return z3.BitVec(name, 32)
    if kind in REAL_TYPES:
        return z3.Real(name)
    raise ExpressionError(f"Unsupported variable type: {type_name}")


def domain_constraint(symbols: Mapping[str, z3.ExprRef], specs: Mapping[str, VariableSpec], config: AnalysisConfig) -> z3.BoolRef:
    constraints: list[z3.BoolRef] = []
    for name, symbol in symbols.items():
        spec = specs[name]
        kind = normalize_type(spec.type)
        if kind == "boolean":
            continue
        low = spec.minimum
        high = spec.maximum
        if kind == "char":
            low = 0 if low is None else low
            high = 65535 if high is None else high
        elif kind == "byte":
            low = -128 if low is None else low
            high = 127 if high is None else high
        elif kind == "short":
            low = -32768 if low is None else low
            high = 32767 if high is None else high
        else:
            low = config.default_int_min if low is None else low
            high = config.default_int_max if high is None else high
        constraints.extend([symbol >= low, symbol <= high])
    return z3.And(*constraints) if constraints else z3.BoolVal(True)


def parse_expression(text: str) -> Any:
    normalized = (
        text.replace("∧", "&&")
        .replace("∨", "||")
        .replace("¬", "!")
        .replace("≤", "<=")
        .replace("≥", ">=")
        .replace("≠", "!=")
    )
    normalized = re.sub(r"\btrue\b", "true", normalized, flags=re.I)
    normalized = re.sub(r"\bfalse\b", "false", normalized, flags=re.I)
    try:
        return javalang.parse.parse_expression(normalized)
    except Exception as exc:
        raise ExpressionError(f"Invalid Java-style expression '{text}': {exc}") from exc


def expression_variables(text_or_node: str | Any) -> set[str]:
    node = parse_expression(text_or_node) if isinstance(text_or_node, str) else text_or_node
    names: set[str] = set()
    for _, child in node:
        if isinstance(child, javalang.tree.MemberReference):
            if child.qualifier in {"Integer", "Long", "Short", "Byte", "Character", "Math"}:
                continue
            if child.qualifier:
                names.add(child.qualifier.split(".")[0])
            else:
                names.add(child.member)
    if isinstance(node, javalang.tree.MemberReference):
        names.add(node.member)
    return names


def _literal(value: str) -> Any:
    raw = value.replace("_", "")
    if raw == "true":
        return True
    if raw == "false":
        return False
    if raw == "null":
        return None
    if raw.startswith(("'", '"')):
        try:
            parsed = ast.literal_eval(raw)
            return ord(parsed) if isinstance(parsed, str) and raw.startswith("'") else parsed
        except Exception as exc:
            raise ExpressionError(f"Invalid literal {value}") from exc
    suffix = raw[-1:] if raw else ""
    if suffix in "lL":
        raw = raw[:-1]
    elif suffix in "fFdD":
        raw = raw[:-1]
        return float(raw)
    try:
        if raw.lower().startswith("0x"):
            return int(raw, 16)
        if raw.lower().startswith("0b"):
            return int(raw, 2)
        if any(ch in raw for ch in ".eE"):
            return float(raw)
        if len(raw) > 1 and raw.startswith("0"):
            return int(raw, 8)
        return int(raw)
    except ValueError as exc:
        raise ExpressionError(f"Unsupported literal {value}") from exc


def _constant(qualifier: str, member: str) -> int | float:
    table = {
        ("Integer", "MAX_VALUE"): 2**31 - 1,
        ("Integer", "MIN_VALUE"): -(2**31),
        ("Long", "MAX_VALUE"): 2**63 - 1,
        ("Long", "MIN_VALUE"): -(2**63),
        ("Short", "MAX_VALUE"): 32767,
        ("Short", "MIN_VALUE"): -32768,
        ("Byte", "MAX_VALUE"): 127,
        ("Byte", "MIN_VALUE"): -128,
        ("Character", "MAX_VALUE"): 65535,
        ("Character", "MIN_VALUE"): 0,
    }
    if (qualifier, member) not in table:
        raise UnsupportedJavaError(f"Unsupported constant {qualifier}.{member}")
    return table[(qualifier, member)]


def _is_symbolic(value: Any) -> bool:
    return isinstance(value, z3.AstRef)


def _java_div(left: Any, right: Any) -> Any:
    if _is_symbolic(left) or _is_symbolic(right):
        if isinstance(left, z3.ArithRef) and not z3.is_bv(left):
            return left / right
        return left / right
    if right == 0:
        raise ZeroDivisionError("Java integer division by zero")
    if isinstance(left, float) or isinstance(right, float):
        return left / right
    return math.trunc(left / right)


def _java_mod(left: Any, right: Any) -> Any:
    if _is_symbolic(left) or _is_symbolic(right):
        if z3.is_bv(left) or z3.is_bv(right):
            return z3.SRem(left, right)
        return z3.Mod(left, right)
    return left - _java_div(left, right) * right


def _apply_binary(operator: str, left: Any, right: Any) -> Any:
    if operator == "&&":
        return z3.And(left, right) if _is_symbolic(left) or _is_symbolic(right) else bool(left and right)
    if operator == "||":
        return z3.Or(left, right) if _is_symbolic(left) or _is_symbolic(right) else bool(left or right)
    if operator == "==":
        return left == right
    if operator == "!=":
        return left != right
    if operator == "<":
        return left < right
    if operator == "<=":
        return left <= right
    if operator == ">":
        return left > right
    if operator == ">=":
        return left >= right
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        return _java_div(left, right)
    if operator == "%":
        return _java_mod(left, right)
    if operator == "&":
        return left & right
    if operator == "|":
        return left | right
    if operator == "^":
        return left ^ right
    if operator == "<<":
        return left << right
    if operator == ">>":
        return left >> right
    if operator == ">>>":
        if _is_symbolic(left):
            return z3.LShR(left, right)
        width = 64 if abs(int(left)) > 2**31 - 1 else 32
        return (left % (1 << width)) >> right
    raise UnsupportedJavaError(f"Unsupported binary operator: {operator}")


def _apply_prefix(operators: list[str] | None, value: Any) -> Any:
    for operator in reversed(operators or []):
        if operator == "!":
            value = z3.Not(value) if _is_symbolic(value) else not value
        elif operator == "-":
            value = -value
        elif operator == "+":
            value = value
        elif operator == "~":
            value = ~value
        elif operator in {"++", "--"}:
            value = value + (1 if operator == "++" else -1)
        else:
            raise UnsupportedJavaError(f"Unsupported prefix operator: {operator}")
    return value


@dataclass(slots=True)
class ExpressionEngine:
    types: Mapping[str, str]

    def evaluate_text(self, text: str, env: Mapping[str, Any]) -> Any:
        return self.evaluate(parse_expression(text), env)

    def evaluate(self, node: Any, env: Mapping[str, Any]) -> Any:
        if node is None:
            return None
        if isinstance(node, (bool, int, float, z3.AstRef)):
            return node
        if isinstance(node, javalang.tree.Literal):
            return _apply_prefix(node.prefix_operators, _literal(node.value))
        if isinstance(node, javalang.tree.MemberReference):
            if node.qualifier in {"Integer", "Long", "Short", "Byte", "Character"}:
                value = _constant(node.qualifier, node.member)
            else:
                name = node.member if not node.qualifier else f"{node.qualifier}.{node.member}"
                if name not in env and node.qualifier in env:
                    value = env[node.qualifier]
                elif name in env:
                    value = env[name]
                elif node.member in env:
                    value = env[node.member]
                else:
                    raise ExpressionError(f"Unknown variable '{name}'.")
            value = self._selectors(value, node.selectors or [], env)
            return _apply_prefix(node.prefix_operators, value)
        if isinstance(node, javalang.tree.BinaryOperation):
            left = self.evaluate(node.operandl, env)
            right = self.evaluate(node.operandr, env)
            return _apply_binary(node.operator, left, right)
        if isinstance(node, javalang.tree.TernaryExpression):
            condition = self.evaluate(node.condition, env)
            yes = self.evaluate(node.if_true, env)
            no = self.evaluate(node.if_false, env)
            value = z3.If(condition, yes, no) if _is_symbolic(condition) else (yes if condition else no)
            return value
        if isinstance(node, javalang.tree.Cast):
            value = self.evaluate(node.expression, env)
            kind = type_to_string(node.type)
            return self._cast(kind, value)
        if isinstance(node, javalang.tree.MethodInvocation):
            args = [self.evaluate(arg, env) for arg in node.arguments]
            value = self._method(node.qualifier or "", node.member, args)
            value = self._selectors(value, node.selectors or [], env)
            return _apply_prefix(node.prefix_operators, value)
        if isinstance(node, javalang.tree.SuperMethodInvocation):
            raise UnsupportedJavaError("super method calls are not supported")
        if isinstance(node, javalang.tree.Assignment):
            left = self.evaluate(node.expressionl, env)
            right = self.evaluate(node.value, env)
            return right if node.type == "=" else _apply_binary(node.type[:-1], left, right)
        if isinstance(node, javalang.tree.ClassCreator):
            raise UnsupportedJavaError("Object construction is outside the scalar Java subset")
        raise UnsupportedJavaError(f"Unsupported expression node: {type(node).__name__}")

    def _selectors(self, value: Any, selectors: list[Any], env: Mapping[str, Any]) -> Any:
        for selector in selectors:
            if isinstance(selector, javalang.tree.ArraySelector):
                index = self.evaluate(selector.index, env)
                if _is_symbolic(index):
                    value = z3.Select(value, index)
                else:
                    value = value[index]
            elif isinstance(selector, javalang.tree.MethodInvocation):
                args = [self.evaluate(arg, env) for arg in selector.arguments]
                value = self._method("", selector.member, [value, *args])
            else:
                raise UnsupportedJavaError(f"Unsupported selector: {type(selector).__name__}")
        return value

    def _method(self, qualifier: str, name: str, args: list[Any]) -> Any:
        full = f"{qualifier}.{name}" if qualifier else name
        if full in {"Math.abs", "StrictMath.abs", "abs"}:
            value = args[0]
            return z3.If(value >= 0, value, -value) if _is_symbolic(value) else abs(value)
        if full in {"Math.min", "StrictMath.min", "min"}:
            return z3.If(args[0] <= args[1], args[0], args[1]) if any(map(_is_symbolic, args)) else min(args)
        if full in {"Math.max", "StrictMath.max", "max"}:
            return z3.If(args[0] >= args[1], args[0], args[1]) if any(map(_is_symbolic, args)) else max(args)
        if full in {"Math.pow", "StrictMath.pow", "pow"} and len(args) == 2:
            if isinstance(args[1], int):
                return args[0] ** args[1]
            if _is_symbolic(args[1]):
                raise UnsupportedJavaError("Symbolic non-integer exponents are unsupported")
            return args[0] ** args[1]
        if name == "equals" and len(args) == 2:
            return args[0] == args[1]
        raise UnsupportedJavaError(f"Unsupported method invocation: {full}")

    def _cast(self, kind: str, value: Any) -> Any:
        kind = normalize_type(kind)
        if kind in INTEGER_TYPES:
            width = 64 if kind == "long" else 32
            if z3.is_bv(value):
                current = value.size()
                if current == width:
                    return value
                return z3.SignExt(width - current, value) if current < width else z3.Extract(width - 1, 0, value)
            if isinstance(value, z3.ArithRef):
                integer = z3.If(value >= 0, z3.ToInt(value), -z3.ToInt(-value))
                return z3.Int2BV(integer, width)
            return int(value)
        if kind in REAL_TYPES:
            if z3.is_bv(value):
                return z3.ToReal(z3.BV2Int(value, is_signed=True))
            return float(value) if not _is_symbolic(value) else value
        if kind == "boolean":
            return value
        raise UnsupportedJavaError(f"Unsupported cast to {kind}")


def type_to_string(node: Any) -> str:
    if node is None:
        return "void"
    name = getattr(node, "name", str(node))
    dimensions = getattr(node, "dimensions", None) or []
    return str(name) + "[]" * len(dimensions)


def model_value(model: z3.ModelRef, symbol: z3.ExprRef, type_name: str) -> Any:
    value = model.eval(symbol, model_completion=True)
    kind = normalize_type(type_name)
    if kind == "boolean":
        return z3.is_true(value)
    if z3.is_bv(value):
        unsigned = value.as_long()
        bits = value.size()
        signed = unsigned - (1 << bits) if unsigned >= (1 << (bits - 1)) else unsigned
        return unsigned if kind == "char" else signed
    if isinstance(value, z3.RatNumRef):
        return value.numerator_as_long() / value.denominator_as_long()
    if isinstance(value, z3.IntNumRef):
        return value.as_long()
    return str(value)


def model_as_dict(model: z3.ModelRef, symbols: Mapping[str, z3.ExprRef], specs: Mapping[str, VariableSpec]) -> dict[str, Any]:
    return {name: model_value(model, symbol, specs[name].type) for name, symbol in symbols.items()}


def z3_text(expr: Any) -> str:
    try:
        return str(z3.simplify(expr))
    except Exception:
        return str(expr)


def collect_uses(node: Any) -> set[str]:
    if node is None:
        return set()
    names: set[str] = set()
    iterator = node if hasattr(node, "__iter__") else []
    for _, child in iterator:
        if isinstance(child, javalang.tree.MemberReference):
            if child.qualifier not in {"Integer", "Long", "Short", "Byte", "Character", "Math"}:
                names.add(child.member if not child.qualifier else child.qualifier.split(".")[0])
    if isinstance(node, javalang.tree.MemberReference):
        names.add(node.member)
    return names
