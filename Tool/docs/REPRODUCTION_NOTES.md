# Reproducibility

## Environment

Install the tested dependency versions with `python -m pip install -r requirements-lock.txt`, then install this directory with `python -m pip install --no-deps .`. `fsf-tbfv doctor` records Python, Z3, parser, compiler, OS, architecture, and CPU count. Analysis reports additionally record effective domains, all analysis settings, specification metadata, and SHA-256 identities for source and specification.

`random_seed` configures Z3 model selection. Models are solver-selected, not a uniform random sample. Keep the solver, dependencies, platform, seed, input bounds, path limit, loop limit, and timeout identical for paired comparisons.

## Replicate the bundled validation

```sh
python -m pytest
python -m fsf_tool dataset-check --java-dir datasets/PCaE-Dataset --output dataset-check.json
python -m fsf_tool benchmark --manifest examples/benchmark.yaml \
  --repeats 2 --seed 2026 --modes fsf,backward,conditioned \
  --output benchmark-output
```

For a larger repeated study, use `--repeats 10`. The manifest explicitly maps a program ID, Java file, and FSF file. Multiple tasks for the same Java program must share `program_id` so the statistical unit is not split incorrectly. Manifest paths are relative to the manifest file.

Each task writes its effective specification, original/slice reports, generated Java source, graph exports, and compiler diagnostics. Failed tasks are listed separately and cause the benchmark CLI to exit with code 2. Unsupported analysis outcomes remain explicit result rows and are never counted as definite agreement.

## Measurements

`runs.csv` has one row per scenario, mode, and repetition. Original and sliced verification use identical settings. `paired_verify_delta_ms` is sliced minus original verification time. `amortized_slice_total_ms` includes slicing and an equal share of the one-time dependence graph construction for the scenario family. `pipeline_ms` measures the complete family run, including validation, compilation, comparisons, and report preparation; it is repeated on each scenario row and must not be summed over those rows.

Metric ratios are slice/original. The summarizer reports scenario-weighted means and percentile 95% intervals from 2,000 program-cluster bootstrap draws. Each draw samples complete programs with replacement and retains all their scenarios and repetitions. A single-program result has no confidence interval. These intervals describe the supplied workload and account for its within-program clustering; they do not establish external validity for other program populations.

The `fsf`, `backward`, and `conditioned` modes use the same parser, semantic model, compiler, and verifier. Safe dependence closure may produce identical FSF and conditioned slices. Timing differences can include warm-up, solver behavior, and system load; a release does not guarantee a speedup on every program.

## Evidence boundaries

The bundled dataset contains Java sources, not a complete validated FSF mapping for every source. The provided benchmark manifest covers four programs and sixteen scenarios. No missing specifications, hardware measurements, or historical experimental records are synthesized. The paper's 250-program/740-scenario results remain separate from the release validation.

Source/FSF agreement checks use the same analysis implementation. The JVM differential tests separately check arithmetic edge cases and representative execution/control-flow behavior against compiled Java. Neither finite differential tests nor matching verification labels alone constitute a general preservation theorem.

The repository contains both `Tool` and `tool`. Use a case-sensitive checkout if checking out the entire repository. Alternatively, download/extract only `Tool` or the release archive. Publication preserves the original `tool` Git tree exactly.
