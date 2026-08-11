# Algorithm-to-implementation mapping

## 1. Functional scenario

Each YAML scenario is a pair `(T, D)`. `T` may use only configured input variables. `D` must mention at least one configured output. The validator also checks that each `T` is satisfiable, pairwise input exclusivity, and coverage of the configured input domain.

## 2. FSF-guided slicing

`fsf_tool.pdg.PDGBuilder` creates statement nodes with DEF/USE sets and conservative data/control edges. Parameter pseudo-nodes represent input locations. Return statements or configured variable exports represent output locations.

For a scenario, `fsf_tool.slicer.FSFGuidedSlicer` computes:

```text
X_i    = inputs(T_i) ∪ inputs(D_i)
Core_i = ⋃ (ForwardSlice(input location) ∩ BackwardSlice(output export))
S_i    = DependenceClosure(Core_i)
FPS    = Reconstruct(PruneUnderT(S_i))
```

Branch pruning is proof-based. An input-only branch `B` is removed only if Z3 proves either `domain ∧ T ∧ B` or `domain ∧ T ∧ ¬B` unsatisfiable. A branch whose feasibility is not decided is retained. Reconstruction emits a new Java class and the result is compiled with `javac`.

## 3. Testing stage

For each scenario the remaining test region starts as `domain ∧ T`. Z3 selects a concrete test model. `ConcolicExecutor` executes the selected Java path with a concrete environment and a symbolic environment at the same time.

Every chosen branch contributes `B` or `¬B` to `C_i`. Assignments update the symbolic state, so the return/export value becomes `f_i(x)`. The next iteration solves:

```text
domain ∧ T ∧ ¬C_1 ∧ ... ∧ ¬C_k
```

This is the executable form of the paper's update `T := T ∧ ¬C`.

## 4. Soundness

For every completed path, the engine asks Z3 whether the negation of the path obligation is satisfiable:

```text
domain ∧ T ∧ C_i ∧ ¬D(f_i(x)/y)
```

- `sat`: `unsound`, with the model as counterexample.
- all obligations `unsat` and `T ⇒ C_1∨...∨C_k`: `sound`.
- all explored obligations `unsat` without total path coverage: `locally_sound`.

## 5. Completeness

Configured output symbols remain free while inputs are existentially quantified. The engine checks for an output allowed by the scenario but not produced by any explored path:

```text
∃x(domain ∧ T ∧ D)
∧ ¬∨_i ∃x(domain ∧ T ∧ C_i ∧ y=f_i(x))
```

- `unsat`: `complete` for the configured domain.
- `sat` plus complete input-path coverage: `incomplete` with an output counterexample.
- `sat` plus partial input-path coverage: `locally_complete`.
- solver `unknown`: `inconclusive`.

## 6. Preservation experiment

The `analyze` command runs the same scenario with the same domain and limits on the original method and the scenario-specific slice. JSON/HTML reports keep both judgments and slicing metrics so preservation can be independently inspected.

