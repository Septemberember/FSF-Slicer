# Reproducibility and Experimental Configuration

This document describes the hardware and software environment, random seeds, input bounds, stopping rules, and scenario-validation procedure for reproducing FSF-Slicer runs.

## 1. Hardware and software environment

The following table lists the validated laptop environment and a suggested Linux configuration for reproduction.

| Component | Validated laptop environment | Suggested Linux reproduction environment |
|---|---|---|
| Processor | Apple M5 Pro, ARM64 | Intel or AMD processor, x86-64 |
| CPU allocation | 18 physical cores | 8 dedicated CPU cores |
| Memory | 64 GiB | 32 GiB |
| Operating system | macOS 26.3.2, build 25D2150 | Ubuntu 26.04 LTS |
| Python | 3.12.14 | 3.12.14 |
| Java | OpenJDK 26, build 26+35-2893 | OpenJDK 26 |
| Java parser | javalang 0.13.0 | javalang 0.13.0 |
| SMT solver package | z3-solver 4.12.2.0 | z3-solver 4.12.2.0 |
| YAML parser | PyYAML 6.0.3 | PyYAML 6.0.3 |

The implementation in [`tool/`](tool/) constructs the PDG using a custom intraprocedural analysis module with javalang as the parsing front end. The JDK compiles generated slices. Dependencies are specified in [`tool/requirements.txt`](tool/requirements.txt). Timing comparisons require sequential execution on the same host with fixed software versions and resource allocation.

## 2. Random seeds and test selection

Test inputs are obtained from satisfying Z3 models without application-level random sampling. The implementation retains the Z3 4.12.2 default seeds, `smt.random_seed = 0` and `sat.random_seed = 0`. Set `PYTHONHASHSEED=0` before execution and keep the source revision, scenario order, and analysis settings fixed. Generated inputs and path conditions are recorded in `report.json`.

## 3. Input bounds and iterative test generation

For this reproduction protocol, set numeric input bounds to the inclusive interval `[-500, +500]` in the FSF YAML file, restricted to values representable by the declared Java type. Boolean and character inputs retain their declared logical and character domains. Let `B` denote the conjunction of the input-domain constraints. For a functional scenario `(T,D)`, the first test case satisfies `B ∧ T`. After exploring completed paths with conditions `C1, ..., Ck`, generate the next test case by solving:

```text
B ∧ T ∧ ¬C1 ∧ ... ∧ ¬Ck
```

The bounds remain fixed throughout execution. Each test produces a path condition and an output state representation. Scenario coverage is established when the completed path conditions cover all inputs satisfying `B ∧ T`. Verification judgments apply to this bounded domain. Retain the complete FSF file, including input bounds and any output bounds used for functional completeness.

## 4. Stopping rules

The defaults in [`AnalysisConfig`](tool/fsf_tool/models.py) are listed below. Record any overrides in the FSF file.

| Setting | Default | Meaning |
|---|---:|---|
| `max_paths` | 128 | Maximum test-generation iterations per scenario and program |
| `max_loop_iterations` | 128 | Total loop-iteration budget per concrete execution, including nested loops |
| `solver_timeout_ms` | 10000 | Timeout for each SMT query |
| `compile_slices` | `true` | Compile each reconstructed Java slice |
| `compare_original` | `true` | Analyze the original program and its slice with the same specification and limits |

Test generation terminates when the remaining input constraint is unsatisfiable, the path budget is exhausted, the solver returns an inconclusive result, or a repeated symbolic path is detected. Exceeding the loop budget truncates the affected execution. Only completed, supported paths contribute to coverage. Coverage, functional soundness, and functional completeness are reported separately; definitive judgments require the corresponding verification obligations to be established.

## 5. Scenario-validation procedure

Before slicing and verification, [`validation.py`](tool/fsf_tool/validation.py) performs the following checks:

1. Check method selection, variable declarations and types, and expression syntax. The testing condition `T` may reference only inputs, and the defining condition `D` must reference at least one configured output.
2. Check satisfiability and pairwise exclusivity of testing conditions within the input bounds. Unsatisfiable or overlapping testing conditions are validation errors.
3. Check input-domain coverage by the scenario family and overlap between defining conditions with matching output-variable sets. Detected coverage gaps and defining-condition overlaps are reported as warnings.

Validation errors block analysis. Review the intended input/output relation, boundary cases, and validation diagnostics before finalizing each Java/FSF pair. Retain errors and warnings with the results and run the standard pipeline without `--force`.

## 6. Reproduction commands and retained records

The following commands use a fixed source revision and run the calculator example with both numeric inputs bounded by `[-500, +500]`:

```bash
git clone https://github.com/Septemberember/FSF-Slicer.git
cd FSF-Slicer
git checkout 5787bbd0adba5e014d0e68ea1e18b572aab41a6c
python3.12 -m venv .venv
.venv/bin/python -m pip install -r tool/requirements.txt 'PyYAML==6.0.3'
export PYTHONHASHSEED=0
mkdir -p reproduction
.venv/bin/python - <<'PY'
from pathlib import Path
import yaml

spec = yaml.safe_load(Path("tool/examples/calculator.fsf.yaml").read_text())
for name in ("num1", "num2"):
    spec["inputs"][name].update(min=-500, max=500)
Path("reproduction/calculator.fsf.yaml").write_text(
    yaml.safe_dump(spec, sort_keys=False), encoding="utf-8"
)
PY
git rev-parse HEAD > reproduction/revision.txt
java -version 2> reproduction/java-version.txt
.venv/bin/python -m pip freeze > reproduction/dependencies.txt
cd tool
../.venv/bin/python -m fsf_tool doctor > ../reproduction/runtime.json
../.venv/bin/python -m fsf_tool validate-fsf \
  --java examples/Calculator.java \
  --fsf ../reproduction/calculator.fsf.yaml \
  > ../reproduction/validation.json
../.venv/bin/python -m fsf_tool analyze \
  --java examples/Calculator.java \
  --fsf ../reproduction/calculator.fsf.yaml \
  --output ../reproduction/calculator
```

Retain the Java source, FSF YAML, environment record, validation diagnostics, generated slices, and JSON/HTML reports. For timing comparisons, perform ten sequential repetitions per task under fixed settings and retain individual measurements before averaging. For result-preservation analysis, calculate agreement over tasks with definitive judgments for both the original program and its slice, and report inconclusive outcomes separately.

## 7. Sampling, paired comparisons, and confidence intervals

### Sampling units and task selection

The analysis set contains 250 programs and 740 scenario-specific tasks across five control-flow categories. The [program manifest](Experimental-results/program_manifest.csv) records categories and scenario counts, and the [task manifest](Experimental-results/task_manifest.csv) links each task to its program. A program–scenario pair is the evaluation unit; scenarios from the same program and repeated runs of the same task are dependent observations. Use a fixed task set for paired comparisons and report exclusions by reason. Interpret results within this benchmark's structural coverage.

### Paired measurements and aggregation

Match original-program and slice measurements by `program_id`, `task_id`, and `repetition`, using identical specifications, input bounds, and analysis settings. For each timing metric, average the ten repetitions separately for the original program and its slice, then calculate the task-level slice/original ratio and the paired difference in milliseconds. Report absolute times and within-task standard deviations alongside ratios. Category and overall estimates are arithmetic means of task-level values, so overall estimates weight categories by their task counts. Comparisons between slicing methods use the same eligible tasks and metric definitions.

### Confidence-interval procedure

Estimate 95% confidence intervals using 2,000 program-cluster bootstrap resamples with bootstrap seed `0`. Sample program identifiers with replacement, retaining all associated scenarios, repetitions, and paired measurements. Recompute the task-weighted estimate in each resample and take the 2.5th and 97.5th percentiles as interval endpoints. For method comparisons, bootstrap the paired differences using identical sampled programs for both methods. This [cluster-bootstrap procedure](https://doi.org/10.1111/j.1467-9868.2007.00593.x) accounts for multiple scenarios from the same program; where related variants are identified, additionally assess sensitivity to clustering by program family.

### Records and analysis support

The published [RQ1 records](Experimental-results/rq1_scale.csv), [RQ2 repeated measurements](Experimental-results/rq2_timing_runs.csv), and [RQ3 judgments](Experimental-results/rq3_preservation.csv) retain task identifiers for paired reanalysis. The [`cluster_interval` function](Tool/fsf_tool/benchmark.py) provides program-cluster bootstrap support for task-level metric rows grouped by `program_id`; [reproduction notes](Tool/docs/REPRODUCTION_NOTES.md) describe repeated-run exports. Retain the source revision, eligible task identifiers, exclusions, bootstrap seed, point estimates, and interval endpoints with each statistical summary.
