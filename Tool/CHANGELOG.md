# Changelog

## 2.0.1 — 2026-09-28

- Check small declared output domains with exact output-tuple enumeration and separate quantifier-free specification/reachability queries, preserving independent input witnesses and genuine unknown results.
- Align the cube-sum example with the revised integer input bound 784 and provide an independent-analysis runner for all four Table 1 alternatives.
- Record actual test-generation solver checks, including exhaustion checks, separately from execution paths.
- Check all four specification variants at input bounds 500, 784, and 800 against independent JVM enumeration; retain unreachable-output and soundness counterexamples.
- Add regressions for multiple-output correlations, different input witnesses, partial coverage, loop limits, solver unknown, and full-width long output domains.


## 2.0.0 — 2026-09-22

- Add structured CFG construction, reaching-definition analysis, postdominance, graph exports, and declaration closure.
- Preserve constant exports, scenario-unmentioned dependencies, abrupt control, exceptions, and termination-relevant loops.
- Specialize branches using symbolic assignments, nested conditions, conservative joins, and loop-variable invalidation.
- Correct Java integer promotion, intermediate overflow, signed division/remainder, shifts, casts, conditional evaluation, and Boolean short-circuit semantics.
- Correct switch fall-through and return/output aliases; support explicit exception observations and all eight calculator scenarios.
- Correct partial-coverage completeness to `inconclusive` and prevent unsupported/compile-failed paths from establishing a definite proof.
- Add same-input original/slice behavior checks separate from conclusive judgment agreement.
- Validate YAML duplicates, unknown settings, types, bounds, predicate definedness, and portable scenario identifiers.
- Add incremental path exclusion, expression/backward-slice/pruning caches, seeded paired benchmarks, raw measurement export, and program-cluster intervals.
- Add JVM differential validation, regression coverage, reproducibility metadata, source distributions, and release checksums.
