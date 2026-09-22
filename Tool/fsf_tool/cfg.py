"""Structured control flow, reaching definitions and postdominance."""
from collections import deque
import javalang as jl


class ControlFlowGraph:
    ENTRY = 0
    EXIT = -1

    def __init__(self, program, nodes, node_ids, parameters):
        self.nodes = nodes
        self.ids = node_ids
        self.edges = {i: set() for i in [self.ENTRY, self.EXIT, *nodes]}
        first = self.sequence(program.method.body or [], self.EXIT, None, None)
        for param in reversed(list(parameters.values())):
            self.edges[param].add(first)
            first = param
        self.edges[self.ENTRY].add(first)
        self.reverse = {i: set() for i in self.edges}
        for a, targets in self.edges.items():
            for b in targets:
                self.reverse[b].add(a)

    def sequence(self, statements, follow, brk, cont):
        for node in reversed(statements):
            follow = self.statement(node, follow, brk, cont)
        return follow

    def statement(self, node, follow, brk, cont):
        if node is None: return follow
        if isinstance(node, jl.tree.BlockStatement):
            return self.sequence(node.statements, follow, brk, cont)
        i = self.ids[id(node)]
        if isinstance(node, (jl.tree.ReturnStatement, jl.tree.ThrowStatement)):
            self.edges[i].add(self.EXIT)
        elif isinstance(node, jl.tree.BreakStatement):
            self.edges[i].add(brk if brk is not None else self.EXIT)
        elif isinstance(node, jl.tree.ContinueStatement):
            self.edges[i].add(cont if cont is not None else self.EXIT)
        elif isinstance(node, jl.tree.IfStatement):
            self.edges[i].update([self.statement(node.then_statement, follow, brk, cont), self.statement(node.else_statement, follow, brk, cont)])
        elif isinstance(node, (jl.tree.WhileStatement, jl.tree.DoStatement, jl.tree.ForStatement)):
            body = self.statement(node.body, i, follow, i)
            self.edges[i].update([body, follow])
            if isinstance(node, jl.tree.DoStatement): return body
        elif isinstance(node, jl.tree.SwitchStatement):
            next_case = follow
            for case in reversed(node.cases):
                next_case = self.sequence(case.statements, next_case, follow, cont)
                self.edges[i].add(next_case)
            if not any(not case.case for case in node.cases): self.edges[i].add(follow)
        else:
            self.edges[i].add(follow)
        return i

    def data_edges(self):
        """Forward fixed point. Compound for headers use weak updates."""
        incoming = {i: set() for i in self.edges}
        outgoing = {i: set() for i in self.edges}
        queue, queued = deque(self.edges), set(self.edges)
        while queue:
            i = queue.popleft()
            queued.discard(i)
            current = set().union(*(outgoing[p] for p in self.reverse[i]))
            incoming[i] = current
            node = self.nodes.get(i)
            if node:
                if not isinstance(node.ast, jl.tree.ForStatement):
                    current = {(var, loc) for var, loc in current if var not in node.defs}
                current |= {(var, i) for var in node.defs}
            if current != outgoing[i]:
                outgoing[i] = current
                for child in self.edges[i]:
                    if child not in queued:
                        queue.append(child)
                        queued.add(child)
        result = set()
        for i, node in self.nodes.items():
            for var, source in incoming[i]:
                if var in node.uses: result.add((source, i))
        return result

    def control_edges(self):
        universe = set(self.edges)
        post = {i: ({i} if i == self.EXIT else set(universe)) for i in universe}
        # Include an exit alternative for regions without an exit path. Loops are
        # also retained explicitly by the slicer's termination closure.
        reaches_exit, queue = {self.EXIT}, [self.EXIT]
        while queue:
            for parent in self.reverse[queue.pop()]:
                if parent not in reaches_exit:
                    reaches_exit.add(parent)
                    queue.append(parent)
        successors = {i: targets | ({self.EXIT} if i not in reaches_exit else set()) for i, targets in self.edges.items()}
        changed = True
        while changed:
            changed = False
            for i in sorted(universe - {self.EXIT}, reverse=True):
                succ = successors[i] or {self.EXIT}
                value = {i} | set.intersection(*(post[s] for s in succ))
                if value != post[i]:
                    post[i] = value
                    changed = True
        result = set()
        for a, successors_a in successors.items():
            if len(successors_a) > 1:
                for b in successors_a:
                    result.update((a, n) for n in post[b] - post[a] if a in self.nodes and n in self.nodes)
        return result
