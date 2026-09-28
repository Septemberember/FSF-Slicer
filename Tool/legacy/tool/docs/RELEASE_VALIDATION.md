# Release validation - 2026-08-11

Environment used for release QA:

- Python 3.12.13
- Z3 4.12.2
- javalang 0.13.0
- OpenJDK/javac 26
- clean virtual environment installed from `pyproject.toml`

Checks:

- `pip check`: no broken requirements.
- Python compile check: passed for all `fsf_tool` modules.
- Automated tests: 6 passed.
- Reference PDF copy SHA-256: `637272ba52b5ff178ecf9303cb9f92cee249b7db38e5c38192b8483fab11e92c`, identical to the supplied PDF.
- Python wheel SHA-256: `7b973d14c746df3fdcdfa2c7449d8ef71c8d0dd24dce2d41e39a7df149f27f8e`.
- Secret-pattern scan: no API key found.
- Dataset scan: 301 total, 300 parsed, 1 source-invalid mutant reported.

End-to-end outcomes:

| Program | Scenarios | Paths | Slice compilation | Soundness | Completeness |
|---|---:|---:|---|---|---|
| Paper calculator example | 5 | 5 | 5/5 | sound (all) | complete (all) |
| Paper cube-sum loop example | 2 | 5 | 2/2 | sound (all) | complete (all) |
| PCaE FizzBuzz original | 4 | 4 | 4/4 | sound (all) | complete (all) |
| PCaE repeated-addition multiply | 2 | 11 | 2/2 | sound (all) | complete (all) |

Every end-to-end run compared the original program and generated slice under the same scenario/domain configuration.
