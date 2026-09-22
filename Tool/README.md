# FSF-Slicer 2.0

FSF-Slicer constructs executable Java slices for functional scenarios and verifies functional soundness and completeness using test-induced symbolic paths and Z3. Each scenario supplies a testing condition `T` and a defining condition `D`.

The workflow performs specification validation, control-flow and dependence analysis, scenario specialization, compilation, path exploration, verification, and original/slice comparison. All analysis runs locally.

## Install

Requirements: Python 3.10+ and JDK 17+ on Linux, macOS, or Windows.

```sh
cd Tool
./install.sh
.venv/bin/fsf-tbfv doctor
```

On Windows, run `./install.ps1`, then `.venv/Scripts/fsf-tbfv.exe doctor`.

The release wheel is in `dist/`. For manual installation:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install .
```

## Analyze a program

```sh
.venv/bin/fsf-tbfv analyze \
  --java examples/Calculator.java \
  --fsf examples/calculator_full.fsf.yaml \
  --output calculator-output
```

The eight calculator scenarios cover arithmetic results, division and remainder by zero, and unsupported operators. Additional examples cover cube sums, FizzBuzz, and multiplication by iteration.

Each run writes:

```text
calculator-output/
  report.json
  report.html
  dependence-graph.json
  dependence-graph.dot
  slices/<scenario>/<ClassName>.java
```

Reports include effective input bounds, configuration and seed, source/specification hashes, runtime versions, slicing metrics, pruning obligations, generated tests, path conditions, output expressions, counterexamples, compilation diagnostics, and timings.

## Capabilities

- Structured CFGs, fixed-point reaching definitions, postdominance-based control dependencies, and declaration closure.
- Forward/backward dependence intersection with mandatory output, exception, and termination preservation.
- SMT-proved branch pruning with symbolic assignments, nested path context, and conservative loop handling.
- Source reconstruction that preserves the compilation unit and method interface.
- Java integer overflow, binary numeric promotion, signed division/remainder, shift-distance masking, narrow casts, and Boolean short-circuit evaluation.
- `if`, `switch` with fall-through, `while`, `do-while`, ordinary `for`, `break`, `continue`, return values, exported scalar locals, and supported exceptions.
- Incremental exclusion of explored paths and cached specification parsing, backward slices, and pruning queries.
- Per-path soundness, existential output-set completeness, and explicit coverage checks.
- Same-input relational comparison of original and sliced path summaries, separate from agreement of verification judgments.
- Repeated paired measurements and program-cluster bootstrap confidence intervals.

## Commands

| Command | Purpose |
|---|---|
| `doctor` | Check dependencies and the Java compiler |
| `init-fsf` | Generate a specification scaffold for a selected method |
| `validate-fsf` | Check schema, types, variables, predicate definedness, and scenario domains |
| `slice` | Generate and compile scenario slices |
| `verify` | Verify the original Java method |
| `analyze` | Run the complete workflow and produce JSON/HTML reports |
| `benchmark` | Execute repeated paired runs and summarize measurements |
| `dataset-check` | Inventory parseable Java methods in a directory |
| `suggest-fsf` | Draft a specification using an explicitly enabled compatible API |

Run `fsf-tbfv <command> --help` for arguments.

## Specification

```yaml
method: calculate
inputs:
  num1: {type: int, min: -20, max: 20}
  num2: {type: int, min: -20, max: 20}
  operator: {type: char, min: 37, max: 47}
outputs:
  return_value: {type: int, source: return}
  exception: {type: int, source: exception}
scenarios:
  - id: division
    T: "operator == '/' && num2 != 0"
    D: "exception == 0 && return_value == num1 / num2"
analysis:
  max_paths: 128
  max_loop_iterations: 128
  solver_timeout_ms: 10000
  random_seed: 0
  compile_slices: true
  compare_original: true
  check_preservation: true
  slicing_mode: fsf
```

Input bounds define the domain of every reported judgment. Omitted `int`/`long` bounds default to `[-100, 100]`; `byte`, `short`, and `char` default to their Java ranges. Output bounds are part of the specified output domain for both soundness and completeness. Only outputs referenced in a scenario's `D` are observed for that scenario.

## Judgments

| Result | Meaning within the configured domain |
|---|---|
| `sound` | All scenario inputs are covered and every observation satisfies `D` |
| `locally_sound` | Every completed explored path satisfies `D`; coverage remains partial |
| `unsound` | A violating input is found, including an unexpected supported Java exception |
| `complete` | Every output allowed by `D` is reachable on an explored path |
| `incomplete` | Full input coverage establishes that an allowed output is unreachable |
| `inconclusive` | Coverage, supported semantics, compilation, or SMT results do not establish the requested judgment |

An unvisited output with partial input coverage yields `inconclusive`. A successful completeness proof can hold before full input coverage because already explored paths may reach every specified output. Reaching the loop limit does not establish nontermination.

`comparison.judgment_agreement` is `agree` only when both judgments are definite and equal. `comparison.behavior` checks same-input output/exception observations in the supported semantic model. A relational proof using this model and a shared solver is distinct from independent validation against the JVM; the test suite includes both.

## Supported Java semantics

The parser accepts Java 8 syntax. End-to-end verification targets static intraprocedural methods over `byte`, `short`, `int`, `long`, `char`, and `boolean`, with `Math`/`StrictMath` `abs`, `min`, and `max`. Standalone increments and scalar compound assignments are supported. Expected exceptions use the explicit `exception` output described in [FSF_FORMAT.md](docs/FSF_FORMAT.md).

Floating-point arithmetic, heap state, arrays, strings, class initialization, inheritance, reflection, dynamic dispatch, recursion, concurrency, exception handlers, labeled jumps, and side effects embedded inside expressions require additional semantic models. Unsupported execution is reported as inconclusive; unsupported reconstruction retains the original source. Compiler failure prevents a definite verification judgment. Console text is outside the output observation model; supported print arguments are still evaluated for arithmetic effects.

## Repeated measurements

```sh
.venv/bin/fsf-tbfv benchmark \
  --manifest examples/benchmark.yaml \
  --repeats 10 --seed 2026 \
  --modes fsf,backward,conditioned \
  --output benchmark-output
```

`runs.csv` records each program/scenario/repetition and `summary.json` reports paired timings and program-cluster confidence intervals. Run order is seeded and shuffled. The supplied manifest covers four programs and sixteen scenarios. These measurements describe the bundled examples; they do not substitute for the paper's 250-program experiment.

## Development

```sh
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest
.venv/bin/python -m build
```

- [Algorithm and preservation contract](docs/ALGORITHM.md)
- [Specification reference](docs/FSF_FORMAT.md)
- [Reproducibility](docs/REPRODUCTION_NOTES.md)
- [Release validation](docs/RELEASE_VALIDATION.md)
- [Dependency notices](THIRD_PARTY_NOTICES.md)

The code is distributed under the [MIT license](LICENSE). The `Tool` directory is self-contained; the existing `tool` directory is retained separately in the repository.
