# Preview Validation Rules

Run:

```bash
python3 scripts/validate_preview.py
```

The validator rejects the preview unless all of the following conditions hold.

## Identity and coverage

- Program and task identifiers are unique.
- Every task references a known program.
- Program counts are 100, 63, 21, 31, and 35 by category.
- Task counts are 339, 137, 57, 104, and 103 by category.
- Each program's declared scenario count matches its task rows.

## RQ1

- Every scale row is marked `SYNTHETIC_ILLUSTRATIVE`.
- Slice metrics are positive and do not exceed original metrics.
- Stored ratios equal the corresponding slice/original quotient.
- Original metrics remain constant across scenarios of the same program.
- Category means round to the values transcribed from Table 2.
- The task-weighted overall means round to 0.6079, 0.5319, and 0.5419.

## RQ2

- Every task has repetitions 1 through 10 exactly once.
- Stored phase ratios equal the corresponding slice/original quotient.
- Original total time equals dynamic, path-derivation, SMT, and other time.
- Slice total time equals dynamic, path-derivation, SMT, slicing, and other time.
- Category and task-weighted overall ratios round to Table 3.

## RQ3

- Original and slice availability always match.
- All 718 definite pairs have identical soundness and completeness judgments.
- All 22 inconclusive pairs have a non-empty illustrative reason code.
- Category availability counts and the 97.03% overall conclusive rate match Table 4.

## Provenance guard

- Metadata declares `empirical=false`.
- Every generated CSV row carries the synthetic status marker.
- Reported summary files carry explicit manuscript-table source labels.

