#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Java package declarations that are incorrectly placed inside comment blocks.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def fix_package_in_comments(java_file: Path) -> bool:
    """Fix package declarations inside comment blocks."""
    try:
        content = java_file.read_text(encoding='utf-8')

        # Pattern to find package declarations inside javadoc comments
        # Look for /** followed by some content including package statement, then */
        pattern = r'(/\*\*[\s\S]*?package\s+[^;]+;[\s\S]*?\*/\s*)'

        def fix_match(match):
            comment_block = match.group(1)

            # Extract the package statement
            package_match = re.search(r'package\s+([^;]+);', comment_block)
            if not package_match:
                return match.group(0)

            package_stmt = f"package {package_match.group(1)};"

            # Remove the package statement from the comment block
            fixed_comment = re.sub(r'\s*package\s+[^;]+;\s*', '', comment_block)

            return f"{package_stmt}\n\n{fixed_comment}"

        # Apply the fix
        new_content = re.sub(pattern, fix_match, content, flags=re.DOTALL)

        if new_content != content:
            java_file.write_text(new_content, encoding='utf-8')
            return True

    except Exception as e:
        print(f"Error processing {java_file}: {e}")

    return False

def main():
    """Main function to fix all Java files with package issues."""
    fixed_count = 0

    for java_file in ROOT.glob('semester_*/**/Algorithm.java'):
        if fix_package_in_comments(java_file):
            print(f"Fixed: {java_file}")
            fixed_count += 1

    print(f"\nFixed {fixed_count} Java files with package declarations inside comments.")

if __name__ == "__main__":
    main()
