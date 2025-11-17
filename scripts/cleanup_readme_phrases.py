#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cleanup README files removing forbidden phrases and cross references.
"""

from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PHRASES: List[str] = [
    "**Time Complexity**: See complexity analysis below",
    "**Space Complexity**: See complexity analysis below",
    "**When to Use**: See 'Best Use Case' section",
    "**When NOT to Employ**: See 'Do Not Confuse With' section",
    "**When NOT to Use**: See 'Do Not Confuse With' section",
]


def cleanup_readme(readme_path: Path) -> bool:
    """Remove forbidden phrases from README."""
    content = readme_path.read_text(encoding="utf-8")
    new_content = content

    for phrase in FORBIDDEN_PHRASES:
        new_content = new_content.replace(phrase, "")

    # Remove references like "Topic 1: See Topic 2"
    new_content = new_content.replace("See 'Best Use Case' section", "")
    new_content = new_content.replace("See 'Do Not Confuse With' section", "")

    if new_content != content:
        readme_path.write_text(new_content, encoding="utf-8")
        return True
    return False


def main():
    readme_files = [
        path
        for path in ROOT.rglob("*/README.md")
        if path.parent != ROOT
    ]

    cleaned = 0
    total = len(readme_files)

    print(f"Cleaning {total} README files...")

    for readme in readme_files:
        if cleanup_readme(readme):
            cleaned += 1

    print(f"[COMPLETE] Cleaned {cleaned}/{total} README files")


if __name__ == "__main__":
    main()

