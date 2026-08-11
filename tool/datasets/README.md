# Bundled dataset

`PCaE-Dataset/` is the dataset supplied with the reproduction request. It is included unchanged and retains its original ownership/licensing status.

Inventory:

| Category | Java files |
|---|---:|
| Branched3 | 151 |
| Sequential3 | 63 |
| Single-path-Loop3 | 21 |
| Multi-path-Loop3 | 31 |
| Nested-Loop3 | 35 |
| Total | 301 |

Run `fsf-tbfv dataset-check --java-dir datasets/PCaE-Dataset` before batch work. One supplied mutant, `Branched3/PassPillowBranch_Mutant2.java`, is syntactically incomplete because its class-closing brace is absent. The tool reports it and does not silently repair benchmark inputs.

