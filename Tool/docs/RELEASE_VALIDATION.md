# Release validation

## 2.0.1 — 2026-09-28

Validated with Python 3.12.14, Z3 4.12.2, and JDK 26 on macOS arm64.
The complete automated suite passed: **110 tests, zero failures, errors, or skips**.
The independent cube-sum oracle compiled the Java program and enumerated every
integer input from 1 through 800. All four specification rows were checked at
input bounds 500, 784, and 800 against the original and compiled slice (twelve
row/domain combinations).

The standalone reproduction command was also run separately for all three
domains. At 784, rows 2 and 4 report the unreachable output 8; all four rows
have seven positive paths and ten test-generation checks across both scenarios.
At 500 all rows are complete. At 800 all rows are complete with eight positive
paths and eleven checks. Every same-input original/slice comparison is equivalent
within the configured domain and supported semantic model.

Fresh evidence:

- `validation/tests-2.0.1.xml`
- `validation/table1-500-2.0.1.json`
- `validation/table1-784-2.0.1.json`
- `validation/table1-800-2.0.1.json`

The JSON summaries contain single-run timings, not the paper's historical times
or repeated statistical estimates. Run `scripts/reproduce_table1.py` to regenerate
the full per-row reports and slices. The 2.0.0 benchmark evidence below remains a
record of that release; the full historical 250-program/740-scenario study has not
been rerun as part of this correction.

## 2.0.0

Validated on 2026-09-22 with Python 3.12.14, Z3 4.12.2, javalang 0.13.0, and JDK 26 on macOS arm64. The test environment reported 18 logical CPUs. Other supported installation platforms are not claimed as tested by this run.

| Check | Result |
|---|---|
| Automated regression suite | 92 tests passed; no failures, errors, or skips |
| Arithmetic JVM oracle | 1,617 expression/input combinations checked against compiled Java, with both concrete and symbolic evaluation |
| Execution JVM oracle | Seven control-flow/arithmetic methods, seven inputs each |
| Slice JVM oracle | Twelve original/slice method pairs, seven identical inputs each |
| Paired benchmark | Sixteen scenarios across four programs × three modes × two repetitions = 96 scenario rows |
| Definite judgment agreement | 96/96 scenario rows |
| Supported-model behavior equivalence | 96/96 scenario rows |
| Dataset parsing | 300/301 sources; one existing syntax error retained and reported |
| Distribution | Wheel, source archive, and self-contained release ZIP |

The regression suite covers constant outputs, unmentioned input dependencies, reassigned parameters, early returns, switch fall-through, loop abrupt control, empty input vectors, overflow, long division, narrow casts, shifts, unary operators on parentheses/casts, division exceptions, short-circuiting, expected exceptions, parser errors, output aliases, invalid YAML/settings, compiler failure, solver unknown, partial coverage, and benchmark error handling.

The calculator's eight scenarios all compile and produce `sound` and `complete` within their declared domains. The cube-sum, FizzBuzz, and iterative multiplication families are included in the paired benchmark. Assertions validate behavior and proof boundaries rather than substituting historical experimental labels.

Evidence:

- `validation/tests.xml`: machine-readable test results.
- `validation/dataset-check.json`: source inventory and parse diagnostics.
- `validation/benchmark/runs.csv`: unaggregated paired measurements.
- `validation/benchmark/summary.json`: environment, aggregation, intervals, and counts.
- `validation/benchmark/details.zip`: per-run specifications, reports, graphs, and generated Java source.

Only current release measurements are reported. The 96 repeated rows are not 96 independent programs; uncertainty is grouped by the four program IDs. These checks establish evidence for the tested workload and supported semantic model, not unrestricted Java correctness.
