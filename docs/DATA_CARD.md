# Data Card

## Data Assets

- `data/samples`: Plain text haiku examples.
- `data/thesaurus`: Synonym and antonym mappings.
- `data/audio`: Word-level WAV clips used for narration.
- `outputs/haiku_003_synonymized`: Previously generated haiku variants retained for reference.

## Format

Haiku files contain one line per row. Thesaurus files use:

```text
keyword: replacement one, replacement two
```

Audio clips use lowercase word filenames such as `autumn.wav`.

## Privacy

The included data does not require credentials and should not contain personal
or sensitive information.

## Quality Checks

- Thesaurus parsing is covered by tests.
- Haiku/thesaurus file detection is covered by tests.
- Audio stitching is covered with generated test WAV files.

## Maintenance

When adding data:

- Use UTF-8 for text files.
- Keep thesaurus keys lowercase where possible.
- Add syllable counts for new vocabulary used by the Markov fallback path.
- Keep generated one-off outputs under `outputs/` rather than `data/`.
