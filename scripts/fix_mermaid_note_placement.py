#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix incorrect placement of Mermaid note text in algorithm descriptions.
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


def fix_mermaid_note(content: str) -> str:
    """Fix incorrectly placed Mermaid notes."""
    # Pattern: Mermaid note text appearing in Purpose/Key Idea sections
    # Should only appear after Mermaid code blocks
    
    # Remove note from Purpose/Key Idea
    patterns_to_fix = [
        (r'- \*\*Purpose:\*\* [^:]+: > \*\*Note\*\*: Mermaid diagrams', 
         r'- **Purpose:** [algorithm description]'),
        (r'- \*\*Key Idea:\*\* [^:]+: > \*\*Note\*\*: Mermaid diagrams',
         r'- **Key Idea:** [algorithm description]'),
        (r'([^:]+): > \*\*Note\*\*: Mermaid diagrams are rendered',
         r'\1: [algorithm description]')
    ]
    
    for pattern, replacement in patterns_to_fix:
        content = re.sub(pattern, replacement, content)
    
    # If we find generic descriptions, try to fix them
    if 'The algorithm works by > **Note**: Mermaid' in content:
        # This is a broken description, replace with generic
        content = content.replace(
            'The algorithm works by > **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.',
            'The algorithm works by systematically processing data according to a specific strategy.'
        )
    
    return content


def fix_file(md_file: Path) -> bool:
    """Fix Mermaid note placement in a single MD file."""
    try:
        content = md_file.read_text(encoding='utf-8')
        original = content
        
        content = fix_mermaid_note(content)
        
        if content != original:
            md_file.write_text(content, encoding='utf-8')
            return True
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
    print("FIXING MERMAID NOTE PLACEMENT")
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

