#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix multiple main() functions in algorithm.py files
Ensure each file has only one main() function
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def fix_multiple_main_functions(file_path: Path) -> bool:
    """Fix files with multiple main() functions."""
    try:
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Count main() functions
        main_count = len(
            [line for line in lines if re.match(r"^\s*def\s+main\s*\(", line)]
        )

        if main_count <= 1:
            return False  # No issue

        # Find all main() function positions
        main_positions = []
        for i, line in enumerate(lines):
            if re.match(r"^\s*def\s+main\s*\(", line):
                main_positions.append(i)

        if len(main_positions) <= 1:
            return False

        # Find the first complete main() function
        first_main_start = main_positions[0]

        # Find where first main() ends (next def or if __name__)
        first_main_end = len(lines)
        for i in range(first_main_start + 1, len(lines)):
            if re.match(r"^\s*def\s+\w+\s*\(", lines[i]) and "main" not in lines[i]:
                first_main_end = i
                break
            if "if __name__" in lines[i]:
                first_main_end = i + 2  # Include the if __name__ block
                break

        # Find if __name__ == "__main__" block
        name_main_pos = None
        for i in range(len(lines)):
            if "if __name__" in lines[i]:
                name_main_pos = i
                break

        # Keep content up to first main, then first main, then if __name__ if exists
        if name_main_pos and name_main_pos < first_main_end:
            # if __name__ is inside first main, keep it
            new_lines = lines[:first_main_end]
        elif name_main_pos:
            # if __name__ is after first main, include it
            new_lines = (
                lines[:first_main_end] + lines[name_main_pos : name_main_pos + 2]
            )
        else:
            # No if __name__, just keep up to first main end
            new_lines = lines[:first_main_end]
            # Add if __name__ if it should be there
            if first_main_end < len(lines):
                # Check if there's an if __name__ later
                for i in range(first_main_end, len(lines)):
                    if "if __name__" in lines[i]:
                        new_lines.extend(lines[i : i + 2])
                        break

        # Ensure we have if __name__ at the end
        if not any("if __name__" in line for line in new_lines):
            new_lines.append("")
            new_lines.append('if __name__ == "__main__":')
            new_lines.append("    main()")

        fixed_content = "\n".join(new_lines)

        # Only write if content changed
        if fixed_content != content:
            file_path.write_text(fixed_content, encoding="utf-8")
            return True

        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Fix all files with multiple main() functions."""
    print("=" * 70)
    print("Fix Multiple main() Functions")
    print("=" * 70)

    fixed_count = 0
    total_files = 0
    multiple_main_count = 0

    for algo_file in ROOT.rglob("**/algorithm.py"):
        if "supporting_documents" in str(algo_file) or "scripts" in str(algo_file):
            continue

        total_files += 1
        try:
            content = algo_file.read_text(encoding="utf-8")
            main_count = len(re.findall(r"^\s*def\s+main\s*\(", content, re.MULTILINE))

            if main_count > 1:
                multiple_main_count += 1
                if fix_multiple_main_functions(algo_file):
                    fixed_count += 1
                    if fixed_count % 50 == 0:
                        print(f"Fixed {fixed_count} files...")
        except Exception:
            continue

    print(f"\n[COMPLETE] Scanned {total_files} files")
    print(f"Files with multiple main() functions: {multiple_main_count}")
    print(f"Files fixed: {fixed_count}")


if __name__ == "__main__":
    main()
