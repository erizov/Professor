#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix all linter errors in README.md files across all algorithm folders.
Fixes: MD012 (multiple blanks), MD032 (blanks around lists), MD007 (list indentation).
"""

import re
import sys
import io
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, encoding='utf-8', errors='replace'
    )

ROOT = Path(__file__).resolve().parents[1]


def fix_multiple_blanks(content: str) -> str:
    """Fix MD012: Remove multiple consecutive blank lines."""
    # Replace 3+ blank lines with 2 blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content


def fix_blanks_around_lists(content: str) -> str:
    """Fix MD032: Ensure lists are surrounded by blank lines."""
    lines = content.split('\n')
    if not lines:
        return content
    
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if current line is a list item
        is_list_item = re.match(r'^(\s*)[-*+]\s+', line)
        is_ordered_list = re.match(r'^\s*\d+\.\s+', line)
        
        if is_list_item or is_ordered_list:
            # Check if previous line exists and is not blank and not a list item
            if i > 0:
                prev_line = lines[i-1]
                prev_is_list = (
                    re.match(r'^(\s*)[-*+]\s+', prev_line) or
                    re.match(r'^\s*\d+\.\s+', prev_line)
                )
                
                if prev_line.strip() and not prev_is_list:
                    # Need blank line before list
                    if result and result[-1].strip():
                        result.append('')
            
            result.append(line)
            
            # Check if next line exists and is not blank and not a list item
            if i < len(lines) - 1:
                next_line = lines[i+1]
                next_is_list = (
                    re.match(r'^(\s*)[-*+]\s+', next_line) or
                    re.match(r'^\s*\d+\.\s+', next_line)
                )
                
                if next_line.strip() and not next_is_list:
                    # Need blank line after list
                    result.append('')
                    i += 1
                    continue
        else:
            result.append(line)
        
        i += 1
    
    return '\n'.join(result)


def fix_list_indentation(content: str) -> str:
    """Fix MD007: Fix unordered list indentation (should be 0 or 2 spaces)."""
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # Check if line is a list item with wrong indentation
        match = re.match(r'^(\s+)([-*+])\s+(.+)$', line)
        if match:
            indent, marker, content_part = match.groups()
            indent_len = len(indent)
            
            # MD007: Unordered list indentation should be 0 or 2 spaces
            # If it's 1 or 3+ spaces, fix it
            if indent_len == 1:
                # Single space - remove it (make it 0)
                new_line = f'{marker} {content_part}'
            elif indent_len == 3:
                # Three spaces - make it 2
                new_line = f'  {marker} {content_part}'
            elif indent_len > 3:
                # More than 3 - make it 2 (for nested lists)
                new_line = f'  {marker} {content_part}'
            else:
                # Already correct (0 or 2 spaces)
                new_line = line
            result.append(new_line)
        else:
            result.append(line)
    
    return '\n'.join(result)


def fix_trailing_newline(content: str) -> str:
    """Ensure file ends with exactly one newline."""
    content = content.rstrip('\n')
    return content + '\n'


def fix_file(file_path: Path) -> bool:
    """Fix all linter errors in a README.md file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Apply fixes
        content = fix_multiple_blanks(content)
        content = fix_blanks_around_lists(content)
        content = fix_list_indentation(content)
        content = fix_trailing_newline(content)
        
        # Only write if content changed
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def main():
    """Main function to fix all README.md files."""
    print("=" * 70)
    print("FIXING LINTER ERRORS IN ALL README.MD FILES")
    print("=" * 70)
    print()
    
    # Find all README.md files
    readme_files = []
    for semester_dir in ROOT.glob("semester_*"):
        for lecture_dir in semester_dir.glob("lecture_*"):
            for algo_dir in lecture_dir.iterdir():
                if algo_dir.is_dir() and not algo_dir.name.startswith('.'):
                    readme_path = algo_dir / "README.md"
                    if readme_path.exists():
                        readme_files.append(readme_path)
    
    readme_files.sort()
    
    print(f"Found {len(readme_files)} README.md files")
    print()
    
    fixed_count = 0
    error_count = 0
    
    for idx, readme_path in enumerate(readme_files, 1):
        relative_path = readme_path.relative_to(ROOT)
        print(f"[{idx}/{len(readme_files)}] {relative_path}")
        
        if fix_file(readme_path):
            print(f"  [OK] Fixed")
            fixed_count += 1
        else:
            print(f"  [OK] No changes needed")
        
        if idx % 100 == 0:
            print(f"\nProgress: {idx}/{len(readme_files)} processed\n")
    
    print()
    print("=" * 70)
    print(f"Summary:")
    print(f"  Total files: {len(readme_files)}")
    print(f"  Files fixed: {fixed_count}")
    print(f"  Errors: {error_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

