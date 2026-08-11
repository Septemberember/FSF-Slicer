# Data Dictionary

## Status convention

Every generated CSV row uses `data_status=SYNTHETIC_ILLUSTRATIVE`. This value is a publication guard, not an experimental variable.

## `program_manifest.csv`

| Field | Meaning |
|---|---|
| `program_id` | Stable synthetic program identifier. |
| `category` | One of the five structural categories used in the paper. |
| `category_ordinal` | One-based position within the category. |
| `scenario_count` | Number of synthetic scenarios assigned to the program. |
| `source_status` | Confirms that the row is only an identifier template. |
| `source_file` | `NOT_INCLUDED` because empirical benchmark code is unavailable. |

## `task_manifest.csv`

| Field | Meaning |
|---|---|
| `task_id` | Unique program/scenario identifier. |
| `scenario_index` | One-based scenario position within a program. |
| `testing_condition` | Illustrative \(T_i\) expression for schema review. |
| `defining_condition` | Illustrative \(D_i\) expression for schema review. |

## `rq1_scale.csv`

Each row represents one scenario-specific slicing task. Ratios are fractions computed as the slice metric divided by the original metric.

| Field family | Unit |
|---|---|
| `*_loc` | Physical lines of code. |
| `*_executable_statements` | Static executable-statement count. |
| `*_cyclomatic_complexity` | Cyclomatic-complexity count. |
| `*_ratio` | Dimensionless slice/original fraction. |

## `rq2_timing_runs.csv`

Each task has ten rows, one per synthetic repetition. All durations are milliseconds.

| Field family | Meaning |
|---|---|
| `*_dynamic_ms` | Dynamic execution and trace collection. |
| `*_path_derivation_ms` | Path-condition and state-representation derivation. |
| `*_smt_ms` | SMT solver time. |
| `original_other_ms` | Other original-program processing. |
| `slice_slicing_ms` | Slicing time included only in the slice total. |
| `slice_other_ms` | Other sliced-program processing and result generation. |
| `*_total_ms` | End-to-end time; slice total includes slicing. |
| `*_ratio` | Slice/original ratio for the named phase. |

## `rq3_preservation.csv`

| Field | Meaning |
|---|---|
| `*_availability` | `DEFINITE` or `INCONCLUSIVE`. |
| `*_soundness` | `SOUND`, `UNSOUND`, or `INCONCLUSIVE`. |
| `*_completeness` | `COMPLETE`, `INCOMPLETE`, or `INCONCLUSIVE`. |
| `*_agreement` | Agreement for definite pairs; otherwise `NOT_APPLICABLE`. |
| `inconclusive_reason` | Illustrative reason code for paired inconclusive records. |

## `data/paper-reported/`

These files transcribe category-level values from manuscript Tables 2-4. They are reported summaries, not values recomputed from actual task-level records. Keeping them separate prevents synthetic preview records from being mistaken for empirical provenance.

