#!/usr/bin/env python3
"""
Fix Python import paths to ensure framework modules are accessible.
Add project root to sys.path if running from subdirectories.
"""

import re
import sys
from pathlib import Path

def fix_python_imports(python_file: Path) -> bool:
    """Add path setup to ensure framework imports work."""
    try:
        content = python_file.read_text(encoding='utf-8')

        # Check if file already has path setup
        if 'sys.path.insert' in content or 'sys.path.append' in content:
            print(f"  OK Path setup already exists in {python_file}")
            return False

        # Check if file imports from framework
        if 'from framework' not in content:
            print(f"  OK No framework imports in {python_file}")
            return False

        lines = content.split('\n')

        # Find the first import line
        insert_index = -1
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                insert_index = i
                break

        if insert_index == -1:
            print(f"  OK No imports found in {python_file}")
            return False

        # Add path setup before the first import
        path_setup = [
            "",
            "# Add project root to path for framework imports",
            "import sys",
            "from pathlib import Path",
            "sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))",
            ""
        ]

        # Insert the path setup
        new_lines = lines[:insert_index] + path_setup + lines[insert_index:]

        new_content = '\n'.join(new_lines)
        python_file.write_text(new_content, encoding='utf-8')

        print(f"  OK Added path setup to {python_file}")
        return True

    except Exception as e:
        print(f"  ERROR Error fixing {python_file}: {e}")
        return False

def main():
    """Main function to fix imports in all Python algorithm files."""
    if len(sys.argv) != 2:
        print("Usage: python fix_python_imports.py <root_directory>")
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
    skipped_count = 0

    for python_file in python_files:
        if "test" in python_file.name.lower():
            continue  # Skip test files

        if fix_python_imports(python_file):
            fixed_count += 1
        else:
            skipped_count += 1

    print(f"\nSummary:")
    print(f"  Fixed: {fixed_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total: {len(python_files)}")

if __name__ == "__main__":
    main()
