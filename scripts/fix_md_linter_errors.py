#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix common linter errors in school.ru.md and univer.ru.md files.
Fixes:
- MD009: Trailing spaces (remove single trailing spaces)
- MD029: Ordered list numbering (restart numbering in each subsection)
- MD047: Missing trailing newline
"""

import re
import sys
import io
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parents[1]


def fix_trailing_spaces(content: str) -> str:
    """Remove single trailing spaces (MD009)."""
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Remove single trailing space, but keep double spaces (for line breaks)
        if line.endswith(' '):
            # Check if it's a single space (not double)
            stripped = line.rstrip(' ')
            if len(line) - len(stripped) == 1:
                # Single trailing space - remove it
                line = stripped
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)


def fix_ordered_list_numbering(content: str) -> str:
    """Fix ordered list numbering to restart in each subsection (MD029)."""
    lines = content.split('\n')
    fixed_lines = []
    current_number = 0
    in_list = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a header (### or ##)
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if header_match:
            # Reset numbering when we hit a new header
            current_number = 0
            in_list = False
            fixed_lines.append(line)
            i += 1
            continue
        
        # Check if this is an ordered list item
        list_match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if list_match:
            number = int(list_match.group(1))
            text = list_match.group(2)
            
            # If this is the first item after a header or gap, restart at 1
            if not in_list:
                current_number = 1
            else:
                current_number += 1
            
            # Always use the correct sequential number
            fixed_lines.append(f"{current_number}. {text}")
            in_list = True
        else:
            # Not a list item - reset state if blank line
            if line.strip() == '':
                in_list = False
                current_number = 0
            fixed_lines.append(line)
        
        i += 1
    
    return '\n'.join(fixed_lines)


def fix_multiple_blank_lines(content: str) -> str:
    """Fix multiple consecutive blank lines (MD012)."""
    # Replace 2+ consecutive newlines with exactly 2 newlines (one blank line)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content


def fix_trailing_newline(content: str) -> str:
    """Ensure file ends with exactly one newline (MD047)."""
    # Remove all trailing newlines
    content = content.rstrip('\n')
    # Add exactly one newline
    return content + '\n'


def fix_file(file_path: Path) -> bool:
    """Fix linter errors in a single file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Apply fixes
        content = fix_trailing_spaces(content)
        content = fix_multiple_blank_lines(content)
        content = fix_ordered_list_numbering(content)
        content = fix_trailing_newline(content)
        
        # Only write if changed
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"  [ERROR] Failed to fix {file_path}: {e}")
        return False


def main():
    """Main function to fix all MD files."""
    print("=" * 70)
    print("ИСПРАВЛЕНИЕ ОШИБОК ЛИНТЕРА В MD ФАЙЛАХ")
    print("=" * 70)
    print()
    
    # Find all school.ru.md and univer.ru.md files
    school_files = list(ROOT.rglob("school.ru.md"))
    univer_files = list(ROOT.rglob("univer.ru.md"))
    all_files = school_files + univer_files
    all_files.sort()
    
    print(f"Найдено файлов:")
    print(f"  school.ru.md: {len(school_files)}")
    print(f"  univer.ru.md: {len(univer_files)}")
    print(f"  Всего: {len(all_files)}")
    print()
    
    fixed_count = 0
    error_count = 0
    
    for idx, file_path in enumerate(all_files, 1):
        relative_path = file_path.relative_to(ROOT)
        print(f"[{idx}/{len(all_files)}] {relative_path}")
        
        if fix_file(file_path):
            print(f"  [OK] Исправлено")
            fixed_count += 1
        else:
            print(f"  [OK] Без изменений")
        
        if idx % 100 == 0:
            print(f"\nПрогресс: {idx}/{len(all_files)} обработано\n")
    
    print()
    print("=" * 70)
    print(f"Итоги:")
    print(f"  Всего файлов: {len(all_files)}")
    print(f"  Исправлено: {fixed_count}")
    print(f"  Без изменений: {len(all_files) - fixed_count}")
    print(f"  Ошибок: {error_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()

