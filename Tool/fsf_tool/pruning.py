"""Scenario specialization with symbolic assignments and conservative loop havoc."""
import javalang as jl
import z3
from .expression import ExpressionEngine, cast_value, type_to_string


class BranchPruner:
    def __init__(self, spec, symbols, domain):
        self.spec = spec
        self.symbols = symbols
        self.domain = domain
        self.types = {n: v.type for n, v in spec.inputs.items()}
        self.solver = z3.Solver()
        self.solver.set(timeout=spec.config.solver_timeout_ms, random_seed=spec.config.random_seed)
        self.cache = {}
        self.decisions = {}
        self.proofs = []

    def impossible(self, formula):
        formula = z3.simplify(z3.And(self.domain, formula))
        key = formula.sexpr()
        if key not in self.cache:
            self.solver.push()
            self.solver.add(formula)
            self.cache[key] = self.solver.check() == z3.unsat
            self.solver.pop()
        return self.cache[key]

    def expression(self, node, env, path):
        engine = ExpressionEngine(self.types)
        value = engine.evaluate(node, env)
        if engine.guards and not self.impossible(z3.And(path, z3.Not(z3.And(*engine.guards)))):
            raise ValueError('Expression may throw on this path.')
        return value

    def run(self, statements, testing):
        self.walk_many(statements, dict(self.symbols), testing)
        return self.decisions

    def walk_many(self, statements, env, path):
        for node in statements:
            self.walk(node, env, path)

    def walk(self, node, env, path):
        if node is None: return
        if isinstance(node, jl.tree.BlockStatement):
            self.walk_many(node.statements, env, path)
        elif isinstance(node, jl.tree.LocalVariableDeclaration):
            kind = type_to_string(node.type)
            for decl in node.declarators:
                self.types[decl.name] = kind
                env.pop(decl.name, None)
                if decl.initializer is not None:
                    try: env[decl.name] = cast_value(kind, self.expression(decl.initializer, env, path))
                    except Exception: pass
        elif isinstance(node, jl.tree.StatementExpression):
            expr = node.expression
            name = None
            if isinstance(expr, jl.tree.Assignment) and isinstance(expr.expressionl, jl.tree.MemberReference):
                name = expr.expressionl.member
                rhs = expr.value if expr.type == '=' else jl.tree.BinaryOperation(operator=expr.type[:-1], operandl=expr.expressionl, operandr=expr.value)
            elif isinstance(expr, jl.tree.MemberReference) and any(op in {'++', '--'} for op in (expr.prefix_operators or []) + (expr.postfix_operators or [])):
                name = expr.member
                ops = (expr.prefix_operators or []) + (expr.postfix_operators or [])
                rhs = jl.tree.BinaryOperation(operator='-' if '--' in ops else '+', operandl=jl.tree.MemberReference(member=name, qualifier='', selectors=[], prefix_operators=[], postfix_operators=[]), operandr=jl.tree.Literal(value='1', prefix_operators=[], postfix_operators=[]))
            if name:
                try: env[name] = cast_value(self.types.get(name, 'int'), self.expression(rhs, env, path))
                except Exception: env.pop(name, None)
        elif isinstance(node, jl.tree.IfStatement):
            try:
                condition = self.expression(node.condition, env, path)
                if not isinstance(condition, bool) and not z3.is_bool(condition): raise ValueError()
            except Exception:
                condition = None
            if condition is not None:
                decision = None
                if self.impossible(z3.And(path, condition)): decision = False
                elif self.impossible(z3.And(path, z3.Not(condition))): decision = True
                if decision is not None:
                    self.decisions[id(node)] = decision
                    self.proofs.append({'line': getattr(node.position, 'line', None), 'selected': decision,
                                        'obligation': str(z3.simplify(z3.And(self.domain, path, z3.Not(condition) if decision else condition))), 'result': 'unsat'})
                    self.walk(node.then_statement if decision else node.else_statement, env, path)
                    return
            yes, no = dict(env), dict(env)
            self.walk(node.then_statement, yes, z3.And(path, condition) if condition is not None else path)
            self.walk(node.else_statement, no, z3.And(path, z3.Not(condition)) if condition is not None else path)
            env.clear()
            env.update({key: value for key, value in yes.items() if key in no and self.same(value, no[key])})
        elif isinstance(node, (jl.tree.WhileStatement, jl.tree.DoStatement, jl.tree.ForStatement)):
            modified = self.modified(node)
            for name in modified: env.pop(name, None)
            self.walk(node.body, dict(env), path)
        elif isinstance(node, jl.tree.SwitchStatement):
            modified = self.modified(node)
            for name in modified: env.pop(name, None)
            # Case guards and fall-through are kept together.

    @staticmethod
    def same(a, b):
        if isinstance(a, z3.AstRef) and isinstance(b, z3.AstRef): return z3.eq(a, b)
        return type(a) == type(b) and not isinstance(a, z3.AstRef) and a == b

    @staticmethod
    def modified(node):
        result = set()
        for _, child in node:
            if isinstance(child, jl.tree.VariableDeclarator): result.add(child.name)
            elif isinstance(child, jl.tree.Assignment) and isinstance(child.expressionl, jl.tree.MemberReference): result.add(child.expressionl.member)
            elif isinstance(child, jl.tree.MemberReference) and any(op in {'++', '--'} for op in (child.prefix_operators or []) + (child.postfix_operators or [])): result.add(child.member)
        return result
