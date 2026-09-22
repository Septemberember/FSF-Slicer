# Changelog

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
