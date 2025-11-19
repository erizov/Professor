#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify all algorithm.py files have exactly one main() method
and clean up duplicate content in README files.
"""

from pathlib import Path
from typing import List, Tuple
import re


def find_all_algorithm_folders() -> List[Path]:
    """Find all algorithm subfolders."""
    base_path = Path(".")
    algorithm_folders = []

    for semester_dir in base_path.glob("semester_*"):
        if not semester_dir.is_dir():
            continue
        if any(x in str(semester_dir) for x in ["__pycache__", ".git"]):
            continue

        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue
            if "lecture_" not in lecture_dir.name:
                continue

            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                if algo_dir.name.startswith("lecture_"):
                    continue
                if any(x in algo_dir.name for x in ["__pycache__", ".git"]):
                    continue

                algorithm_folders.append(algo_dir)

    return sorted(algorithm_folders)


def verify_main_method(algorithm_path: Path) -> Tuple[bool, int]:
    """Verify algorithm.py has exactly one main() method."""
    if not algorithm_path.exists():
        return False, 0

    content = algorithm_path.read_text(encoding="utf-8")
    main_count = content.count("def main(")
    return main_count == 1, main_count


def clean_readme_duplicates(readme_path: Path) -> bool:
    """Remove duplicate sections from README."""
    if not readme_path.exists():
        return False

    content = readme_path.read_text(encoding="utf-8")
    original_content = content

    # Remove duplicate "Algorithm Description" sections
    # Keep only the first one
    sections = re.split(r"(## Algorithm Description)", content)
    if len(sections) > 3:  # More than one section
        # Reconstruct with only first section
        content = sections[0] + sections[1] + sections[2]
        # Add remaining content after first complete section
        if len(sections) > 3:
            # Find where first section ends
            first_section_end = content.find(
                "## ", content.find("## Algorithm Description") + 1
            )
            if first_section_end > 0:
                remaining = "".join(sections[3:])
                # Remove duplicate "Algorithm Description" from remaining
                remaining = re.sub(
                    r"## Algorithm Description.*?## (?!Algorithm Description)",
                    "## ",
                    remaining,
                    flags=re.DOTALL,
                )
                content = content[:first_section_end] + "\n" + remaining

    # Remove duplicate "How It Works" sections
    how_it_works_pattern = r"(### How It Works.*?)(?=### |## |$)"
    matches = list(re.finditer(how_it_works_pattern, content, re.DOTALL))
    if len(matches) > 1:
        # Keep first, remove others
        for match in reversed(matches[1:]):
            content = content[: match.start()] + content[match.end() :]

    # Remove duplicate "Complexity Analysis" sections
    complexity_pattern = r"(### Complexity Analysis.*?)(?=### |## |$)"
    matches = list(re.finditer(complexity_pattern, content, re.DOTALL))
    if len(matches) > 1:
        for match in reversed(matches[1:]):
            content = content[: match.start()] + content[match.end() :]

    # Remove duplicate "Use Cases" sections
    use_cases_pattern = r"(### Use Cases.*?)(?=### |## |$)"
    matches = list(re.finditer(use_cases_pattern, content, re.DOTALL))
    if len(matches) > 1:
        for match in reversed(matches[1:]):
            content = content[: match.start()] + content[match.end() :]

    # Remove placeholder sections that come after real content
    if "## Algorithm Description" in content:
        # Remove old placeholder sections
        placeholder_patterns = [
            r"## Overview\s+[^\n]+\s+is a fundamental algorithm.*?## Description",
            r"## Description\s+Bubble sort is used to solve.*?## Algorithm Details",
            r"## Algorithm Details.*?\[describe use case\].*?## Use Cases",
        ]
        for pattern in placeholder_patterns:
            content = re.sub(pattern, "", content, flags=re.DOTALL)

    # Clean up extra blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)

    if content != original_content:
        readme_path.write_text(content, encoding="utf-8")
        return True

    return False


def main() -> None:
    """Main function."""
    print("Finding all algorithm folders...")
    algorithm_folders = find_all_algorithm_folders()
    print(f"Found {len(algorithm_folders)} algorithm folders\n")

    # Verify main() methods
    print("Verifying main() methods in algorithm.py files...")
    correct_count = 0
    incorrect_count = 0
    missing_count = 0
    errors = []

    for algo_folder in algorithm_folders:
        algorithm_path = algo_folder / "algorithm.py"
        is_correct, main_count = verify_main_method(algorithm_path)

        if not algorithm_path.exists():
            missing_count += 1
            errors.append(f"{algo_folder}: algorithm.py missing")
        elif is_correct:
            correct_count += 1
        else:
            incorrect_count += 1
            errors.append(f"{algo_folder}: {main_count} main() methods (expected 1)")

    print(f"  Correct (1 main()): {correct_count}")
    print(f"  Incorrect: {incorrect_count}")
    print(f"  Missing: {missing_count}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors[:20]:
            print(f"  {error}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")

    # Clean up README duplicates
    print("\nCleaning up duplicate content in README files...")
    cleaned_count = 0

    for algo_folder in algorithm_folders:
        readme_path = algo_folder / "README.md"
        if clean_readme_duplicates(readme_path):
            cleaned_count += 1

    print(f"  Cleaned {cleaned_count} README files")

    print("\nSummary:")
    print(f"  Total algorithm folders: {len(algorithm_folders)}")
    print(f"  algorithm.py files with correct main(): {correct_count}")
    print(f"  algorithm.py files needing fixes: {incorrect_count + missing_count}")
    print(f"  README files cleaned: {cleaned_count}")


if __name__ == "__main__":
    main()
