"""Explicit boundaries for the intraprocedural Java semantic model."""
import javalang
from .expression import INTEGER_TYPES, type_to_string


def support_issues(program):
    issues = []
    method = program.method
    if 'static' not in (method.modifiers or set()):
        issues.append('Instance methods require receiver/heap state.')
    if {'native', 'synchronized', 'abstract'} & (method.modifiers or set()) or method.body is None:
        issues.append('Native, synchronized and abstract methods require an external execution model.')
    cls = program.class_decl
    if cls.fields or cls.extends or cls.implements or any(isinstance(item, list) for item in cls.body):
        issues.append('Class fields, initializers and inheritance require a class-state model.')
    if program.return_type not in INTEGER_TYPES | {'boolean', 'void'}:
        issues.append(f'Unsupported return type: {program.return_type}.')
    declared = dict(program.parameters)
    for _, node in method:
        if isinstance(node, javalang.tree.FormalParameter):
            if node.varargs or type_to_string(node.type) not in INTEGER_TYPES | {'boolean'}:
                issues.append('Parameters must be scalar Java integers or Booleans.')
        if isinstance(node, (javalang.tree.LocalVariableDeclaration, javalang.tree.VariableDeclaration)):
            if type_to_string(node.type) not in INTEGER_TYPES | {'boolean'}:
                issues.append(f'Unsupported local type: {type_to_string(node.type)}.')
            for decl in node.declarators:
                if decl.dimensions:
                    issues.append('Array declarators require a heap model.')
                if decl.name in declared and declared[decl.name] != type_to_string(node.type):
                    issues.append(f'Local names with different types require scope resolution: {decl.name}.')
                declared[decl.name] = type_to_string(node.type)
        if isinstance(node, (javalang.tree.TryStatement, javalang.tree.SynchronizedStatement,
                             javalang.tree.EnhancedForControl, javalang.tree.LambdaExpression,
                             javalang.tree.AssertStatement, javalang.tree.ClassDeclaration)):
            issues.append(f'Unsupported control or state construct: {type(node).__name__}.')
        if getattr(node, 'label', None) or getattr(node, 'goto', None):
            issues.append('Labeled control flow is not supported.')
    return list(dict.fromkeys(issues))
