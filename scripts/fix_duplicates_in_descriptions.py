#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix duplicate sections in enhanced algorithm descriptions.
"""

import sys
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def remove_duplicate_sections(content: str) -> str:
    """Remove duplicate sections from content."""
    lines = content.split('\n')
    seen_sections = set()
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a section header
        if line.startswith('## '):
            section_name = line.strip()
            
            # Check if we've seen this section before
            if section_name in seen_sections:
                # Skip this section and its content until next section or end
                i += 1
                while i < len(lines):
                    if lines[i].startswith('## ') or lines[i].strip() == '':
                        break
                    i += 1
                continue
            else:
                seen_sections.add(section_name)
        
        result.append(line)
        i += 1
    
    # Also remove duplicate Quick Summary bullet points
    content = '\n'.join(result)
    
    # Remove duplicate bullet points in Quick Summary
    if '## 📋 Quick Summary' in content:
        summary_start = content.find('## 📋 Quick Summary')
        summary_end = content.find('\n## ', summary_start + 1)
        if summary_end == -1:
            summary_end = len(content)
        
        summary_section = content[summary_start:summary_end]
        lines = summary_section.split('\n')
        seen_bullets = set()
        unique_lines = []
        
        for line in lines:
            if line.strip().startswith('- **'):
                if line.strip() not in seen_bullets:
                    seen_bullets.add(line.strip())
                    unique_lines.append(line)
                else:
                    continue
            else:
                unique_lines.append(line)
        
        content = content[:summary_start] + '\n'.join(unique_lines) + content[summary_end:]
    
    return content


def fix_file(filepath: Path) -> bool:
    """Fix duplicates in a single file."""
    try:
        content = filepath.read_text(encoding='utf-8')
        fixed = remove_duplicate_sections(content)
        filepath.write_text(fixed, encoding='utf-8')
        return True
    except Exception as e:
        print(f"  [ERROR] {filepath.name}: {e}")
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
    print("FIXING DUPLICATE SECTIONS IN ALGORITHM DESCRIPTIONS")
    print("="*70)
    
    md_files = find_all_md_files()
    print(f"\nFound {len(md_files)} MD files")
    
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

