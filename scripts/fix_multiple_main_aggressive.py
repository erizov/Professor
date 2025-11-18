#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix multiple main() functions - Aggressive version
Remove all duplicates, keep only first complete implementation
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def fix_multiple_main_aggressive(file_path: Path) -> bool:
    """Aggressively fix files with multiple main() functions."""
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # Count main() functions
        main_count = len([line for line in lines if re.match(r'^\s*def\s+main\s*\(', line)])
        
        if main_count <= 1:
            return False  # No issue
        
        # Find the first function definition
        first_func_start = None
        for i, line in enumerate(lines):
            if re.match(r'^\s*def\s+\w+\(', line):
                first_func_start = i
                break
        
        if first_func_start is None:
            return False
        
        # Find the first complete implementation ending with if __name__
        if_name_pos = None
        for i in range(first_func_start, len(lines)):
            if 'if __name__' in lines[i]:
                if_name_pos = i
                break
        
        if if_name_pos is None:
            # No if __name__, find end of first main()
            # Look for second def or end of file
            first_main_end = len(lines)
            for i in range(first_func_start + 1, len(lines)):
                if re.match(r'^\s*def\s+\w+\s*\(', lines[i]):
                    # Check if this is a duplicate
                    if i > first_func_start + 50:  # Reasonable function size
                        first_main_end = i
                        break
            
            # Keep up to first main end, add if __name__
            new_lines = lines[:first_main_end]
            new_lines.append('')
            new_lines.append('if __name__ == "__main__":')
            new_lines.append('    main()')
        else:
            # Keep everything up to and including if __name__
            new_lines = lines[:if_name_pos + 2]  # Include if __name__ and main() call
        
        # Clean up: remove excessive blank lines
        cleaned_lines = []
        prev_blank = False
        for line in new_lines:
            is_blank = not line.strip()
            if is_blank and prev_blank:
                continue  # Skip consecutive blank lines
            cleaned_lines.append(line)
            prev_blank = is_blank
        
        # Ensure we end with exactly one blank line
        while cleaned_lines and not cleaned_lines[-1].strip():
            cleaned_lines.pop()
        cleaned_lines.append('')
        
        fixed_content = '\n'.join(cleaned_lines)
        
        # Only write if content changed significantly
        if len(fixed_content.split('\n')) < len(lines) * 0.9:  # At least 10% reduction
            file_path.write_text(fixed_content, encoding='utf-8')
            return True
        
        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False


def main():
    """Fix all files with multiple main() functions."""
    print("=" * 70)
    print("Fix Multiple main() Functions - Aggressive")
    print("=" * 70)
    
    fixed_count = 0
    total_files = 0
    multiple_main_count = 0
    
    for algo_file in ROOT.rglob("**/algorithm.py"):
        if "supporting_documents" in str(algo_file) or "scripts" in str(algo_file):
            continue
        
        total_files += 1
        try:
            content = algo_file.read_text(encoding='utf-8')
            main_count = len(re.findall(r'^\s*def\s+main\s*\(', content, re.MULTILINE))
            
            if main_count > 1 or len(content.split('\n')) > 500:  # Also fix very long files
                multiple_main_count += 1
                if fix_multiple_main_aggressive(algo_file):
                    fixed_count += 1
                    if fixed_count % 50 == 0:
                        print(f"Fixed {fixed_count} files...")
        except Exception:
            continue
    
    print(f"\n[COMPLETE] Scanned {total_files} files")
    print(f"Files with multiple main() or excessive length: {multiple_main_count}")
    print(f"Files fixed: {fixed_count}")


if __name__ == "__main__":
    main()

