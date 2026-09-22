"""Typed Java scalar expressions shared by FSF, symbolic execution and pruning."""
from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Mapping, Callable

import javalang
import z3

from .errors import ExpressionError, UnsupportedJavaError
from .models import AnalysisConfig, VariableSpec, TYPE_LIMITS
from .java_parser import JavaParser

INTEGER_TYPES = set(TYPE_LIMITS)
REAL_TYPES = {"float", "double"}
BOOLEAN_TYPES = {"bool", "boolean"}
CONSTANT_CLASSES = {"Integer", "Long", "Short", "Byte", "Character"}


def normalize_type(type_name):
    kind = type_name.replace("java.lang.", "").strip()
    return "boolean" if kind == "bool" else kind


def make_symbol(name, type_name):
    kind = normalize_type(type_name)
    if kind == "boolean":
        return z3.Bool(name)
    if kind in INTEGER_TYPES:
        return z3.BitVec(name, 64 if kind == "long" else 32)
    if kind in REAL_TYPES:
        raise UnsupportedJavaError("IEEE-754 floating-point verification is not supported.")
    raise ExpressionError(f"Unsupported variable type: {type_name}")


def effective_bounds(spec, config):
    kind = normalize_type(spec.type)
    if kind == "boolean":
        return None, None
    defaults = TYPE_LIMITS[kind] if kind in {"byte", "short", "char"} else (config.default_int_min, config.default_int_max)
    return (defaults[0] if spec.minimum is None else spec.minimum,
            defaults[1] if spec.maximum is None else spec.maximum)


def domain_constraint(symbols, specs, config):
    terms = []
    for name, symbol in symbols.items():
        low, high = effective_bounds(specs[name], config)
        if low is not None:
            terms.extend([symbol >= low, symbol <= high])
    return z3.And(*terms)


def output_constraint(symbols, specs):
    terms = []
    for name, symbol in symbols.items():
        spec = specs[name]
        limits = TYPE_LIMITS.get(normalize_type(spec.type))
        if limits:
            lo = limits[0] if spec.minimum is None else spec.minimum
            hi = limits[1] if spec.maximum is None else spec.maximum
            terms.extend([symbol >= lo, symbol <= hi])
    return z3.And(*terms)


@lru_cache(maxsize=1024)
def parse_expression(text):
    parts = re.split(r'''('(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")''', text)
    for i in range(0, len(parts), 2):
        for a, b in {"∧": "&&", "∨": "||", "¬": "!", "≤": "<=", "≥": ">=", "≠": "!="}.items():
            parts[i] = parts[i].replace(a, b)
    normalized = ''.join(parts)
    try:
        parser = JavaParser(javalang.tokenizer.tokenize(normalized + ' ;'))
        node = parser.parse_expression()
        parser.accept(';')
        if not isinstance(parser.tokens.look(), javalang.tokenizer.EndOfInput):
            raise ValueError("trailing tokens")
        return node
    except Exception as exc:
        raise ExpressionError(f"Invalid Java-style expression '{text}': {exc}") from exc


def collect_uses(node):
    if node is None:
        return set()
    return {n.member if not n.qualifier else n.qualifier.split('.')[0]
            for _, n in node if isinstance(n, javalang.tree.MemberReference)
            and n.qualifier not in CONSTANT_CLASSES}


def expression_variables(text_or_node):
    return collect_uses(parse_expression(text_or_node) if isinstance(text_or_node, str) else text_or_node)


def _literal(value):
    raw = value.replace('_', '')
    if raw in {'true', 'false'}:
        return raw == 'true'
    if raw.startswith("'"):
        try:
            val = ast.literal_eval(raw)
            if len(val) != 1 or ord(val) > 65535:
                raise ValueError()
            return ord(val)
        except Exception as exc:
            raise ExpressionError(f"Invalid Java character: {value}") from exc
    if raw.startswith('"') or raw == 'null':
        raise UnsupportedJavaError("String and reference values are not scalar integers.")
    if _literal_type(raw) in REAL_TYPES:
        raise UnsupportedJavaError("IEEE-754 floating-point expressions are not supported.")
    raw = raw.rstrip('lL')
    try:
        return int(raw, 16 if raw.lower().startswith('0x') else 2 if raw.lower().startswith('0b') else 8 if len(raw) > 1 and raw.startswith('0') else 10)
    except ValueError as exc:
        raise ExpressionError(f"Invalid integer literal: {value}") from exc


def _literal_type(raw):
    raw = raw.replace('_', '')
    if raw in {'true', 'false'}:
        return 'boolean'
    if raw.startswith("'"):
        return 'char'
    if raw.startswith('"') or raw == 'null':
        return 'reference'
    if raw[-1:] in {'l', 'L'}:
        return 'long'
    if raw.lower().startswith(('0x', '0b')) and '.' not in raw and 'p' not in raw.lower():
        return 'int'
    if '.' in raw or 'e' in raw.lower() or raw[-1:] in {'d', 'D', 'f', 'F'}:
        return 'double'
    return 'int'


def _constant(qualifier, member):
    kinds = {'Integer': 'int', 'Long': 'long', 'Short': 'short', 'Byte': 'byte', 'Character': 'char'}
    if qualifier not in kinds or member not in {'MIN_VALUE', 'MAX_VALUE'}:
        raise UnsupportedJavaError(f"Unsupported constant {qualifier}.{member}")
    return TYPE_LIMITS[kinds[qualifier]][member == 'MAX_VALUE']


def cast_value(kind, value):
    kind = normalize_type(kind)
    if kind == 'boolean':
        if not isinstance(value, bool) and not z3.is_bool(value):
            raise ExpressionError("Expected Boolean value.")
        return value
    if kind not in INTEGER_TYPES:
        raise UnsupportedJavaError(f"Unsupported scalar type: {kind}")
    if isinstance(value, bool) or z3.is_bool(value):
        raise ExpressionError("Boolean cannot be converted to an integer.")
    width = {'byte': 8, 'short': 16, 'char': 16, 'int': 32, 'long': 64}[kind]
    if z3.is_bv(value):
        size = value.size()
        value = z3.Extract(width - 1, 0, value) if size > width else z3.SignExt(width - size, value) if size < width else value
        if width < 32:
            value = z3.ZeroExt(32 - width, value) if kind == 'char' else z3.SignExt(32 - width, value)
        return value
    if type(value) is not int:
        raise UnsupportedJavaError("Only integral values have a Java integer encoding.")
    value %= 1 << width
    return value - (1 << width) if kind != 'char' and value >= (1 << (width - 1)) else value


def _java_div(left, right):
    if z3.is_bv(left) or z3.is_bv(right):
        return left / right
    if right == 0:
        raise ZeroDivisionError("integer division by zero")
    result = abs(left) // abs(right)
    return -result if (left < 0) != (right < 0) else result


def _java_mod(left, right):
    if z3.is_bv(left) or z3.is_bv(right):
        return z3.SRem(left, right)
    return left - _java_div(left, right) * right


def _apply_binary(operator, left, right):
    if operator == '&&': return z3.And(left, right) if z3.is_bool(left) or z3.is_bool(right) else left and right
    if operator == '||': return z3.Or(left, right) if z3.is_bool(left) or z3.is_bool(right) else left or right
    if operator == '==': return left == right
    if operator == '!=': return left != right
    if operator == '<': return left < right
    if operator == '<=': return left <= right
    if operator == '>': return left > right
    if operator == '>=': return left >= right
    if operator == '+': return left + right
    if operator == '-': return left - right
    if operator == '*': return left * right
    if operator == '/': return _java_div(left, right)
    if operator == '%': return _java_mod(left, right)
    if operator == '&': return z3.And(left, right) if z3.is_bool(left) else left & right
    if operator == '|': return z3.Or(left, right) if z3.is_bool(left) else left | right
    if operator == '^': return z3.Xor(left, right) if z3.is_bool(left) else left ^ right
    if operator == '<<': return left << right
    if operator == '>>': return left >> right
    if operator == '>>>': return z3.LShR(left, right)
    raise UnsupportedJavaError(f"Unsupported operator: {operator}")


@dataclass
class ExpressionEngine:
    types: Mapping[str, str]
    choose: Callable[[Any], bool] | None = None
    guards: list[Any] = field(default_factory=list)
    context: Any = True

    def evaluate_text(self, text, env):
        return self.evaluate(parse_expression(text), env)

    def kind(self, node):
        if isinstance(node, javalang.tree.Literal):
            return _literal_type(node.value)
        if isinstance(node, javalang.tree.MemberReference):
            if node.qualifier in CONSTANT_CLASSES:
                return 'long' if node.qualifier == 'Long' else 'int'
            return normalize_type(self.types.get(node.member, 'int'))
        if isinstance(node, javalang.tree.Cast):
            return type_to_string(node.type)
        if isinstance(node, javalang.tree.BinaryOperation):
            if node.operator in {'==', '!=', '<', '>', '<=', '>=', '&&', '||'}:
                return 'boolean'
            left, right = self.kind(node.operandl), self.kind(node.operandr)
            if node.operator in {'<<', '>>', '>>>'}:
                return 'long' if left == 'long' else 'int'
            return self.promoted(left, right)
        if isinstance(node, javalang.tree.TernaryExpression):
            yes, no = self.kind(node.if_true), self.kind(node.if_false)
            if yes == no:
                return yes
            # Java's constant/narrowing conditional conversion requires full typing.
            if yes in {'byte', 'short', 'char'} or no in {'byte', 'short', 'char'}:
                raise UnsupportedJavaError('Mixed narrow-type conditional expressions require Java type resolution.')
            return self.promoted(yes, no)
        if isinstance(node, javalang.tree.MethodInvocation) and node.arguments:
            kind = self.kind(node.arguments[0])
            for arg in node.arguments[1:]:
                kind = self.promoted(kind, self.kind(arg))
            return 'long' if kind == 'long' else 'int'
        raise UnsupportedJavaError(f"Cannot type expression: {type(node).__name__}")

    @staticmethod
    def promoted(left, right):
        if left == right == 'boolean': return 'boolean'
        if 'boolean' in {left, right}: raise ExpressionError('Mixed Boolean/numeric operands.')
        if {left, right} & REAL_TYPES: raise UnsupportedJavaError('IEEE-754 arithmetic is not supported.')
        return 'long' if 'long' in {left, right} else 'int'

    def _under(self, guard, node, env):
        previous = self.context
        self.context = z3.And(previous, guard)
        try:
            return self.evaluate(node, env)
        finally:
            self.context = previous

    def evaluate(self, node, env):
        value = self._evaluate(node, env)
        if node is None or isinstance(node, (bool, int, z3.AstRef)):
            return value
        kind = self.kind(node)
        for op in reversed(getattr(node, 'prefix_operators', None) or []):
            if op == '!':
                value = cast_value('boolean', value)
                value = z3.Not(value) if z3.is_bool(value) else not value
            elif op in {'-', '+', '~'}:
                if kind == 'boolean':
                    raise ExpressionError('Numeric unary operators cannot be applied to Boolean values.')
                kind = 'long' if kind == 'long' else 'int'
                value = cast_value(kind, -value if op == '-' else ~value if op == '~' else value)
            else:
                raise UnsupportedJavaError(f'Unsupported unary operator: {op}')
        return value

    def _evaluate(self, node, env):
        if node is None: return None
        if isinstance(node, (bool, int, z3.AstRef)): return node
        operators = (getattr(node, 'prefix_operators', None) or []) + (getattr(node, 'postfix_operators', None) or [])
        if any(op in {'++', '--'} for op in operators):
            raise UnsupportedJavaError('Embedded increment/decrement is not supported; use a separate statement.')
        if getattr(node, 'selectors', None):
            raise UnsupportedJavaError('Array/object selectors are not supported.')
        if isinstance(node, javalang.tree.Literal):
            value = cast_value(self.kind(node), _literal(node.value))
        elif isinstance(node, javalang.tree.MemberReference):
            if node.qualifier in CONSTANT_CLASSES:
                value = _constant(node.qualifier, node.member)
            elif node.qualifier:
                raise UnsupportedJavaError(f'Field access {node.qualifier}.{node.member} requires a heap model.')
            elif node.member in env:
                value = cast_value(self.kind(node), env[node.member])
            else:
                raise ExpressionError(f"Unknown or uninitialized variable '{node.member}'.")
        elif isinstance(node, javalang.tree.BinaryOperation):
            left = self.evaluate(node.operandl, env)
            op = node.operator
            if op in {'&&', '||'}:
                cast_value('boolean', left)
                if isinstance(left, bool) or self.choose is not None:
                    decision = left if isinstance(left, bool) else self.choose(left)
                    if op == '&&' and not decision: return False
                    if op == '||' and decision: return True
                    return cast_value('boolean', self.evaluate(node.operandr, env))
                right = self._under(left if op == '&&' else z3.Not(left), node.operandr, env)
                return _apply_binary(op, left, cast_value('boolean', right))
            right = self.evaluate(node.operandr, env)
            if op in {'<<', '>>', '>>>'}:
                kind = self.kind(node)
                left, right = cast_value(kind, left), cast_value(kind, right)
                width = 64 if kind == 'long' else 32
                right = right & (width - 1)
                if op == '>>>' and not z3.is_bv(left) and not z3.is_bv(right):
                    return cast_value(kind, (left % (1 << width)) >> right)
            else:
                kind = self.promoted(self.kind(node.operandl), self.kind(node.operandr))
                if kind == 'boolean' and op not in {'==', '!=', '&', '|', '^'}:
                    raise ExpressionError('Boolean operands do not support numeric operators.')
                left, right = cast_value(kind, left), cast_value(kind, right)
            if op in {'/', '%'}:
                safe = right != 0
                self.guards.append(z3.Implies(self.context, safe))
                if self.choose is not None and not self.choose(safe):
                    raise ZeroDivisionError('integer division by zero')
            # Coerce numeric constants before overloaded Z3 operations.
            if z3.is_bv(left) and not z3.is_bv(right): right = z3.BitVecVal(right, left.size())
            if z3.is_bv(right) and not z3.is_bv(left): left = z3.BitVecVal(left, right.size())
            value = _apply_binary(op, left, right)
            return value if op in {'==', '!=', '<', '>', '<=', '>='} else cast_value(kind, value)
        elif isinstance(node, javalang.tree.TernaryExpression):
            condition = cast_value('boolean', self.evaluate(node.condition, env))
            kind = self.kind(node)
            if isinstance(condition, bool) or self.choose is not None:
                decision = condition if isinstance(condition, bool) else self.choose(condition)
                return cast_value(kind, self.evaluate(node.if_true if decision else node.if_false, env))
            yes = cast_value(kind, self._under(condition, node.if_true, env))
            no = cast_value(kind, self._under(z3.Not(condition), node.if_false, env))
            if kind in INTEGER_TYPES:
                width = 64 if kind == 'long' else 32
                yes = z3.BitVecVal(yes, width) if isinstance(yes, int) else yes
                no = z3.BitVecVal(no, width) if isinstance(no, int) else no
            return z3.If(condition, yes, no)
        elif isinstance(node, javalang.tree.Cast):
            return cast_value(type_to_string(node.type), self.evaluate(node.expression, env))
        elif isinstance(node, javalang.tree.MethodInvocation):
            full = f'{node.qualifier}.{node.member}'
            if full not in {'Math.abs', 'Math.min', 'Math.max', 'StrictMath.abs', 'StrictMath.min', 'StrictMath.max'}:
                raise UnsupportedJavaError(f'Unsupported method invocation: {full}')
            if len(node.arguments) != (1 if node.member == 'abs' else 2):
                raise ExpressionError(f'Wrong arity: {full}')
            kind = self.kind(node)
            args = [cast_value(kind, self.evaluate(arg, env)) for arg in node.arguments]
            if node.member == 'abs':
                v = args[0]
                value = z3.If(v >= 0, v, -v) if z3.is_bv(v) else abs(v)
            else:
                a, b = args
                condition = a <= b if node.member == 'min' else a >= b
                value = z3.If(condition, a, b) if z3.is_bool(condition) else a if condition else b
            value = cast_value(kind, value)
        else:
            raise UnsupportedJavaError(f'Unsupported expression: {type(node).__name__}')
        return value

    def _cast(self, kind, value):
        return cast_value(kind, value)


def type_to_string(node):
    if node is None: return 'void'
    return str(getattr(node, 'name', str(node))) + '[]' * len(getattr(node, 'dimensions', None) or [])


def model_value(model, symbol, type_name):
    value = model.eval(symbol, model_completion=True)
    if z3.is_bool(value): return z3.is_true(value)
    if z3.is_bv(value):
        raw = value.as_long()
        return raw - (1 << value.size()) if normalize_type(type_name) != 'char' and raw >= (1 << (value.size() - 1)) else raw
    return str(value)


def model_as_dict(model, symbols, specs):
    return {name: model_value(model, symbol, specs[name].type) for name, symbol in symbols.items()}


def z3_text(expr):
    return str(z3.simplify(expr)) if isinstance(expr, z3.AstRef) else str(expr)
