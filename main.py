"""Compatibility launcher for the HaikuForge AI command-line app.

The project source now lives in ``src/haiku_forge``. This thin wrapper keeps the
coursework-friendly command ``python main.py`` working from the repository root.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from haiku_forge.main import main  # noqa: E402

if __name__ == "__main__":
    main()
