#!/usr/bin/env python3
"""
Fix missing package declarations in remaining semester_01 Algorithm.java files.
"""

import os
from pathlib import Path

def fix_remaining_packages():
    """Fix package declarations in all remaining semester_01 Algorithm.java files."""
    semester01_path = Path("semester_01")

    if not semester01_path.exists():
        print("semester_01 directory not found!")
        return

    fixed_count = 0

    for java_file in semester01_path.rglob("Algorithm.java"):
        content = java_file.read_text(encoding='utf-8')

        # Skip if already has package
        if 'package semester_01.' in content:
            continue

        # Generate package name from path
        path_parts = java_file.parts
        package_parts = []
        for part in path_parts:
            if part != "semester_01":
                package_parts.append(part)

        package_name = "semester_01." + ".".join(package_parts[:-1])  # Exclude filename

        # Add package declaration at top
        lines = content.split('\n')

        # Find first non-comment, non-empty line
        insert_idx = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('*'):
                insert_idx = i
                break

        lines.insert(insert_idx, f'package {package_name};')
        if insert_idx > 0 or lines[insert_idx + 1].strip():
            lines.insert(insert_idx + 1, '')

        content = '\n'.join(lines)
        java_file.write_text(content, encoding='utf-8')
        print(f"Fixed package in: {java_file}")
        fixed_count += 1

    print(f"\nFixed package declarations in {fixed_count} additional files")

if __name__ == "__main__":
    fix_remaining_packages()
