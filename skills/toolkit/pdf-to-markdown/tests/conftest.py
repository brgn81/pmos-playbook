"""Shared pytest configuration for the pdf-to-markdown test suite.

The converter lives in ``scripts/pdf_to_markdown.py`` and is imported as a
top-level module (the same way the CLI runs it), so that directory is placed
on ``sys.path`` here rather than in every test file.
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
