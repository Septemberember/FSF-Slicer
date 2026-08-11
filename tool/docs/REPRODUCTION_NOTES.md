# Reproduction notes

## Materials audited

- The supplied 25-page PDF and its LaTeX source were used as the algorithmic source of truth.
- The supplied `PCaE-main` project was inspected as a related SG4PM/PCaE prototype. It contains JavaParser-based instrumentation, test generation, an external Python/Z3 verifier, LLM-based FSF generation, and verifier-guided refinement. It does not contain the paper's FSF-guided slicer.
- The repository named by the paper's Data Availability section (`Septemberember/FSF-Slicer`) was empty at reproduction time, so no hidden implementation was assumed or copied.
- The supplied PCaE dataset contains 301 Java files across Branched, Sequential, Single-path-Loop, Multi-path-Loop, and Nested-Loop folders. `dataset-check` parses 300. `PassPillowBranch_Mutant2.java` lacks the final class brace and also fails `javac`.

## Design choices

- Python was chosen for a compact, auditable integration of Java parsing, Z3, slicing, concolic execution, reporting, and an optional OpenAI-compatible HTTP client.
- Integer expressions use signed Java bit-vector behavior. Real expressions are an exact-real abstraction of `float/double`.
- The PDG is deliberately conservative: it may keep extra definitions but should not delete a potential scalar dependency. This favors semantic preservation over the smallest possible slice.
- Branches are pruned only after an UNSAT proof under `T` and the configured domain.
- Global soundness/completeness words are reserved for complete path coverage. Limits and solver uncertainty propagate to local/inconclusive outcomes.

## Known scope

The automated executor targets scalar, single-method Java programs represented by the supplied benchmark. Complex arrays, object graphs, recursion, interprocedural calls, strings, collections, concurrency, reflection, and native/library effects require additional semantic models. Unsupported constructs are reported instead of guessed. The slicer remains useful as a conservative static reducer even when full TBFV is inconclusive.

