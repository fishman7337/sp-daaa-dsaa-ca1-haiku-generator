# HaikuForge AI

HaikuForge AI is a command-line haiku transformation, generation, and narration
application. It supports synonym replacement, shortest-synonym "zen" rewriting,
antonym replacement, batch permutation generation, simple Markov-based haiku
generation, and word-level WAV narration.

This project was prepared for Singapore Polytechnic, School of Computing,
Diploma in Applied AI & Analytics, module ST1507 Data Structure & Algorithm
(AI), CA1. It was completed by Goh Kun Ming, DAAA student, AY25/26 Year 2
Semester 1. Lecturer: Liu Zheng.

## Evidence and interpretation

| Evidence-backed measure | Current repository evidence |
| --- | --- |
| Poetic constraint | Generation targets the canonical **5–7–5** syllable structure. |
| Interaction modes | HaikuForge AI implements synonym, Zen, antonym, and batch transformations alongside Markov generation and WAV narration. |

The qualitative outcome is a layered CLI that combines data structures, constrained generation, transformation, and audio output. “HaikuForge AI” is the canonical product name; syllable correctness and runtime complexity are not presented as measured benchmarks.

## Features

- Transform haiku using synonym, antonym, and shortest-synonym thesaurus files.
- Generate every synonym permutation for a selected haiku through batch processing.
- Generate haiku-like text with a syllable-aware Markov chain.
- Narrate haiku using word-level WAV clips and optionally stitch clips into one WAV file.
- Run automated tests, linting, formatting checks, security scanning, and dependency audits.

## Project Structure

```text
.
|-- main.py                    # Compatibility launcher: python main.py
|-- pyproject.toml             # Package, test, lint, coverage, and security config
|-- src/haiku_forge/           # Application package
|-- tests/                     # Pytest suite
|-- data/
|   |-- samples/               # Sample haiku text files
|   |-- thesaurus/             # Synonym and antonym text files
|   `-- audio/                 # Word-level WAV clips
|-- outputs/                   # Generated artifacts retained for reference
|-- docs/                      # Architecture, MLOps, model, data, and testing docs
`-- .github/workflows/         # CI and security automation
```

## Quick Start

Use Python 3.11 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python main.py
```

After installation, the package entry point also works:

```powershell
haiku-forge
```

## Running Quality Checks

```powershell
python -m ruff format --check .
python -m ruff check .
python -m pytest
python -m bandit -c pyproject.toml -r src
python -m pip_audit . --skip-editable
```

## Data Format

Haiku files are plain UTF-8 text files with one haiku line per row.

Thesaurus files use one mapping per line:

```text
keyword: replacement one, replacement two, replacement three
```

Sample files live in `data/samples` and `data/thesaurus`. Audio clips live in
`data/audio` and are named after lowercase words, for example `sun.wav`.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [MLOps Notes](docs/MLOPS.md)
- [Model Card](docs/MODEL_CARD.md)
- [Data Card](docs/DATA_CARD.md)
- [Testing Guide](docs/TESTING.md)
- [Coursework Context](docs/COURSEWORK_CONTEXT.md)

## Academic Integrity

The repository keeps the original coursework context and supporting submission
PDFs under `docs/submission`. Any future reuse should preserve attribution and
comply with Singapore Polytechnic academic integrity requirements.

## Licensing

This repository currently does not declare a repository-wide software license.
Copyright therefore remains with the respective authors by default. Obtain
permission before copying, modifying, or redistributing the code, coursework,
datasets, audio, or other assets, and preserve all collaborator attribution.
