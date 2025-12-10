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
    in_section = False
    current_section = None
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a section header
        if line.startswith('## '):
            section_name = line.strip()
            
            # Check if we've seen this section before
            if section_name in seen_sections:
                # Skip this entire section
                in_section = True
                current_section = section_name
                i += 1
                # Skip until next section or significant blank line
                while i < len(lines):
                    if lines[i].startswith('## '):
                        break
                    # Stop at significant blank (2+ newlines or section break)
                    if i < len(lines) - 1 and lines[i].strip() == '' and lines[i+1].strip() == '':
                        i += 1
                        break
                    i += 1
                in_section = False
                current_section = None
                continue
            else:
                seen_sections.add(section_name)
                in_section = True
                current_section = section_name
        
        # Also check for duplicate content patterns
        line_stripped = line.strip()
        
        # Skip duplicate bullet points (same content)
        if line_stripped.startswith('- **'):
            # Check if we've seen this exact bullet recently
            if line_stripped in [r.strip() for r in result[-20:] if r.strip().startswith('- **')]:
                i += 1
                continue
        
        # Skip duplicate standalone lines (same content repeated)
        if line_stripped and not line_stripped.startswith('#') and not line_stripped.startswith('-'):
            # Check last 10 lines for duplicates
            recent_lines = [r.strip() for r in result[-10:] if r.strip() and not r.strip().startswith('#')]
            if line_stripped in recent_lines:
                i += 1
                continue
        
        result.append(line)
        i += 1
    
    content = '\n'.join(result)
    
    # Additional cleanup: remove duplicate Quick Summary sections
    if content.count('## 📋 Quick Summary') > 1:
        parts = content.split('## 📋 Quick Summary')
        # Keep first occurrence, remove others
        content = parts[0] + '## 📋 Quick Summary' + parts[1]
        # Remove any remaining duplicates
        while '## 📋 Quick Summary' in content[content.find('## 📋 Quick Summary') + 1:]:
            first = content.find('## 📋 Quick Summary')
            second = content.find('## 📋 Quick Summary', first + 1)
            next_section = content.find('\n## ', second)
            if next_section == -1:
                content = content[:second]
            else:
                content = content[:second] + content[next_section:]
    
    # Remove duplicate "In One Sentence", "Key Insight", "Memory Tip" sections
    for section in ['## 💬 In One Sentence', '## 💡 Key Insight', '## 🧠 Memory Tip']:
        if content.count(section) > 1:
            parts = content.split(section)
            # Keep first, remove others
            new_content = parts[0] + section + parts[1]
            # Remove remaining
            for part in parts[2:]:
                next_section = part.find('\n## ')
                if next_section != -1:
                    new_content += part[next_section:]
                else:
                    new_content += part
            content = new_content
    
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

