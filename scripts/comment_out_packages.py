#!/usr/bin/env python3
"""
Comment out package declarations in Java files.
This allows testing Java files without package structure.
"""

import re
import sys
from pathlib import Path

def comment_out_package(java_file: Path) -> bool:
    """Comment out package declaration in a Java file."""
    try:
        content = java_file.read_text(encoding='utf-8')

        # Check if package declaration exists
        package_match = re.search(r'^package\s+([^;]+);', content, re.MULTILINE)
        if not package_match:
            print(f"  No package declaration found in {java_file}")
            return False

        package_line = package_match.group(0)
        package_start = package_match.start()
        package_end = package_match.end()

        # Check if already commented out
        lines = content.split('\n')
        package_line_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith('package '):
                package_line_index = i
                # Check if already commented
                if line.strip().startswith('//'):
                    print(f"  Package already commented in {java_file}")
                    return False
                break

        if package_line_index is None:
            print(f"  ERROR Could not find package line in {java_file}")
            return False

        # Comment out the package line
        lines[package_line_index] = '// ' + lines[package_line_index]

        new_content = '\n'.join(lines)
        java_file.write_text(new_content, encoding='utf-8')

        print(f"  OK Commented out package in {java_file}")
        return True

    except Exception as e:
        print(f"  ERROR Error processing {java_file}: {e}")
        return False

def main():
    """Main function to comment out packages in all Java files."""
    if len(sys.argv) != 2:
        print("Usage: python comment_out_packages.py <root_directory>")
        sys.exit(1)

    root_dir = Path(sys.argv[1])

    if not root_dir.exists():
        print(f"Directory {root_dir} does not exist")
        sys.exit(1)

    # Find all Java files
    java_files = list(root_dir.rglob("**/Algorithm.java"))

    print(f"Found {len(java_files)} Java files to process")

    fixed_count = 0
    skipped_count = 0

    for java_file in java_files:
        if comment_out_package(java_file):
            fixed_count += 1
        else:
            skipped_count += 1

    print(f"\nSummary:")
    print(f"  Commented out: {fixed_count}")
    print(f"  Skipped: {skipped_count}")
    print(f"  Total: {len(java_files)}")

if __name__ == "__main__":
    main()
