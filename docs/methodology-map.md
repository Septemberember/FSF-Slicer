# Methodology-to-Artifact Map

| Manuscript concept | Planned artifact location | Preview status |
|---|---|---|
| Java input program | `benchmarks/<category>/<program_id>/original.java` | Missing |
| Functional scenario \((T_i,D_i)\) | `benchmarks/<category>/<program_id>/fsf.yaml` | Synthetic manifest only |
| Executable scenario slice | `benchmarks/<category>/<program_id>/slices/<scenario_id>.java` | Missing |
| CFG and PDG construction | Java tool source | Interface contract only |
| Scenario core and dependence closure | Java tool source | Interface contract only |
| Testing-condition pruning | Java tool source | Interface contract only |
| TBFV execution and verification | Java and Python tool source | Interface contract only |
| RQ1 task measurements | `results/rq1_scale.csv` | Synthetic schema preview |
| RQ2 repeated timings | `results/rq2_timing_runs.csv` | Synthetic schema preview |
| RQ3 paired judgments | `results/rq3_preservation.csv` | Synthetic schema preview |
| Tables 2-4 | `data/paper-reported/` | Included as reported aggregates |

