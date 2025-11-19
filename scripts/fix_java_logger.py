#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix common Java compilation errors:
1. logger.info() without arguments -> logger.info("")
2. String.repeat() compatibility issues
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fix_java_file(file_path: Path) -> bool:
    """Fix common Java compilation errors in a file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        original_content = content
        
        # Fix logger.info() without arguments
        content = re.sub(r'logger\.info\(\);', 'logger.info("");', content)
        
        # Fix String.repeat() in logger.info() calls - extract to variable first
        # Pattern: logger.info("=".repeat(70));
        def fix_repeat_in_logger(match):
            separator = match.group(1)
            count = match.group(2)
            var_name = "separator" if separator == "=" else "dash"
            return f'{var_name} = "{separator}".repeat({count});\n        logger.info({var_name});'
        
        # Check if we need to add separator variable declaration
        if re.search(r'logger\.info\(["\']=+["\']\.repeat\(', content):
            # Find first occurrence and add variable declaration before main method
            main_match = re.search(r'(public static void main\(String\[\] args\) \{)', content)
            if main_match:
                # Check if separator already declared
                if 'String separator' not in content[:main_match.end()]:
                    # Add separator declaration right after main method start
                    content = content[:main_match.end()] + '\n        String separator = "=".repeat(70);\n        String dash = "-".repeat(70);' + content[main_match.end():]
        
        # Replace logger.info("=".repeat(70)) with logger.info(separator)
        content = re.sub(r'logger\.info\(["\']=+["\']\.repeat\(70\)\);', 'logger.info(separator);', content)
        content = re.sub(r'logger\.info\(["\']-+["\']\.repeat\(70\)\);', 'logger.info(dash);', content)
        
        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            return True
        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Fix all Java files."""
    java_files = list(ROOT.rglob("**/Algorithm.java"))
    print(f"Found {len(java_files)} Java files")
    
    fixed_count = 0
    for java_file in java_files:
        if fix_java_file(java_file):
            fixed_count += 1
            print(f"Fixed: {java_file.relative_to(ROOT)}")
    
    print(f"\nFixed {fixed_count} files")


if __name__ == "__main__":
    main()

