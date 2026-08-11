# FSF-Slicer

FSF-Slicer is the companion repository planned for the manuscript **“FSF-Guided Program Slicing for Testing-Based Formal Verification of Functional Soundness and Completeness.”** The proposed technique constructs an executable, scenario-specific Java slice for each Functional Scenario Form (FSF) pair \((T_i, D_i)\). It uses \(T_i\) to identify scenario-relevant inputs and prune infeasible branches, and \(D_i\) to identify the output behavior that must be preserved before testing-based formal verification (TBFV).

## Preview purpose

The current `main` branch demonstrates the intended public-artifact structure and validation workflow while the actual experiment package is being assembled. It provides:

- A 250-program and 740-task synthetic manifest with the category counts reported in the manuscript.
- Deterministic illustrative RQ1 task metrics.
- Ten illustrative timing runs per task for the RQ2 schema.
- Illustrative paired TBFV outcomes for RQ3, including the reported category-level availability counts.
- Machine-readable copies of the aggregate values reported in manuscript Tables 2-4.
- A validator that checks row counts, category counts, identifiers, ratios, paired outcomes, and aggregate agreement.
- A replacement checklist for converting this preview into a genuine reproducibility artifact.


## Repository layout

```text
.
├── ARTIFACT_STATUS.md
├── Makefile
├── README.md
├── data
│   ├── paper-reported
│   │   ├── README.md
│   │   ├── rq1_category_summary.csv
│   │   ├── rq2_category_summary.csv
│   │   └── rq3_category_summary.csv
│   └── synthetic
│       ├── README.md
│       ├── metadata.json
│       ├── program_manifest.csv
│       ├── rq1_scale.csv
│       ├── rq2_timing_runs.csv
│       ├── rq3_preservation.csv
│       └── task_manifest.csv
├── docs
│   ├── data-dictionary.md
│   ├── methodology-map.md
│   ├── replacement-checklist.md
│   └── validation.md
├── scripts
│   ├── generate_synthetic_preview.py
│   └── validate_preview.py
└── tool
    └── README.md
```

## Quick start

Only Python 3.9 or later is required for the preview.

```bash
make generate
make validate
```

The generator uses a fixed seed. Running it again should reproduce the same CSV and JSON files byte for byte.

## Paper-reported experiment design

The manuscript evaluates 740 scenario-specific slicing tasks derived from 250 Java programs:

| Category | Programs | Tasks | Average FSFs |
|---|---:|---:|---:|
| Branched | 100 | 339 | 3.39 |
| Sequential | 63 | 137 | 2.17 |
| Single-path-Loop | 21 | 57 | 2.71 |
| Multi-path-Loop | 31 | 104 | 3.35 |
| Nested-Loop | 35 | 103 | 2.94 |
| Overall | 250 | 740 | 2.96 |

The reported aggregate findings are stored separately in `data/paper-reported/`:

- RQ1: slices retain 60.79% of LOC, 53.19% of executable statements, and 54.19% of cyclomatic complexity overall.
- RQ2: the overall slice/original total-cost ratio is 0.775, corresponding to a 22.5% reduction.
- RQ3: 718 of 740 paired tasks are conclusive, and all conclusive tasks preserve both soundness and completeness judgments.

## Intended tool workflow

```text
Java program + functional scenario (T_i, D_i)
                  |
                  v
      Parse code and FSF expressions
                  |
                  v
 Build CFG/PDG and compute the scenario core
                  |
                  v
 Apply dependence closure and T_i pruning
                  |
                  v
 Reconstruct an executable Java slice
                  |
                  v
 Run TBFV on the original program and slice
                  |
                  v
 Compare scale, cost, soundness, and completeness
```

The expected production interface is documented in `tool/README.md`; it is a contract for the missing implementation, not an implementation claim.

