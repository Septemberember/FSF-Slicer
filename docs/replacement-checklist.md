# Empirical Artifact Replacement Checklist

Use this checklist before replacing the synthetic preview with the paper artifact.

## Benchmark identity

- [ ] Add the exact manifest of 250 evaluated programs.
- [ ] Confirm category counts of 100, 63, 21, 31, and 35.
- [ ] Record a source, version, and redistribution status for every program.
- [ ] Remove helper files from benchmark counts.
- [ ] Assign stable program identifiers that match every result table.

## Functional scenarios and slices

- [ ] Add exactly 740 reviewed FSF pairs.
- [ ] Confirm task counts of 339, 137, 57, 104, and 103 by category.
- [ ] Store each testing condition and defining condition without normalization loss.
- [ ] Add each generated executable slice or a deterministic regeneration command.
- [ ] Compile every original program and generated slice in a clean environment.

## Tool implementation

- [ ] Add the Java parsing, FSF parsing, CFG, PDG, slicing, pruning, reconstruction, execution, and verification modules.
- [ ] Pin Z3 4.12.2, JavaParser 3.25.4, and Subprocess 3.10.9, or update the manuscript and artifact together.
- [ ] Document Java, Python, operating-system, and solver requirements.
- [ ] Include a small end-to-end example with expected outputs.

## RQ1

- [ ] Export original and slice LOC, executable statements, and cyclomatic complexity for every task.
- [ ] Recompute category means from task-level ratios.
- [ ] Recompute the task-weighted overall means.
- [ ] Confirm that the recomputed values round to Table 2.

## RQ2

- [ ] Export all ten timing repetitions per task.
- [ ] Record dynamic execution, path derivation, SMT solving, slicing, result-generation, and total time.
- [ ] Document warm-up, timeout, stopping, input-range, and cluster-allocation rules.
- [ ] Confirm that total slice time includes slicing.
- [ ] Recompute task, category, and task-weighted overall ratios for Table 3.

## RQ3

- [ ] Export paired original/slice soundness and completeness judgments.
- [ ] Identify the 718 conclusive and 22 inconclusive pairs.
- [ ] Record failure evidence for every inconclusive pair.
- [ ] Confirm that no mixed-availability pair exists.
- [ ] Recompute conclusive preservation and judgment agreement for Table 4.

## Publication hygiene

- [ ] Replace all `SYNTHETIC_ILLUSTRATIVE` files; do not relabel synthetic rows.
- [ ] Remove unrelated projects, development logs, credentials, local paths, IDE metadata, and temporary files.
- [ ] Scan all public text for unsupported claims and non-English content.
- [ ] Add a license and verify third-party redistribution rights.
- [ ] Run validation and a clean end-to-end reproduction before merging to `main`.

