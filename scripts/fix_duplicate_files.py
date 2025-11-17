#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix duplicate content in algorithm files
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def fix_duplicate_content(file_path: Path) -> bool:
    """Fix duplicate content in file."""
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Check if file is suspiciously large (over 1000 lines)
        if len(lines) > 1000:
            # Find first complete function definition
            first_func_start = None
            for i, line in enumerate(lines):
                if re.match(r'^def\s+\w+\(', line):
                    first_func_start = i
                    break
            
            if first_func_start:
                # Find the first complete implementation (has main and if __name__)
                main_found = False
                name_main_found = False
                end_line = len(lines)
                
                for i in range(first_func_start, len(lines)):
                    if 'if __name__' in lines[i]:
                        name_main_found = True
                        end_line = i + 2  # Include the if __name__ block
                        break
                    if 'def main()' in lines[i]:
                        main_found = True
                
                if name_main_found:
                    # Keep only the first complete implementation
                    fixed_content = '\n'.join(lines[:end_line])
                    file_path.write_text(fixed_content, encoding='utf-8')
                    return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
    return False

def main():
    """Fix all duplicate files."""
    print("Fixing duplicate content in algorithm files...")
    
    fixed_count = 0
    for algo_file in ROOT.rglob("**/algorithm.py"):
        if "supporting_documents" in str(algo_file) or "scripts" in str(algo_file):
            continue
        
        try:
            content = algo_file.read_text(encoding='utf-8')
            if len(content.split('\n')) > 1000:
                if fix_duplicate_content(algo_file):
                    fixed_count += 1
                    if fixed_count % 10 == 0:
                        print(f"Fixed {fixed_count} files...")
        except Exception:
            continue
    
    print(f"\nFixed {fixed_count} files with duplicate content")

if __name__ == "__main__":
    main()

