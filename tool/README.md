# Production Tool Interface Contract

The production artifact should provide a Java command-line interface equivalent to:

```bash
java -jar fsf-slicer.jar \
  --program benchmarks/Branched/BR-001/original.java \
  --fsf benchmarks/Branched/BR-001/fsf.yaml \
  --scenario T1 \
  --output build/BR-001/T1
```

## Required outputs

```text
build/BR-001/T1/
├── slice.java
├── slicing.json
├── original-verification.json
├── slice-verification.json
└── timing.json
```

`slicing.json` should include the selected input and output variables, input and export locations, retained dependence nodes, pruned branches, original/slice static metrics, and deterministic tool version information.

The two verification files should include the explored path conditions, output state representations, coverage result, soundness judgment, completeness judgment, and any conclusive or inconclusive status.

`timing.json` should separate slicing, dynamic execution, path derivation, SMT solving, other processing, and end-to-end time.

## Required modules

1. Java and FSF parsers.
2. CFG and PDG construction.
3. Forward and backward slicing.
4. Scenario-core construction and dependence closure.
5. Testing-condition feasibility checks and branch pruning.
6. Executable Java reconstruction.
7. Constraint-based test generation and dynamic execution.
8. Path-condition and state-representation derivation.
9. Z3-based soundness and completeness verification.
10. Structured result export.

No executable implementation is included in this preview repository.
