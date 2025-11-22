#!/usr/bin/env python3
"""
Find semester_01 Algorithm.java files missing package declarations.
"""

import os
from pathlib import Path

def find_files_missing_packages():
    """Find all semester_01 Algorithm.java files without proper package declarations."""
    semester01_path = Path("semester_01")
    missing_packages = []

    for java_file in semester01_path.rglob("Algorithm.java"):
        try:
            content = java_file.read_text(encoding='utf-8')
            # Check if it has proper semester_01 package
            if not re.search(r'^\s*package\s+semester_01\.', content, re.MULTILINE):
                missing_packages.append(java_file)
        except Exception as e:
            print(f"Error reading {java_file}: {e}")

    return missing_packages

def main():
    """Main function."""
    import re  # Import here to avoid issues

    missing = find_files_missing_packages()
    print(f"Found {len(missing)} files missing package declarations:")

    for file_path in missing:
        print(f"  {file_path}")

    return missing

if __name__ == "__main__":
    main()
