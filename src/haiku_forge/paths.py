"""Shared filesystem paths used by the application."""

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_DIR.parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SAMPLES_DIR = DATA_DIR / "samples"
THESAURUS_DIR = DATA_DIR / "thesaurus"
DEFAULT_AUDIO_DIR = DATA_DIR / "audio"
