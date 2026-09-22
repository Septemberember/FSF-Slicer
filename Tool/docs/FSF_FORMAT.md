# FSF YAML reference

| Field | Meaning |
|---|---|
| `method` | Target Java method name; ambiguous overloads are rejected |
| `inputs` | All method parameters; inferred when omitted |
| `outputs` | Named scalar observations; inferred from a non-void return when omitted |
| `scenarios` | Nonempty list of `{id, T, D, description?}` |
| `analysis` | Validated analysis settings below |
| `metadata` | Optional user metadata copied into reports |

Duplicate YAML keys and unknown fields are errors. Input and output names must be distinct. Scenario IDs contain 1–80 ASCII letters, digits, `_`, or `-`, beginning with a letter or digit; case-insensitive duplicates and platform-reserved names are rejected.

## Variables and bounds

```yaml
inputs:
  x: {type: int, min: -100, max: 100}
outputs:
  result: {type: int, source: return}
  count: {type: int, source: count, min: 0, max: 100}
  exception: {type: int, source: exception}
```

Supported verification types are `byte`, `short`, `int`, `long`, `char`, and `boolean` (`bool` is an alias). Bounds must be finite integers within the selected Java type. Boolean variables have no numeric bounds. If omitted, `int`/`long` inputs use the configured default bounds; narrow integer inputs use the entire Java type range. The report always records effective bounds.

`source: return` observes the method result, including an alias such as `result`. A named local source observes its value at a method exit. A local must exist on every scenario path that constrains it. Outputs absent from a scenario's `D` are not required on that scenario's path.

Output bounds constrain the specified output domain for both soundness and completeness; they are not sampling hints. Integer arithmetic in `T` and `D` follows Java overflow rules. Use `long` expressions explicitly when a specification requires wider intermediate arithmetic.

## Exceptions

`source: exception` is an `int` observation:

| Value | Outcome |
|---:|---|
| 0 | Normal return |
| 1 | `java.lang.ArithmeticException` |
| 2 | `java.lang.IllegalArgumentException` |
| 3 | `java.lang.IllegalStateException` |
| 4 | `java.lang.RuntimeException` |

Explicit supported throws accept literal string messages; messages are not part of the observation. Integer division/remainder by zero produces code 1. Unsupported calls and analysis failures are not encoded as Java exceptions.

```yaml
scenarios:
  - id: division_by_zero
    T: "operator == '/' && num2 == 0"
    D: "exception == 1"
```

A return value does not exist on an exceptional path. An unexpected exception violates a scenario that requires a normal return value. See `examples/calculator_full.fsf.yaml` for all eight calculator scenarios.

## Expressions

Use Java-style comparisons, arithmetic, Boolean operators, bitwise operators, shifts, integer casts, ternary expressions, and `Math`/`StrictMath` `abs`, `min`, and `max`. The logical symbols `∧ ∨ ¬ ≤ ≥ ≠` are accepted as aliases. `T` and `D` must be Boolean. Assignments and increments inside predicates are rejected. Short-circuit and conditional evaluation protect guarded division just as in Java.

## Analysis settings

```yaml
analysis:
  max_paths: 128
  max_loop_iterations: 128
  solver_timeout_ms: 10000
  default_int_min: -100
  default_int_max: 100
  random_seed: 0
  compare_original: true
  compile_slices: true
  check_preservation: true
  slicing_mode: fsf
```

The first three values are positive integers. `max_loop_iterations` is the total across all loops in one execution. `solver_timeout_ms` applies to each solver query. Seeds are integers in `[0, 2^31)`. Reproducibility also requires the same solver version and platform; the seed does not imply uniform random sampling of inputs.

`check_preservation` runs original/slice behavioral comparison and therefore also analyzes the original even when `compare_original` is false. `slicing_mode` is `fsf`, `backward`, or `conditioned`. Disabling compilation reports analysis in the scalar model without a compiler check.

`analyze --force` writes an inconclusive report for invalid specifications. It never converts invalid input into a proof.
