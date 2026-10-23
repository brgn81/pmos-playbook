"""Find minutes that mention a customer or a contact.

Usage:
    uv run find_customer_minutes.py --folder <minutes folder> <term> [term ...]

Searches the .md files of each folder (file name and content, case-insensitive) and prints the
matching paths with their item_id. Resolve the folder with `pmos where --pmos-type minute --json`.
Exit 0 (also when nothing matches), 1 when a folder does not exist or no term is given.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional


def item_id(text: str) -> Optional[str]:
    """The item_id of the identity frontmatter, if the file has one."""
    if not text.startswith("---"):
        return None
    head = text.split("\n---", 1)[0]
    match = re.search(r"^item_id:\s*['\"]?([^'\"\n]+?)['\"]?\s*$", head, re.MULTILINE)
    return match.group(1) if match else None


def search_minutes(folders: List[Path], terms: List[str]) -> List[tuple]:
    """Sorted (path, item_id) pairs of the .md files that contain any of the terms."""
    pattern = re.compile("|".join(re.escape(term) for term in terms), re.IGNORECASE)
    matches = []
    for folder in folders:
        for md_file in sorted(folder.glob("*.md")):
            try:
                text = md_file.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if pattern.search(md_file.name) or pattern.search(text):
                matches.append((md_file, item_id(text)))
    return matches


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Find minutes that mention a customer or a contact.")
    parser.add_argument("--folder", action="append", required=True, type=Path, help="Minutes folder (repeatable)")
    parser.add_argument("terms", nargs="+", help="Customer name and contact names")
    args = parser.parse_args(argv)

    missing = [folder for folder in args.folder if not folder.is_dir()]
    if missing:
        print(f"ERROR: folder not found: {', '.join(str(folder) for folder in missing)}", file=sys.stderr)
        return 1

    matches = search_minutes(args.folder, args.terms)
    if not matches:
        print(f"No minutes found mentioning: {', '.join(args.terms)}")
        return 0
    print(f"Found {len(matches)} minutes file(s) mentioning '{', '.join(args.terms)}':\n")
    for path, ident in matches:
        print(f"  {path}" + (f"  (item_id {ident})" if ident else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
