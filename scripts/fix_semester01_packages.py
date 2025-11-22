#!/usr/bin/env python3
"""
Fix missing package declarations in semester_01 Algorithm.java files.
"""

import os
import re
from pathlib import Path

def fix_package_declarations():
    """Fix package declarations in all semester_01 Algorithm.java files."""
    semester01_path = Path("semester_01")

    if not semester01_path.exists():
        print("semester_01 directory not found!")
        return

    fixed_count = 0

    for java_file in semester01_path.rglob("Algorithm.java"):
        content = java_file.read_text(encoding='utf-8')

        # Check if package declaration already exists
        if re.search(r'^\s*package\s+semester_01\.', content, re.MULTILINE):
            continue  # Already has proper package

        # Generate package name from path
        relative_path = java_file.relative_to(semester01_path.parent)
        package_parts = []
        for part in relative_path.parts[:-1]:  # Exclude filename
            if part != "semester_01":
                package_parts.append(part)

        package_name = "semester_01." + ".".join(package_parts)

        # Check if package is mentioned in comments
        package_in_comment = re.search(r'package\s+(' + re.escape(package_name) + r');', content)

        if package_in_comment:
            # Package declaration is in comment, move it to proper location
            # Remove from comment and add at top
            content = re.sub(r'/\*\*\s*\n\s*package\s+' + re.escape(package_name) + r';\s*\n', '', content)
            content = re.sub(r'^\s*\*\s*package\s+' + re.escape(package_name) + r';\s*\n', '', content)

            # Add proper package declaration at top
            lines = content.split('\n')
            # Find where imports start
            insert_index = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('import') or line.strip().startswith('public class'):
                    insert_index = i
                    break

            lines.insert(insert_index, f'package {package_name};')
            lines.insert(insert_index + 1, '')

            content = '\n'.join(lines)
        else:
            # No package declaration at all, add it
            lines = content.split('\n')
            # Find first non-comment, non-empty line
            insert_index = 0
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('*'):
                    insert_index = i
                    break

            lines.insert(insert_index, f'package {package_name};')
            if insert_index > 0:
                lines.insert(insert_index + 1, '')

            content = '\n'.join(lines)

        # Write back the file
        java_file.write_text(content, encoding='utf-8')
        print(f"Fixed package in: {java_file}")
        fixed_count += 1

    print(f"\nFixed package declarations in {fixed_count} files")

if __name__ == "__main__":
    fix_package_declarations()
