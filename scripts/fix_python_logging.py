#!/usr/bin/env python3
"""
Fix Python logging formatting issues.
Replace logger.info("Message: {}", var) with logger.info("Message: %s", var)
"""

import re
import sys
from pathlib import Path

def fix_logging_format(python_file: Path) -> bool:
    """Fix logging format strings in a Python file."""
    try:
        content = python_file.read_text(encoding='utf-8')

        # Pattern to match logger calls with {} placeholders
        # Matches: logger.info("message {}", var) but not f"message {var}"
        pattern = r'(\w+)\.(\w+)\(\s*"([^"]*)\{\}([^"]*)"\s*,\s*([^)]+)\s*\)'

        def replace_match(match):
            logger_name = match.group(1)
            method_name = match.group(2)
            prefix = match.group(3)
            suffix = match.group(4)
            args = match.group(5)

            # Replace {} with %s for proper logging format
            new_message = f'"{prefix}%s{suffix}"'
            return f'{logger_name}.{method_name}({new_message}, {args})'

        new_content = re.sub(pattern, replace_match, content)

        if new_content != content:
            python_file.write_text(new_content, encoding='utf-8')
            print(f"  OK Fixed logging in {python_file}")
            return True
        else:
            print(f"  OK No logging issues in {python_file}")
            return False

    except Exception as e:
        print(f"  ERROR Error fixing {python_file}: {e}")
        return False

def main():
    """Main function to fix logging in all Python algorithm files."""
    if len(sys.argv) != 2:
        print("Usage: python fix_python_logging.py <root_directory>")
        sys.exit(1)

    root_dir = Path(sys.argv[1])

    if not root_dir.exists():
        print(f"Directory {root_dir} does not exist")
        sys.exit(1)

    # Find all Python algorithm files (not test files)
    python_files = []
    for pattern in ["**/algorithm.py", "**/Algorithm.py"]:
        python_files.extend(list(root_dir.rglob(pattern)))

    print(f"Found {len(python_files)} Python algorithm files to process")

    fixed_count = 0
    error_count = 0

    for python_file in python_files:
        if "test" in python_file.name.lower():
            continue  # Skip test files

        if fix_logging_format(python_file):
            fixed_count += 1
        else:
            error_count += 1

    print(f"\nSummary:")
    print(f"  Fixed: {fixed_count}")
    print(f"  No changes needed: {error_count}")
    print(f"  Total: {len(python_files)}")

if __name__ == "__main__":
    main()
