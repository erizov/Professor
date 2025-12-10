#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive fix for all placeholders and issues:
- Fix duplicate text patterns
- Add missing solutions to Common Mistakes
- Clean up generic descriptions
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def fix_duplicate_text(content: str, algorithm_name: str) -> str:
    """Fix duplicate/repetitive text patterns."""
    readable_name = algorithm_name.replace('_', ' ').title()
    
    # Pattern: "Algorithm Name: Algorithm Name is..."
    pattern1 = re.compile(
        re.escape(readable_name) + r':\s+' + re.escape(readable_name) + r'\s+is',
        re.IGNORECASE
    )
    content = pattern1.sub(f"{readable_name} is", content)
    
    # Pattern: Remove trailing double periods
    content = re.sub(r'\.\.+', '.', content)
    
    # Pattern: "Algorithm Name: Algorithm Name:" (double colon)
    pattern2 = re.compile(
        re.escape(readable_name) + r':\s+' + re.escape(readable_name) + r':',
        re.IGNORECASE
    )
    content = pattern2.sub(f"{readable_name}:", content)
    
    return content


def get_mistake_solution(algorithm_name: str, mistake_text: str) -> str:
    """Get solution for a mistake."""
    name_lower = algorithm_name.lower()
    mistake_lower = mistake_text.lower()
    
    # Specific solutions
    if 'edge case' in mistake_lower or 'empty' in mistake_lower or 'boundary' in mistake_lower:
        return "Add validation: `if not data or len(data) <= 1: return data`"
    elif 'trace' in mistake_lower or 'step-by-step' in mistake_lower:
        return "Manually trace through a small example (3-5 elements) to verify each step matches the algorithm logic"
    elif 'debug' in mistake_lower or 'verify' in mistake_lower:
        return "Use print statements or debugger to check variable values at each step, compare with expected behavior"
    elif 'review' in mistake_lower or 'key steps' in mistake_lower:
        return "Study the algorithm's pseudocode or description, identify the core steps, then implement one step at a time"
    elif 'complexity' in mistake_lower:
        return "Understand time/space complexity - choose appropriate algorithm for your data size and constraints"
    else:
        return "Review the algorithm's core steps, test with known examples, and use debugging tools to verify correctness"


def fix_missing_solutions(content: str, algorithm_name: str) -> str:
    """Add missing solutions to Common Mistakes."""
    if "## Common Mistakes" not in content:
        return content
    
    mistakes_start = content.find("## Common Mistakes")
    next_section = content.find("\n## ", mistakes_start + 1)
    if next_section == -1:
        mistakes_section = content[mistakes_start:]
        rest = ""
    else:
        mistakes_section = content[mistakes_start:next_section]
        rest = content[next_section:]
    
    lines = mistakes_section.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a mistake header
        if "### ❌ Mistake" in line:
            mistake_text = line
            fixed_lines.append(line)
            i += 1
            
            # Check if next line has solution
            has_solution = False
            if i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith("**Solution:**"):
                    solution_text = next_line[len("**Solution:**"):].strip()
                    if solution_text and "[How to fix" not in solution_text:
                        # Valid solution exists
                        fixed_lines.append(lines[i])
                        i += 1
                        has_solution = True
                        continue
            
            # No solution found, add one
            if not has_solution:
                solution = get_mistake_solution(algorithm_name, mistake_text)
                fixed_lines.append(f"**Solution:** {solution}")
                fixed_lines.append("")
                # Skip empty lines
                while i < len(lines) and not lines[i].strip():
                    i += 1
        else:
            fixed_lines.append(line)
            i += 1
    
    return content[:mistakes_start] + '\n'.join(fixed_lines) + rest


def fix_file(md_file: Path) -> bool:
    """Fix all issues in a single MD file."""
    try:
        content = md_file.read_text(encoding='utf-8')
        
        # Get algorithm name
        algorithm_folder = md_file.parent
        algorithm_name = algorithm_folder.name
        
        # Apply fixes
        content = fix_duplicate_text(content, algorithm_name)
        content = fix_missing_solutions(content, algorithm_name)
        
        md_file.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"  [ERROR] {md_file.name}: {e}")
        return False


def find_all_md_files() -> list:
    """Find all algorithm MD files."""
    md_files = []
    
    for md_file in ROOT.glob("semester_*/lecture_*/*/school.*.md"):
        md_files.append(md_file)
    
    for md_file in ROOT.glob("semester_*/lecture_*/*/univer.*.md"):
        md_files.append(md_file)
    
    return sorted(md_files)


def main() -> int:
    """Main execution."""
    print("="*70)
    print("COMPREHENSIVE FIX FOR PLACEHOLDERS AND ISSUES")
    print("="*70)
    
    md_files = find_all_md_files()
    print(f"\nFound {len(md_files)} MD files")
    print("\nFixing:")
    print("  - Duplicate text patterns")
    print("  - Missing solutions in Common Mistakes")
    print("  - Trailing periods and formatting issues")
    
    fixed = 0
    errors = 0
    
    for i, md_file in enumerate(md_files, 1):
        if fix_file(md_file):
            fixed += 1
        else:
            errors += 1
        
        if i % 500 == 0:
            print(f"Progress: {i}/{len(md_files)} ({i/len(md_files)*100:.1f}%)")
    
    print(f"\n{'='*70}")
    print(f"Fixed: {fixed}/{len(md_files)} files")
    print(f"Errors: {errors}")
    print(f"{'='*70}")
    
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

