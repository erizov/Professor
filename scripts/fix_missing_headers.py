#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix missing section headers in algorithm descriptions.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def fix_missing_headers(content: str) -> str:
    """Fix missing section headers."""
    lines = content.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this looks like Quick Summary content without header
        if (line.strip().startswith('- **Purpose:**') and 
            i > 0 and not lines[i-1].strip().startswith('## 📋 Quick Summary')):
            # Add Quick Summary header
            result.append('## 📋 Quick Summary')
            result.append('')
        
        # Check if this looks like "In One Sentence" content without header
        if (line.strip() and 
            not line.strip().startswith('#') and 
            not line.strip().startswith('-') and
            not line.strip().startswith('**') and
            i > 0 and 
            '## 📋 Quick Summary' in '\n'.join(result[-10:]) and
            '## 💬 In One Sentence' not in '\n'.join(result[-10:])):
            # Check if next few lines suggest this is "In One Sentence"
            if i < len(lines) - 1:
                next_line = lines[i+1].strip()
                if (next_line.startswith('The ') or 
                    next_line.startswith('This ') or
                    (len(line.strip()) > 30 and len(line.strip()) < 200)):
                    result.append('## 💬 In One Sentence')
                    result.append('')
        
        result.append(line)
        i += 1
    
    # Fix: If Quick Summary content exists but no header, add it
    content_str = '\n'.join(result)
    if '- **Purpose:**' in content_str and '## 📋 Quick Summary' not in content_str:
        # Find where Purpose line is
        lines = content_str.split('\n')
        new_lines = []
        for i, line in enumerate(lines):
            if line.strip().startswith('- **Purpose:**') and i > 0:
                # Check if previous line is not the header
                if not (i > 0 and lines[i-1].strip() == '## 📋 Quick Summary'):
                    new_lines.append('## 📋 Quick Summary')
                    new_lines.append('')
            new_lines.append(line)
        content_str = '\n'.join(new_lines)
    
    return content_str


def fix_file(filepath: Path) -> bool:
    """Fix missing headers in a single file."""
    try:
        content = filepath.read_text(encoding='utf-8')
        
        # Quick fix: if Quick Summary content exists without header, add it
        if '- **Purpose:**' in content and '## 📋 Quick Summary' not in content:
            lines = content.split('\n')
            new_lines = []
            found_purpose = False
            
            for i, line in enumerate(lines):
                if line.strip().startswith('- **Purpose:**') and not found_purpose:
                    # Add header before this line (but don't add title if it already exists)
                    if i == 0 or not lines[i-1].strip().startswith('#'):
                        # Title might be missing, but let's not add it here
                        pass
                    new_lines.append('## 📋 Quick Summary')
                    new_lines.append('')
                    found_purpose = True
                new_lines.append(line)
            
            content = '\n'.join(new_lines)
        
        # Remove extra "# School" or "# Univer" headers that might have been added
        lines = content.split('\n')
        new_lines = []
        for i, line in enumerate(lines):
            # Skip standalone "# School" or "# Univer" that appear after title
            if (line.strip() in ['# School', '# Univer'] and 
                i > 0 and lines[i-1].strip().startswith('# ') and 
                'Bubble' in lines[i-1] or 'Sort' in lines[i-1] or 'Algorithm' in lines[i-1]):
                continue
            new_lines.append(line)
        content = '\n'.join(new_lines)
        else:
            content = fix_missing_headers(content)
        
        filepath.write_text(content, encoding='utf-8')
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
    print("FIXING MISSING SECTION HEADERS")
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

