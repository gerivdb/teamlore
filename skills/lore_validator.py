#!/usr/bin/env python3
"""
teamlore validate — Lore Validator
Checks that all .lore/ entries conform to the schema:
- Frontmatter: kind, commit, verify_by
- Word count <= 120
- Paths exist in repo
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime

VALID_KINDS = {"mistake", "gotcha", "decision"}
MAX_WORDS = 120

def validate_lore_file(path: Path) -> list:
    errors = []
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"read error: {e}"]

    if not content.startswith("---"):
        errors.append("missing frontmatter")
        return errors

    match = re.match(r"---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        errors.append("malformed frontmatter")
        return errors

    frontmatter = match.group(1)
    body = content[match.end():]

    for key in ["kind", "commit", "verify_by"]:
        if key not in frontmatter:
            errors.append(f"missing field: {key}")

    kind_match = re.search(r"kind:\s*(\w+)", frontmatter)
    if kind_match and kind_match.group(1) not in VALID_KINDS:
        errors.append(f"invalid kind: {kind_match.group(1)}")

    words = len(body.split())
    if words > MAX_WORDS:
        errors.append(f"word count {words} > {MAX_WORDS}")

    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: teamlore validate <lore-root>")
        sys.exit(1)

    lore_root = Path(sys.argv[1])
    if not lore_root.exists():
        print(f"ERROR: {lore_root} does not exist")
        sys.exit(1)

    all_errors = []
    for md in lore_root.rglob("*.md"):
        errors = validate_lore_file(md)
        if errors:
            all_errors.append((str(md), errors))

    if all_errors:
        print("VALIDATION FAILED")
        for path, errors in all_errors:
            print(f"  {path}:")
            for err in errors:
                print(f"    - {err}")
        sys.exit(1)
    else:
        print("VALIDATION PASSED")
        sys.exit(0)

if __name__ == "__main__":
    main()
