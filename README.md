# FSF-Slicer

FSF-Slicer is the artifact repository for the manuscript **“FSF-Guided Program Slicing for Testing-Based Formal Verification of Functional Soundness and Completeness.”**

The artifact contains a Java dataset, task-level experimental results, category-level summaries, and an executable prototype tool for **FSF-guided program slicing** and **testing-based formal verification (TBFV)**. Given a Java program and a Functional Scenario Form (FSF) specification, the tool constructs executable scenario-specific slices for functional scenarios \((T_i,D_i)\), and then compares the original program and the generated slices with respect to program scale, verification cost, and verification-result preservation.

## Main Idea

For each functional scenario \((T_i,D_i)\):

- \(T_i\) defines the input domain and is used to identify scenario-relevant inputs and prune infeasible branches.
- \(D_i\) defines the output behavior that should be preserved.
- FSF-Slicer constructs an executable Java slice that preserves the verification-relevant behavior of the original program under the selected functional scenario.
- TBFV is then applied to analyze functional soundness and functional completeness on the original program and on the corresponding slice under the same settings.

## Repository Layout

```text
.
├── README.md
├── Makefile
├── .github/
│   └── workflows/
│       └── validate-preview.yml
├── Experimental-results/
│   ├── program_manifest.csv
│   ├── task_manifest.csv
│   ├── rq1_scale.csv
│   ├── rq1_category_summary.csv
│   ├── rq2_timing_runs.csv
│   ├── rq2_category_summary.csv
│   ├── rq3_preservation.csv
│   └── rq3_category_summary.csv
├── FSF-Slicer-Dataset/
│   ├── Branched3/
│   ├── Sequential3/
│   ├── Single-path-Loop3/
│   ├── Multi-path-Loop3/
│   └── Nested-Loop3/
└── tool/
    ├── README.md
    ├── LICENSE
    ├── pyproject.toml
    ├── requirements.txt
    ├── install.sh
    ├── install.ps1
    ├── fsf_tool/
    ├── examples/
    ├── docs/
    ├── tests/
    ├── scripts/
    ├── configs/
    ├── datasets/
    └── dist/
```

## Artifact Contents

### 1. Java Dataset

The Java programs used in the experiment are placed under `FSF-Slicer-Dataset/`. The dataset is organized into five structural categories:

| Category | Directory |
|---|---|
| Branched programs | `FSF-Slicer-Dataset/Branched3/` |
| Sequential programs | `FSF-Slicer-Dataset/Sequential3/` |
| Single-path-loop programs | `FSF-Slicer-Dataset/Single-path-Loop3/` |
| Multi-path-loop programs | `FSF-Slicer-Dataset/Multi-path-Loop3/` |
| Nested-loop programs | `FSF-Slicer-Dataset/Nested-Loop3/` |

A tool-local copy of the dataset is also included under `tool/datasets/PCaE-Dataset/` for running the prototype commands from the `tool/` directory.

### 2. Experimental Results

The `Experimental-results/` directory contains the CSV files used to report the three research questions in the paper.

| File | Description |
|---|---|
| `program_manifest.csv` | Program-level manifest, including program identifiers, categories, and scenario counts. |
| `task_manifest.csv` | Scenario-specific task manifest. Each task corresponds to one \((P,(T_i,D_i))\) pair. |
| `rq1_scale.csv` | Task-level RQ1 results for program-scale reduction. |
| `rq1_category_summary.csv` | Category-level RQ1 summary. |
| `rq2_timing_runs.csv` | Repeated timing results for RQ2. |
| `rq2_category_summary.csv` | Category-level RQ2 summary. |
| `rq3_preservation.csv` | Task-level RQ3 results for verification-result preservation. |
| `rq3_category_summary.csv` | Category-level RQ3 summary. |

The experiment contains **250 Java programs** and **740 scenario-specific verification tasks**.

| Category | Programs | Tasks | Average FSFs |
|---|---:|---:|---:|
| Branched | 100 | 339 | 3.39 |
| Sequential | 63 | 137 | 2.17 |
| Single-path-Loop | 21 | 57 | 2.71 |
| Multi-path-Loop | 31 | 104 | 3.35 |
| Nested-Loop | 35 | 103 | 2.94 |
| Overall | 250 | 740 | 2.96 |

### RQ1: Program-Scale Reduction

RQ1 evaluates whether FSF-guided slicing reduces the static scale of programs.

| Category | LOC Ratio | Executable Statement Ratio | Cyclomatic Complexity Ratio |
|---|---:|---:|---:|
| Branched | 0.4690 | 0.3546 | 0.3478 |
| Sequential | 0.9930 | 1.0000 | 1.0000 |
| Single-path-Loop | 0.7340 | 0.5998 | 0.7000 |
| Multi-path-Loop | 0.5780 | 0.5000 | 0.5553 |
| Nested-Loop | 0.5130 | 0.4875 | 0.4702 |
| Overall | 0.6079 | 0.5319 | 0.5419 |

The ratios are computed as `slice/original`. Lower values indicate stronger reduction.

### RQ2: Verification-Cost Reduction

RQ2 evaluates whether FSF-guided slicing reduces the cost of TBFV.

| Category | Dynamic Execution Ratio | Path Derivation Ratio | SMT Solving Ratio | Total Time Ratio |
|---|---:|---:|---:|---:|
| Branched | 0.653 | 0.721 | 0.660 | 0.682 |
| Sequential | 0.943 | 0.982 | 0.964 | 0.971 |
| Single-path-Loop | 0.893 | 0.849 | 0.863 | 0.874 |
| Multi-path-Loop | 0.742 | 0.750 | 0.745 | 0.746 |
| Nested-Loop | 0.865 | 0.806 | 0.702 | 0.794 |
| Overall | 0.767 | 0.795 | 0.750 | 0.775 |

The overall total-time ratio is **0.775**, corresponding to a **22.5% reduction** in the total TBFV cost.

### RQ3: Verification-Result Preservation

RQ3 evaluates whether the verification results are preserved after applying FSF-guided slicing.

| Category | Tasks | Comparable Tasks | Inconclusive Tasks | Soundness Agreement | Completeness Agreement |
|---|---:|---:|---:|---:|---:|
| Branched | 339 | 333 | 6 | 100% | 100% |
| Sequential | 137 | 133 | 4 | 100% | 100% |
| Single-path-Loop | 57 | 53 | 4 | 100% | 100% |
| Multi-path-Loop | 104 | 104 | 0 | 100% | 100% |
| Nested-Loop | 103 | 95 | 8 | 100% | 100% |
| Overall | 740 | 718 | 22 | 100% | 100% |

A task is regarded as comparable only when both the original program and the corresponding slice produce definite TBFV results. Inconclusive tasks are not used in the agreement calculation.

## Tool Overview

The executable prototype is located in `tool/`. See `tool/README.md` for the detailed tool manual.

The tool supports the following workflow:

```text
Java program + FSF specification
            |
            v
Validate FSF syntax and scenario constraints
            |
            v
Build CFG/PDG and identify scenario-relevant dependencies
            |
            v
Construct FSF-guided executable slices
            |
            v
Run TBFV on the original program and generated slices
            |
            v
Report scale reduction, verification cost, and result preservation
```

## Requirements

For the prototype tool:

- Python 3.10+
- Java/JDK 17+
- macOS, Linux, or Windows

The main Python dependencies are listed in `tool/requirements.txt` and `tool/pyproject.toml`:

- `javalang`
- `PyYAML`
- `z3-solver`

## Installation

From the repository root, enter the tool directory:

```bash
cd tool
```

On macOS or Linux:

```bash
./install.sh
.venv/bin/fsf-tbfv doctor
```

On Windows PowerShell:

```powershell
./install.ps1
.venv/Scripts/fsf-tbfv.exe doctor
```

Manual installation is also supported:

```bash
cd tool
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/fsf-tbfv doctor
```

## Quick Start

Run the full workflow on the cube-sum example:

```bash
cd tool
.venv/bin/fsf-tbfv analyze \
  --java examples/UserInputProgram.java \
  --fsf examples/cube_sum.fsf.yaml \
  --output demo-output
```

Run the calculator example:

```bash
cd tool
.venv/bin/fsf-tbfv analyze \
  --java examples/Calculator.java \
  --fsf examples/calculator.fsf.yaml \
  --output calculator-output
```

The output directory contains JSON/HTML reports and generated Java slices, for example:

```text
demo-output/
├── report.json
├── report.html
└── slices/
```

## Main Commands

The prototype provides the following command-line interface:

```text
doctor          Check Python, Z3, javalang, and javac.
init-fsf        Generate an editable FSF YAML scaffold from a Java method.
validate-fsf    Validate FSF syntax, variables, exclusivity, and input-domain coverage.
slice           Run FSF-guided slicing and compile generated slices.
verify          Run TBFV on a given program and FSF specification.
analyze         Run the full pipeline: validation, slicing, TBFV, comparison, and report generation.
dataset-check   Scan a Java dataset and report parseable files and failure reasons.
suggest-fsf     Optionally draft an FSF with an LLM; formal validation remains local.
```

Inspect the bundled dataset:

```bash
cd tool
.venv/bin/fsf-tbfv dataset-check \
  --java-dir datasets/PCaE-Dataset \
  --output dataset-check.json
```

Run tests for the prototype:

```bash
cd tool
.venv/bin/python -m pip install pytest
.venv/bin/python -m pytest
```

## FSF Specification Format

An FSF file is written in YAML. A minimal example is shown below.

```yaml
method: calculate
inputs:
  num1: {type: int, min: -20, max: 20}
  num2: {type: int, min: -20, max: 20}
  operator: {type: char, min: 37, max: 47}
outputs:
  return_value: {type: int, source: return}
scenarios:
  - id: T_div
    T: "operator == '/' && num2 != 0"
    D: "return_value == num1 / num2"
analysis:
  max_paths: 128
  max_loop_iterations: 128
  solver_timeout_ms: 10000
  compare_original: true
  compile_slices: true
```

For the full FSF format, see `tool/docs/FSF_FORMAT.md`.

## Documentation

Additional documentation is available under `tool/docs/`:

| File | Description |
|---|---|
| `tool/docs/ALGORITHM.md` | Mapping between the paper algorithm and the implementation. |
| `tool/docs/FSF_FORMAT.md` | FSF YAML field reference and expression format. |
| `tool/docs/REPRODUCTION_NOTES.md` | Reproduction notes, boundaries, and material audit. |

## Reproduction Notes

The CSV files under `Experimental-results/` provide the task-level and category-level data used for the reported RQ1, RQ2, and RQ3 results. The prototype under `tool/` can be used to run FSF-guided slicing and TBFV on the included examples and supported Java programs.

The current implementation targets the scalar Java subset used in the experiment. Complex data structures, object graphs, recursion, interprocedural symbolic execution, string semantics, and complex library calls are not fully supported and may produce inconclusive results.

The root-level `Makefile` and `.github/workflows/validate-preview.yml` are legacy preview files and are not required for running the current prototype. The recommended workflow is to use the commands under `tool/` described above.

## License

The prototype tool is released under the MIT License. See `tool/LICENSE`.

## Citation

Please cite the accompanying manuscript if you use this artifact:

```bibtex
@article{FSFSlicerTBFV,
  title   = {FSF-Guided Program Slicing for Testing-Based Formal Verification of Functional Soundness and Completeness},
  author  = {Anonymous},
  journal = {Under Review},
  year    = {2026}
}
```
