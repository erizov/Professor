#!/usr/bin/env python3
"""
Fix package declarations to be the first line in Java files.
Package declarations should come before any imports, comments, or blank lines.
"""

import re
import sys
from pathlib import Path

def fix_package_declaration(java_file: Path) -> bool:
    """Fix package declaration to be the first line in a Java file."""
    try:
        content = java_file.read_text(encoding='utf-8')

        # Check if package declaration exists
        package_match = re.search(r'^package\s+([^;]+);', content, re.MULTILINE)
        if not package_match:
            print(f"  No package declaration found in {java_file}")
            return False

        package_line = package_match.group(0)
        package_start = package_match.start()

        # If package is already the first line (ignoring whitespace), no change needed
        before_package = content[:package_start].strip()
        if not before_package:
            print(f"  OK Package already first line in {java_file}")
            return True

        # Extract everything after the package declaration
        after_package_start = package_match.end()
        remaining_content = content[after_package_start:]

        # Remove any leading whitespace/comments before package
        lines = content.split('\n')
        package_line_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith('package '):
                package_line_index = i
                break

        if package_line_index is None:
            print(f"  ERROR Could not find package line index in {java_file}")
            return False

        # Reconstruct file with package as first line
        new_lines = []

        # Add the package declaration first
        new_lines.append(lines[package_line_index])

        # Add the rest of the lines, skipping the original package line
        for i, line in enumerate(lines):
            if i != package_line_index:
                new_lines.append(line)

        # Write back to file
        new_content = '\n'.join(new_lines)
        java_file.write_text(new_content, encoding='utf-8')

        print(f"  OK Fixed package to first line in {java_file}")
        return True

    except Exception as e:
        print(f"  ERROR Error fixing {java_file}: {e}")
        return False

def main():
    """Main function to fix package declarations in all Java files."""
    if len(sys.argv) != 2:
        print("Usage: python fix_package_first_line.py <root_directory>")
        sys.exit(1)

    root_dir = Path(sys.argv[1])

    if not root_dir.exists():
        print(f"Directory {root_dir} does not exist")
        sys.exit(1)

    # Find all Java files
    java_files = list(root_dir.rglob("**/Algorithm.java"))

    print(f"Found {len(java_files)} Java files to process")

    fixed_count = 0
    error_count = 0

    for java_file in java_files:
        if fix_package_declaration(java_file):
            fixed_count += 1
        else:
            error_count += 1

    print(f"\nSummary:")
    print(f"  Fixed: {fixed_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total: {len(java_files)}")

if __name__ == "__main__":
    main()
