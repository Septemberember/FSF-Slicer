# Third-party notices

FSF-Slicer's Python source is distributed under the MIT license in `LICENSE`. Dependencies are obtained from their upstream distributions; their licenses and notices remain applicable.

| Dependency | Version used | License |
|---|---|---|
| javalang | 0.13.0 | MIT |
| six | 1.17.0 | MIT |
| PyYAML | 6.0.2 | MIT |
| Z3 / z3-solver | 4.12.2.0 | MIT |
| setuptools | 80.10.2 | MIT |

The JDK is an external prerequisite and is not bundled. Its license depends on the distribution selected by the user.

`datasets/PCaE-Dataset` is retained byte-for-byte from the repository's existing `tool/datasets/PCaE-Dataset` subtree. Existing source notices and ownership remain applicable; this release does not relicense third-party dataset content. The tool's MIT license is not a substitute for a dataset author's own license.

The parser adaptation in `fsf_tool/java_parser.py` retains the upstream javalang MIT notice in `licenses/javalang.txt`.
