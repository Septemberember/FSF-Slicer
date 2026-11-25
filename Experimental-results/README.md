# Experimental Results for the Reconstructed Dataset

These files describe the dataset revision identified in [run_metadata.json](run_metadata.json).
The release contains **250 Java–FSF pairs and 740 scenarios**. The results come
from one local paired sweep with FSF-Slicer 2.0.1 on this release. Earlier
manuscript figures and ordinal task IDs have separate provenance.

## Mapping

- [program_manifest.csv](program_manifest.csv) identifies each Java file,
  FSF file, target method, scenario count, and SHA-256 hash.
- [task_manifest.csv](task_manifest.csv) records each indexed T/D pair and
  its program ID. All three task-level CSVs join on these IDs.

## Results

| File pair | Contents |
|---|---|
| [RQ1 tasks](rq1_scale.csv) and [summary](rq1_category_summary.csv) | Static metrics and mean task-level retention ratios over 583 compiled original/slice pairs. |
| [RQ2 tasks](rq2_timing_runs.csv) and [summary](rq2_category_summary.csv) | One attempt per task. Summary timing ratios use 541 pairs with definite judgments and average the individual task ratios. |
| [RQ3 tasks](rq3_preservation.csv) and [summary](rq3_category_summary.csv) | Original and sliced verification outcomes. There are 541 identical definite pairs, 38 pairs inconclusive on both sides, four mixed-availability pairs, and 157 tasks without paired results. |

RQ2 records original and sliced verifier times, graph construction, and slicing.
`preprocess_and_slice_verify_ms` sums sliced verification, graph construction,
and slicing. `pipeline_ms` is the combined analysis pipeline clock and has no
paired counterpart. The protocol excludes compilation and report generation from
the paired timing. One repetition supplies no within-task standard deviation.
The sweep did not measure separate dynamic-execution, path-derivation, or
SMT-solving phases and did not rerun Slicer4J or JavaSlicer.

All 740 attempts appear in each task-level CSV. Blank numeric or judgment fields
denote unavailable results. The 157 tasks without paired results comprise
117 native translation exclusions, 18 guards outside the configured bounds,
15 invalid or unsupported FSFs, and seven timeouts. RQ3 agreement describes the
tool's judgments on the bounded input domain. Independent behavioral comparison
was disabled for this sweep. Run parameters and source fingerprints are in
[run_metadata.json](run_metadata.json).
