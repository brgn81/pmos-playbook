"""Markdown rules of the Playbook: em dash, fence languages, BOM, title case headings.

Run with `uv run scripts/lint.py [root]`. Exit 0 clean, 1 findings.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

EM_DASH = "—"
BOM = "﻿"
SKIP_DIRS = {".git", ".venv", "node_modules"}
# Proper nouns that keep their capitals inside a heading.
PROPER = ("Porter's Five Forces", "Ansoff Matrix")
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")


def title_case(text: str) -> bool:
    """True when three or more plain words all start with a capital: 'Output Deliverables Here'."""
    for name in PROPER:
        text = text.replace(name, "")
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'-]*", text) if not w.isupper()]
    return len(words) >= 3 and all(w[0].isupper() for w in words)


def lint_file(path: Path, root: Path) -> list[str]:
    name = path.relative_to(root).as_posix()
    raw = path.read_text(encoding="utf-8")
    findings = []
    if raw.startswith(BOM):
        findings.append(f"{name}:1: byte order mark")
    fence = None
    for number, line in enumerate(raw.lstrip(BOM).splitlines(), start=1):
        if EM_DASH in line:
            findings.append(f"{name}:{number}: em dash, use an en dash with spaces")
        match = FENCE.match(line)
        if match:
            if fence is None:
                fence = match.group(2)[0]
                if not match.group(3).strip():
                    findings.append(f"{name}:{number}: fenced block without a language (use `text`)")
            elif match.group(2)[0] == fence and not match.group(3).strip():
                fence = None
            continue
        if fence is None:
            heading = HEADING.match(line)
            if heading and title_case(heading.group(1)):
                findings.append(f"{name}:{number}: heading is not sentence case: {heading.group(1)}")
    return findings


def main(argv: list[str]) -> int:
    root = Path(argv[1] if len(argv) > 1 else ".").resolve()
    findings = []
    for path in sorted(root.rglob("*.md")):
        if SKIP_DIRS & set(path.relative_to(root).parts):
            continue
        findings += lint_file(path, root)
    for finding in findings:
        print(finding)
    print(f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
