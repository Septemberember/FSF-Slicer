# Synthetic Data

Every record in this directory is generated for schema review and validator testing. These files are not measurements from the manuscript experiment.

The static metric magnitudes are deliberately high numerical fixtures so that integer-valued slice metrics can be tuned at the manuscript's displayed precision. They are not intended to resemble the size distribution of the evaluated programs.

Each CSV includes a `data_status` field whose required value is `SYNTHETIC_ILLUSTRATIVE`. The metadata file also records the fixed generator seed and a non-empirical provenance statement.

Regenerate the files with:

```bash
python3 scripts/generate_synthetic_preview.py
```

Validate them with:

```bash
python3 scripts/validate_preview.py
```

Do not overwrite these records with partial empirical data. Replace the directory atomically only when the complete 250-program, 740-task artifact is available.
