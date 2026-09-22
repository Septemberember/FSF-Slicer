# Reproducibility and Experimental Configuration

This document specifies the environment and execution protocol for the public FSF-Slicer implementation in [`tool/`](tool/), including hardware, random seeds, input bounds, stopping rules, and scenario validation. The implementation examined is commit [`5787bbd0adba5e014d0e68ea1e18b572aab41a6c`](https://github.com/Septemberember/FSF-Slicer/tree/5787bbd0adba5e014d0e68ea1e18b572aab41a6c); its provenance is described in the [reproduction notes](tool/docs/REPRODUCTION_NOTES.md). The archived study contains [250 program records](Experimental-results/program_manifest.csv) and [740 task records](Experimental-results/task_manifest.csv). The reference execution checks below concern the public implementation and are separate from those archived experimental measurements.

## 1. Hardware and software environment

The laptop configuration was measured on the host used to validate the documented commands. The Linux configuration is a suggested allocation for an independent reproduction run, rather than a record of the server used for the archived experiments.

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

The public tool implements PDG construction in a custom intraprocedural analysis module using javalang as its parsing front end. Java is used to compile the reconstructed slices; concrete and symbolic path execution are implemented by the public tool. Dependency constraints are provided in [`tool/requirements.txt`](tool/requirements.txt). For timing comparisons, run tasks sequentially on the same host and retain the actual CPU allocation, memory, operating system, runtime versions, and dependency versions with the results. The two hardware profiles above are not interchangeable timing baselines.

## 2. Random seeds and test selection

The public TBFV engine selects concrete inputs from satisfying Z3 models. It does not use an application-level random sampler. Its solver configuration sets a timeout and retains the Z3 4.12.2 defaults, including `smt.random_seed = 0` and `sat.random_seed = 0`.

The reproduction commands below set `PYTHONHASHSEED=0` before starting Python to fix hash randomization. This setting is distinct from the SMT solver seeds. Keep the source revision, dependency versions, variable declarations, scenario order, and analysis settings fixed between paired runs. Each generated input and its path condition are retained in `report.json`, allowing the actual test sequence to be inspected even when solver model selection differs across environments.

## 3. Input bounds and iterative test generation

Before execution, specify inclusive `min` and `max` bounds for each numeric input in the FSF YAML file. Let `B` denote the conjunction of these bounds. For a functional scenario `(T,D)`, the first test case satisfies `B ∧ T`. After exploring paths with conditions `C1, ..., Ck`, the next test case is obtained by solving:

```text
B ∧ T ∧ ¬C1 ∧ ... ∧ ¬Ck
```

The input bounds remain fixed throughout the run. Each completed execution supplies a path condition and an output state representation. Testing covers the specified scenario domain when the completed path conditions cover all inputs satisfying `B ∧ T`; individual input values need not be enumerated. Verification conclusions are relative to this bounded domain.

The supplied examples contain explicit bounds:

| FSF file | Input bounds | Maximum paths | Loop-iteration budget |
|---|---|---:|---:|
| [`cube_sum.fsf.yaml`](tool/examples/cube_sum.fsf.yaml) | `x ∈ [-20,100]` | 32 | 16 |
| [`calculator.fsf.yaml`](tool/examples/calculator.fsf.yaml) | `num1,num2 ∈ [-20,20]`; character codes for `operator ∈ [37,47]` | 32 | 64 |

For reproducible runs, retain the complete FSF file, including any output bounds used by the completeness check. When an input bound is omitted, the implementation uses `[-100,100]` for `int`, `long`, `float`, and `double`; the fallback ranges for `byte`, `short`, and `char` are `[-128,127]`, `[-32768,32767]`, and `[0,65535]`, respectively. Boolean inputs range over both truth values. Explicit per-input bounds take precedence over these defaults.

## 4. Stopping rules

The default analysis settings are defined in [`AnalysisConfig`](tool/fsf_tool/models.py); individual FSF files may override them.

| Setting | Default | Meaning |
|---|---:|---|
| `max_paths` | 128 | Maximum test-generation iterations per scenario and program |
| `max_loop_iterations` | 128 | Total loop-iteration budget per concrete execution, including nested loops |
| `solver_timeout_ms` | 10000 | Timeout for each SMT query |
| `compile_slices` | `true` | Compile each reconstructed Java slice |
| `compare_original` | `true` | Analyze the original program and its slice with the same specification and limits |

Test generation terminates normally when the remaining input constraint is unsatisfiable. It also stops when the path budget is exhausted, the solver does not return a definite satisfiability result, or a repeated symbolic path is detected. Exceeding the loop budget truncates the affected execution. The coverage check uses completed, supported paths; a truncated execution does not establish coverage of its input region.

Coverage, functional soundness, and functional completeness are reported separately. Reaching a resource limit does not establish a global verification result. Local results, inconclusive outcomes, exceptions, and solver diagnostics are retained in the report; definitive judgments require the corresponding verification obligations to be established.

## 5. Scenario-validation procedure

Before slicing or verification, the standard pipeline parses the Java method and the FSF file and performs the checks implemented in [`validation.py`](tool/fsf_tool/validation.py):

1. Check the selected method, input names and types, return-output type, expression syntax, and declared variables. The testing condition may reference only inputs, and the defining condition must reference at least one configured output.
2. Check satisfiability of each testing condition within the input bounds and detect overlap between testing conditions. An unsatisfiable condition or a detected overlap is a validation error.
3. Check whether the scenario family covers the bounded input domain and examine overlap between defining conditions with matching output-variable sets. Coverage gaps and detected defining-condition overlaps are reported as warnings.

Validation errors block the standard analysis pipeline. Warnings remain visible in the validation output and final report. Review the intended input/output relation, boundary cases, and diagnostics before freezing each Java/FSF pair; automated admissibility checks do not establish that the specification expresses the intended requirement. Use the normal pipeline without `--force` for reproduction, and preserve validation failures as recorded outcomes.

## 6. Reproduction commands and retained records

With Python 3.12.14 and the JDK available, the following commands install the dependencies and run the supplied calculator example:

```bash
git clone https://github.com/Septemberember/FSF-Slicer.git
cd FSF-Slicer
git checkout 5787bbd0adba5e014d0e68ea1e18b572aab41a6c
python3.12 -m venv .venv
.venv/bin/python -m pip install -r tool/requirements.txt 'PyYAML==6.0.3'
export PYTHONHASHSEED=0
mkdir -p reproduction
git rev-parse HEAD > reproduction/revision.txt
java -version 2> reproduction/java-version.txt
.venv/bin/python -m pip freeze > reproduction/dependencies.txt
cd tool
../.venv/bin/python -m fsf_tool doctor > ../reproduction/runtime.json
../.venv/bin/python -m fsf_tool validate-fsf \
  --java examples/Calculator.java \
  --fsf examples/calculator.fsf.yaml \
  > ../reproduction/validation.json
../.venv/bin/python -m fsf_tool analyze \
  --java examples/Calculator.java \
  --fsf examples/calculator.fsf.yaml \
  --output ../reproduction/calculator
```

Retain the exact Java source and FSF YAML, environment record, validation diagnostics, generated slices, and JSON/HTML reports together. The JSON report records input declarations, execution limits, generated tests, path conditions, output state representations, compilation outcomes, coverage, judgments, and elapsed verification time.

For repeated timing studies, use ten sequential repetitions per task, hold the environment and analysis settings fixed, and retain every run before computing averages. The archived [`rq2_timing_runs.csv`](Experimental-results/rq2_timing_runs.csv) contains ten records per task. For result-preservation analysis, compare only tasks for which both the original program and its slice produce definitive judgments, and report the remaining outcomes separately.

On 22 September 2026, the calculator validation and analysis commands were checked on the laptop configuration above with `PYTHONHASHSEED=0`. All five scenario slices compiled, and the original and sliced programs produced matching soundness and completeness judgments with complete scenario input coverage. Scenario-family warnings were retained in the validation report. These checks validate the documented execution procedure.
