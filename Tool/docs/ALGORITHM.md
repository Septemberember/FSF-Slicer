# Algorithm and preservation contract

## Scenario validation

A functional scenario is `(T, D)`. `T` uses input parameters; `D` constrains at least one output. Predicates must be Boolean and free of undefined integer division/remainder in their admitted domains. IDs are unique portable directory names. YAML duplicate keys, unknown settings, invalid bounds, and mismatched Java/FSF types are errors.

Scenario testing conditions are checked for satisfiability and pairwise exclusivity. Incomplete input-family coverage is reported explicitly. Distinct scenarios may have overlapping output ranges: addition and subtraction, for example, can produce the same integer. Such overlap does not invalidate a scenario-specific verification obligation.

## Slicing

For the inputs `X = inputs(T) ∪ inputs(D)` and outputs `Y = outputs(D)`:

```text
F    = union of forward slices from X's parameter locations
B    = union of backward slices from Y's export locations
Core = F ∩ B
Seeds = Core ∪ output exports ∪ required termination/exception/effect nodes
S    = predecessor and declaration closure of Seeds
Slice = reconstruct(prune under domain ∧ T, S)
```

Output exports remain mandatory even when `Core` is empty. This preserves constant outputs and dependencies on inputs absent from the specification. Return/throw, loops, abrupt control, potentially throwing arithmetic, and modeled/unknown calls remain in the conservative preservation closure. Removing a loop solely because it does not affect a returned value could change termination and is therefore avoided.

`cfg.py` constructs structured control-flow edges, including early returns, loop back edges, `break`, `continue`, and switch fall-through. A worklist reaches the fixed point of reaching definitions; strong updates kill earlier scalar definitions. A combined `for` header uses weak updates to conservatively account for initialization and updates. Postdominance yields control dependencies, supplemented by structural containment for reconstruction. The PDG is an intraprocedural overapproximation and is exported as JSON and DOT.

Branch specialization propagates typed symbolic assignments through straight-line code. Unresolved joins retain only common symbolic bindings. Loop-modified variables are forgotten before specializing the body and continuation. A branch is pruned only after Z3 returns `unsat` for its feasibility obligation. Division guards must also be proved safe before their expressions are used for specialization. `unknown` retains code. Each pruning proof records the original source line and discharged obligation.

The original method signature and surrounding compilation unit remain intact. New block scopes are retained when selecting an `if` arm. `javac -proc:none` checks the original and each slice by default.

`backward` uses the output dependency closure without scenario pruning. `conditioned` combines output closure with the same scenario pruning. `fsf` also computes and records the forward/backward core. Mandatory output closure can make the conditioned and FSF slices identical; the implementation does not assume an extra reduction from the intersection alone.

## Testing

Z3 selects an input from `domain ∧ T`. The scalar executor follows that input, records branch and arithmetic-exception conditions, and substitutes assignments to derive `(C_i, f_i)`. Concrete scalar values are evaluated from the same typed expressions, including overflow at intermediate operations. An incremental solver adds `¬C_i` after each explored path.

The generated input must satisfy its derived path condition. Only completed supported paths contribute to full input coverage. Truncated and unsupported paths retain diagnostics and do not establish coverage. The loop bound counts all loop-body iterations in one execution, including nested loops.

## Verification

For each completed path, soundness checks:

```text
domain ∧ T ∧ C_i ∧ ¬D(f_i(x)/y)
```

Configured output bounds and expression-definedness conditions are included in `D`. A satisfying model is a counterexample. If all obligations are unsatisfiable, full input coverage establishes `sound`; a nonempty set of completed normal or specified-exception paths without full coverage establishes `locally_sound`.

Completeness keeps the observed output symbols free and quantifies inputs independently:

```text
∃x(domain ∧ T ∧ D)
∧ ¬∨_i ∃x(domain ∧ T ∧ C_i ∧ y=f_i(x))
```

An unsatisfiable result establishes `complete`, including before full input coverage. A satisfying result establishes `incomplete` only with full input coverage. Otherwise it is `inconclusive`. No `locally_complete` verdict is emitted. Empty input vectors are handled without constructing an invalid empty quantifier.

## Preservation checks

The behavior checker compares each pair of original/slice completed paths under the same input symbols:

```text
domain ∧ T ∧ C_original ∧ C_slice ∧ (observation_original ≠ observation_slice)
```

A satisfying model is a preservation counterexample. Full coverage of both programs and unsatisfiability of every comparison establish `equivalent` in the supported semantic model. Otherwise the result is `inconclusive`. This check is stronger than equal soundness/completeness labels but shares the executor and solver; independent JVM differential tests provide a separate validation channel.

The contract concerns outputs selected by `D` and supported exception outcomes on inputs satisfying the configured domain and `T`. Behavior outside that domain is unspecified. The implementation retains loops conservatively; it does not prove termination of unbounded computations.

## Semantic references

The integer operations follow the [Java Language Specification, Chapter 15](https://docs.oracle.com/javase/specs/jls/se17/html/jls-15.html). Integer formulas use [Z3 bit-vectors](https://microsoft.github.io/z3guide/docs/theories/Bitvectors/). `int` and `long` use 32 and 64 bits; `byte`, `short`, and `char` are narrowed at storage/cast boundaries and promoted for arithmetic.
