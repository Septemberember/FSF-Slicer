# FSF-Slicer-TBFV

This project is an independent, executable reproduction of the paper **FSF-Guided Program Slicing for Testing-Based Formal Verification of Functional Soundness and Completeness**. The tool accepts a Java source file and a Functional Scenario Form (FSF) specification as input, generates an executable Java slice for each scenario, and evaluates functional soundness and functional completeness according to the TBFV workflow described in the paper.

The project runs entirely offline by default: Java parsing, PDG construction, program slicing, test generation, symbolic path derivation, and Z3 verification are all performed locally. An LLM is used only by the optional `suggest-fsf` drafting command; it does not participate in the final formal judgments, and the tool never stores API keys.

## Implemented Capabilities

- Java method parsing and validation of method names, parameters, and return types.
- FSF YAML parsing and strict pre-validation, including variable constraints, satisfiability of `T`, mutual exclusivity of testing conditions, input-domain coverage of the scenario family, output constraints in `D`, and overlap warnings.
- Conservative construction of control-flow and program dependence graphs, including parameters, DEF/USE sets, data dependencies, control dependencies, and output locations.
- FSF-guided slicing as described in the paper: `ForwardSlice(input) ∩ BackwardSlice(output)`, dependence closure, proof and pruning of unreachable branches under `T`, and Java source reconstruction.
- Invocation of `javac` for every generated slice, turning a syntactic slice into a compilation-validated executable slice.
- TBFV iteration: Z3 generates tests satisfying `T ∧ ¬C₁ ∧ ... ∧ ¬Cₖ`; concrete and symbolic execution proceed in parallel to record path condition `Cᵢ` and output state representation `y=fᵢ(x)`.
- Soundness judgment: `T ∧ Cᵢ ⇒ D(fᵢ(x)/y)`.
- Completeness judgment: `∃x(T ∧ D) ⇒ ∨ᵢ∃x(T ∧ Cᵢ ∧ y=fᵢ(x))`.
- Graded outcomes—`sound / locally_sound / unsound` and `complete / locally_complete / incomplete / inconclusive`—without presenting path or loop truncation as a global proof.
- Repeated verification of the original program and its slice under identical parameters, with preservation of judgments reported explicitly.
- JSON and HTML reports covering LOC, executable statement count, cyclomatic complexity, path count, path conditions, test data, counterexamples, and execution time.
- Optional FSF drafting through an OpenAI-compatible LLM. The `--allow-llm` flag is required explicitly, and the API key is read only from an environment variable.
- A bundled dataset inspection command. Of the 301 Java files in the supplied dataset, 300 can be parsed. The only failing file is itself missing the closing brace of its class, and `javac` rejects it as well.

## Requirements

- Python 3.10+
- Java/JDK 17+ (required only for compilation validation of generated slices)
- macOS, Linux, or Windows

The core dependencies are pinned in `requirements.txt`: `javalang`, `PyYAML`, and `z3-solver`.

## Installation

macOS / Linux:

```bash
./install.sh
.venv/bin/fsf-tbfv doctor
```

Windows PowerShell:

```powershell
./install.ps1
.venv/Scripts/fsf-tbfv.exe doctor
```

Manual installation is also supported:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
```

## Quick Start

Run the complete workflow—slicing, TBFV, comparison with the original program, and report generation:

```bash
.venv/bin/fsf-tbfv analyze \
  --java examples/UserInputProgram.java \
  --fsf examples/cube_sum.fsf.yaml \
  --output demo-output
```

The output includes:

```text
demo-output/
├── report.json
├── report.html
└── slices/
    ├── T_nonpositive/UserInputProgram.java
    └── T_positive/UserInputProgram.java
```

The calculator scenario from the paper is also included:

```bash
.venv/bin/fsf-tbfv analyze \
  --java examples/Calculator.java \
  --fsf examples/calculator.fsf.yaml \
  --output calculator-output
```

## Commands

```text
doctor          Check Python, Z3, javalang, and javac
init-fsf        Generate an editable FSF YAML scaffold from a Java method
validate-fsf    Validate FSF syntax, variables, exclusivity, and input-domain coverage
slice           Run only FSF-guided slicing and compile the generated slices
verify          Run only TBFV on the given program
analyze         Run the full pipeline: validation, slicing, compilation, TBFV,
                original/slice comparison, and report generation
dataset-check   Scan a Java dataset and list parseable files and failure reasons
suggest-fsf     Optionally draft an FSF with an LLM; formal validation remains local
```

Create an FSF scaffold for any Java file:

```bash
.venv/bin/fsf-tbfv init-fsf \
  --java datasets/PCaE-Dataset/Branched3/FizzBuzz_Original.java \
  --method fizzBuzz \
  --output fizzbuzz.fsf.yaml
```

Inspect the dataset:

```bash
.venv/bin/fsf-tbfv dataset-check \
  --java-dir datasets/PCaE-Dataset \
  --output dataset-check.json
```

## FSF File

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

Expressions use Java-style syntax: `&&`, `||`, `!`, comparisons, `+ - * / %`, bitwise operations, ternary expressions, and `Math.abs/min/max`. The `int` and `long` types use Java signed bit-vector semantics, including overflow and negative remainders. At the verification layer, `float` and `double` are modeled using exact real-number approximations; conclusions that depend on IEEE-754 NaN, Infinity, or rounding behavior should therefore be treated as model approximations.

Input `min/max` values define the analysis domain for the current TBFV run. The testing stage in the paper likewise requires a terminating testing condition—for example, narrowing `x>0` to `0<x<=500`. If no bounds are provided, the tool uses `[-100,100]` for numeric inputs by default. Output `min/max` values are not required for soundness, but they can define the output domain explicitly in completeness formulas involving overflow.

## Judgment Semantics

- `sound`: All inputs satisfying `T` are covered by complete paths, and every path satisfies `D`.
- `locally_sound`: Every explored path satisfies `D`, but the derived path conditions do not yet cover all of `T`.
- `unsound`: Z3 provides an input counterexample for which the program output violates `D`, or execution raises an exception not permitted by the scenario.
- `complete`: Every output permitted by `D` can be produced by at least one explored input satisfying `T`.
- `incomplete`: The paths cover all of `T`, but there is an output permitted by `D` that the program cannot reach.
- `locally_complete`: An uncovered output is found in the explored region, but a global `incomplete` judgment cannot be made because `T` has not been fully covered.
- `inconclusive`: A timeout occurs, or the current scalar Java model does not support the relevant syntax or invocation.

## Bounds and Trust Boundary

The advantage of TBFV is that it does not require manually supplied loop invariants; the trade-off is that it relies on test-induced paths. The tool strictly follows the paper's rule that global judgments may be issued only after complete path coverage:

- When `max_paths` or `max_loop_iterations` is reached, the report marks the result as partial/local or inconclusive.
- A Z3 result of `unknown` is never treated as `unsat`.
- Every generated slice is compiled with `javac`; complete compiler diagnostics are retained when compilation fails.
- By default, the original program and its slice are verified separately under the same FSF, input domain, path limit, and solver configuration.

The current executor targets the scalar Java subset used in the paper and PCaE dataset. It supports sequential code, branches, `switch`, `while`, `do-while`, conventional `for` loops, `break/continue/return/throw`, integer/real/Boolean/character values, and common `Math` functions. Arrays, collections, object graphs, recursion, interprocedural symbolic execution, string semantics, and complex library calls explicitly produce `inconclusive`; the slicer still performs conservative dependency analysis. The paper itself also identifies complex data structures, method invocations, and richer Java language features as directions for future extension.

## Optional LLM Integration

```bash
export FSF_LLM_API_KEY='...'
.venv/bin/fsf-tbfv suggest-fsf \
  --java MyProgram.java \
  --method targetMethod \
  --model your-model \
  --base-url https://api.example.com/v1 \
  --output MyProgram.fsf.yaml \
  --allow-llm
```

After generation, you must run `validate-fsf` or `analyze`. LLM output is not a proof; the judgments produced by Z3 and path verification are authoritative.

## Testing

```bash
.venv/bin/python -m pip install pytest
.venv/bin/python -m pytest
```

For a detailed mapping between the paper and the implementation, see `docs/ALGORITHM.md`. For the FSF field reference, see `docs/FSF_FORMAT.md`. For the material audit and reproduction boundaries, see `docs/REPRODUCTION_NOTES.md`.
