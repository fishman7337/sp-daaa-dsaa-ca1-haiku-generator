# Contributing

Thank you for improving HaikuForge AI. Keep changes small, clear, and easy to
review.

## Development Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

## Before Submitting Changes

Run the same checks used by CI:

```powershell
python -m ruff format .
python -m ruff check .
python -m pytest
python -m bandit -c pyproject.toml -r src
```

## Style Guide

- Follow PEP 8 for code style.
- Use Google-style docstrings for public modules, classes, and functions.
- Prefer `pathlib.Path` for filesystem work.
- Keep comments useful and specific; avoid comments that simply repeat the code.
- Add tests for new behaviour or bug fixes.

## Pull Request Checklist

- The change has a clear purpose.
- Tests have been added or updated where useful.
- Documentation is updated when behaviour, setup, or data paths change.
- Generated caches and local environment files are not committed.
