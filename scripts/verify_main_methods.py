#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify that all algorithm.py files have exactly one main() method."""

from pathlib import Path


def main() -> None:
    """Verify all algorithm.py files have exactly one main()."""
    base_path = Path('.')
    errors = []
    
    # Find all algorithm.py files in lecture folders
    for algorithm_file in base_path.rglob('algorithm.py'):
        if 'semester_' not in str(algorithm_file):
            continue
        if 'lecture_' not in str(algorithm_file):
            continue
        # Check if it's in a lecture folder (not algorithm subfolder)
        if algorithm_file.parent.name.startswith('lecture_'):
            content = algorithm_file.read_text(encoding='utf-8')
            main_count = content.count('def main(')
            if main_count != 1:
                errors.append(
                    f"{algorithm_file}: {main_count} main() methods"
                )
    
    if errors:
        print(f"Found {len(errors)} files with incorrect main() count:")
        for error in errors:
            print(f"  {error}")
        return 1
    else:
        print("All lecture algorithm.py files have exactly one main() method")
        return 0


if __name__ == "__main__":
    exit(main())

