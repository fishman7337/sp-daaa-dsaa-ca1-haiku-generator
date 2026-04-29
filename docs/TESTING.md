# Testing Guide

## Local Test Commands

```powershell
python -m ruff format --check .
python -m ruff check .
python -m compileall main.py src tests
python -m pytest
python -m bandit -c pyproject.toml -r src
python -m pip_audit . --skip-editable
```

## Test Coverage

The current pytest suite covers:

- File read/write and thesaurus parsing.
- Tokenisation and punctuation preservation.
- Haiku transformation and batch rendering helpers.
- Thesaurus synonym and antonym lookup.
- Markov model training and generation shape.
- Syllable dictionary lookup.
- WAV stitching with generated test audio.
- Basic prompt validation.

Interactive menu paths are intentionally thinner in automated tests because they
depend on console input. Shared logic is tested below the menu layer.
