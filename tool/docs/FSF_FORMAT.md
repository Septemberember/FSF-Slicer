# FSF YAML format

## Top-level fields

| Field | Required | Meaning |
|---|---:|---|
| `method` | recommended | Java method name; overloads currently select the first matching declaration |
| `inputs` | optional | Mapping from every parameter to its scalar Java type and optional bounds; inferred if omitted |
| `outputs` | optional | Output mapping; inferred as `return_value` for a non-void method |
| `scenarios` | yes | Ordered list of `{id, T, D, description?}` |
| `analysis` | optional | Path, loop, solver, compilation, and comparison settings |
| `metadata` | optional | User-defined metadata copied into the in-memory spec |

## Variables

Compact form:

```yaml
inputs:
  x: int
```

Bounded form:

```yaml
inputs:
  x: {type: int, min: -500, max: 500}
outputs:
  return_value: {type: int, source: return, min: -1000, max: 1000}
```

Supported scalar types are `byte`, `short`, `int`, `long`, `char`, `boolean`, `float`, and `double`.

For a non-return exported local variable:

```yaml
outputs:
  error: {type: int, source: error}
```

The variable must be present when execution returns. Multiple configured scalar outputs are supported by the verification formula.

## Analysis options

```yaml
analysis:
  max_paths: 128
  max_loop_iterations: 128
  solver_timeout_ms: 10000
  default_int_min: -100
  default_int_max: 100
  compare_original: true
  compile_slices: true
```

`max_loop_iterations` is a per-execution total across nested loops. A reached limit produces a bounded/local result, not a false global proof.

