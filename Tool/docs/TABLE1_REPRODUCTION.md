# Reproducing the revised cube-sum example

Run from `Tool/` after installing this version:

```sh
.venv/bin/python scripts/reproduce_table1.py --output cube-table-output
```

This runs `examples/UserInputProgram.java` with four independent versions of
`examples/cube_sum.fsf.yaml`. Each version retains the nonpositive scenario and
one positive scenario. The positive definitions use the paper's four combinations
of strict/non-strict lower and upper bounds, without changing the program.
Both the original and compiled slice are verified and compared.

## Domain and expected results

Let `A(n) = (n-1)^2 n^2 / 4` and `B(n) = n^2 (n+1)^2 / 4`, interpreted with the
integer domains below. The positive input domain is `1..784`, where
`784 = 1^3 + ... + 7^3`. The actual positive outputs are exactly `1..7`.

| Row | Defining condition | Allowed outputs | Soundness | Completeness |
|---|---|---|---|---|
| 1 | `A(n) < x <= B(n)` | `1..7` | sound | complete |
| 2 | `A(n) <= x <= B(n)` | `1..8` | sound | incomplete |
| 3 | `A(n) < x < B(n)` | `2..7` | unsound | complete |
| 4 | `A(n) <= x < B(n)` | `2..8` | unsound | incomplete |

At `x=784`, rows 2 and 4 allow `n=8`, but no input in `1..784` produces 8.
At `x=1`, the program produces 1 and violates the strict upper bound of rows
3 and 4. Inputs `1, 2, 10, 37, 101, 226, 442` witness outputs `1..7`.
The verifier checks output-set inclusion: a specification witness and a program
witness for the same output can use different inputs.

The input configuration also includes `-20..0` for the nonpositive scenario.
The explicitly declared output domain is `-1..10`, including the unreachable
value 8. Within this domain, all intermediate products in the defining formulas
fit Java `int`, and each division by four is exact, so the formulas agree with
the mathematical integer example. For these input bounds, mathematical outputs
outside the declared output domain cannot satisfy the formulas. Removing the
output bounds instead changes the FSF to full-width Java arithmetic: overflow
can admit large spurious mathematical outputs. The tool does not silently
reinterpret Java expressions as unbounded integers or discard such outputs.

## Evidence and counting

Each row gets its own `spec.fsf.yaml`, `report.json`, `report.html`, generated
slice, and dependence graph. `summary.json` records actual judgments, witnesses,
test inputs, source/specification hashes, tool/runtime versions, and fresh
single-run timings. It does not contain the historical paper's timings.

The positive scenario has seven paths and eight test-generation checks; the
nonpositive scenario has one path and two checks. The final unsatisfiable check
is included for each scenario, giving ten checks in total. Other feasibility,
verification, and preservation solver calls are not counted in that field.

Alternative domains can be reproduced explicitly:

```sh
.venv/bin/python scripts/reproduce_table1.py --upper-bound 500 --output cube-500-output
.venv/bin/python scripts/reproduce_table1.py --upper-bound 800 --output cube-800-output
```

At 500 all four rows are complete. At 800 the output 8 becomes reachable, all
four rows are again complete, and there are eight positive paths (eleven
test-generation checks across both scenarios). The runner reports solver results
and never assigns these labels from this table.

`tests/test_cube_sum.py` independently compiles the Java program, executes every
positive input through 800, computes the mathematical specification output sets,
and compares them with the original and sliced verifier results for all twelve
row/domain combinations.

## Understanding inconclusive results

- The four table rows are alternative specifications. Combining their identical
  positive testing conditions into one family produces `NON_EXCLUSIVE_T`.
  `analyze --force` reports invalid specifications as inconclusive; it is not a
  way to turn overlapping alternatives into a valid FSF. Use the runner above.
- For at most 256 declared output tuples, the verifier now uses separate
  quantifier-free SAT checks for membership in the specified and reached output
  sets. The entire output domain is considered, including unreachable outputs.
  This avoids relying on quantified nonlinear bit-vector solving for this case.
- A genuine solver timeout/unknown or a truncated execution remains unresolved.
  Missing an output proves incompleteness only after full input coverage. Check
  the reported reason, coverage, and configured path/loop limits.
- Reinstall after updating the repository. The wheel, source archive, and ZIP
  for this correction are version 2.0.1; installing a 2.0.0 artifact does not use
  the new code.
