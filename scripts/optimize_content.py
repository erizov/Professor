#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Optimize content by removing repetitions, consolidating duplicates,
and improving variety.
"""

import re
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]

# Excessive qualifiers to remove or reduce
EXCESSIVE_QUALIFIERS = [
    r"\bvery\s+",
    r"\breally\s+",
    r"\bextremely\s+",
    r"\bincredibly\s+",
    r"\bquite\s+",
    r"\brather\s+",
    r"\bpretty\s+",
]

# Repetitive phrases to consolidate
REPETITIVE_PHRASES = [
    (r"\bfundamental\s+algorithm\s+that\s+is\s+fundamental", "fundamental algorithm"),
    (r"\bimportant\s+technique\s+that\s+is\s+important", "important technique"),
    (r"\bwidely\s+used\s+and\s+widely\s+applicable", "widely used"),
    (r"\bcommonly\s+used\s+and\s+commonly\s+applied", "commonly used"),
]

# Synonyms for variety
SYNONYM_REPLACEMENTS = {
    "algorithm": ["algorithm", "technique", "method", "approach"],
    "important": ["important", "significant", "crucial", "essential"],
    "efficient": ["efficient", "effective", "optimal", "performant"],
    "use": ["use", "utilize", "employ", "apply"],
    "example": ["example", "instance", "case", "illustration"],
}


def remove_excessive_qualifiers(content: str) -> Tuple[str, bool]:
    """Remove excessive qualifiers."""
    changed = False
    for qualifier in EXCESSIVE_QUALIFIERS:
        pattern = re.compile(qualifier, re.IGNORECASE)
        if pattern.search(content):
            content = pattern.sub("", content)
            changed = True
    return content, changed


def consolidate_repetitive_phrases(content: str) -> Tuple[str, bool]:
    """Consolidate repetitive phrases."""
    changed = False
    for pattern, replacement in REPETITIVE_PHRASES:
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            changed = True
    return content, changed


def remove_duplicate_sentences(content: str) -> Tuple[str, bool]:
    """Remove duplicate sentences."""
    lines = content.split("\n")
    seen = set()
    new_lines = []
    changed = False

    for line in lines:
        # Normalize line (lowercase, strip)
        normalized = line.lower().strip()
        # Skip if empty or header
        if not normalized or normalized.startswith("#"):
            new_lines.append(line)
            continue
        # Check if we've seen this sentence
        if normalized not in seen:
            seen.add(normalized)
            new_lines.append(line)
        else:
            changed = True

    return "\n".join(new_lines), changed


def remove_redundant_lists(content: str) -> Tuple[str, bool]:
    """Remove redundant list items."""
    changed = False
    # Find bullet lists
    list_pattern = r"(-|\*|\d+\.)\s+(.+?)(?=\n(-|\*|\d+\.)|\n\n|$)"

    def process_list(match):
        items = []
        list_text = match.group(0)
        items_pattern = r"(-|\*|\d+\.)\s+(.+?)(?=\n(-|\*|\d+\.)|\n\n|$)"
        for item_match in re.finditer(items_pattern, list_text):
            item = item_match.group(2).strip().lower()
            if item not in items:
                items.append(item)
            else:
                nonlocal changed
                changed = True
                return ""  # Remove duplicate
        return list_text

    content = re.sub(
        list_pattern, process_list, content, flags=re.MULTILINE | re.DOTALL
    )
    return content, changed


def optimize_readme(readme_path: Path) -> bool:
    """Optimize a single README file."""
    try:
        content = readme_path.read_text(encoding="utf-8")
        original = content

        # Apply optimizations
        content, changed1 = remove_excessive_qualifiers(content)
        content, changed2 = consolidate_repetitive_phrases(content)
        content, changed3 = remove_duplicate_sentences(content)
        content, changed4 = remove_redundant_lists(content)

        if changed1 or changed2 or changed3 or changed4:
            readme_path.write_text(content, encoding="utf-8")
            return True

        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False


def main():
    """Optimize all README files."""
    updated_count = 0
    total_count = 0

    # Find all README files
    for readme_path in ROOT.rglob("README.md"):
        # Skip root README
        if readme_path == ROOT / "README.md":
            continue

        total_count += 1
        if optimize_readme(readme_path):
            updated_count += 1
            print(f"Optimized: {readme_path.relative_to(ROOT)}")

    print(f"\nOptimized {updated_count}/{total_count} README files")


if __name__ == "__main__":
    main()
