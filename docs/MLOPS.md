# MLOps Notes

## Scope

The project uses a lightweight Markov chain rather than a trained neural model.
MLOps is therefore focused on reproducible data handling, deterministic tests,
quality gates, and transparent model limitations.

## Lifecycle

1. Data is stored as versioned text and WAV assets under `data/`.
2. The Markov model is trained in memory from selected haiku lines.
3. Generated output can be saved into user-selected output folders.
4. Tests verify tokenisation, thesaurus loading, Markov behaviour, and audio stitching.
5. CI runs formatting, linting, compilation, pytest, security scanning, and dependency audits.

## Reproducibility

- Runtime dependencies are declared in `pyproject.toml`.
- Development dependencies are installed through `requirements-dev.txt`.
- Tests seed randomness where deterministic behaviour matters.
- The Markov model has no persisted binary model artifact.

## Monitoring and Evaluation

For this coursework scale, evaluation is local:

- Functional tests for expected transformations.
- Manual review of generated haiku quality.
- Security scans for unsafe Python patterns and vulnerable dependencies.
- Documentation review for academic attribution and setup clarity.

## Risks and Mitigations

- Random generation may produce awkward lines: keep the model card honest and test structural behaviour.
- Unknown syllable counts require user input: cache values in memory during the session.
- Missing audio clips reduce narration completeness: report missing words and continue safely.
- Coursework reuse may create academic integrity concerns: preserve attribution and context.
