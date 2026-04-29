# Architecture

## Overview

HaikuForge AI is a local command-line application. It uses plain text files as
input, in-memory Python data structures for processing, and text or WAV files as
output.

## Main Flow

```text
main.py
  -> haiku_forge.main
  -> Menu
  -> Haiku workflow
  -> FileHandler / Thesaurus / TokenizedLine / AIHaikuGenerator / HaikuAudioNarrator
```

## Key Modules

- `menu.py`: Displays the interactive menu and routes user choices.
- `haiku_utils.py`: Coordinates transformation, batch, generation, and narration workflows.
- `file_handler.py`: Reads haiku files, writes output files, and loads thesaurus mappings.
- `tokenized_utils.py`: Splits words into prefix, core, and suffix so punctuation survives replacement.
- `thesaurus.py`: Provides synonym and antonym lookup operations.
- `keyword_utils.py`: Tracks token positions for batch permutation generation.
- `ai_markov.py`: Learns bigram transitions and generates syllable-limited lines.
- `ai_syllables.py`: Stores and prompts for syllable counts.
- `audio_narrator.py`: Plays or stitches word-level WAV narration clips.
- `paths.py`: Centralises repository data paths.

## Data Structures

- Dictionaries provide O(1) average-case thesaurus and Markov transition lookup.
- Token lists preserve punctuation while allowing individual word replacement.
- `KeywordIndex` maps `(line_idx, token_idx)` to synonym lists for batch processing.
- `itertools.product` generates the Cartesian product of synonym choices.

## Platform Notes

Audio playback uses `winsound` when available on Windows. CI and non-Windows
systems can still import the package and stitch WAV files because playback is
gracefully skipped when `winsound` is unavailable.
