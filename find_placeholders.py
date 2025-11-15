#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find all placeholder implementations that need to be completed."""

from pathlib import Path
import re

def is_placeholder(file_path: Path) -> bool:
    """Check if file is a placeholder."""
    if not file_path.exists():
        return True
    
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    
    # Too short = placeholder
    if len(lines) < 30:
        return True
    
    # Check for placeholder patterns
    placeholder_patterns = [
        r'print\("==" \* 35\)',
        r'System\.out\.println\("=="\.repeat\(35\)\)',
        r'def \w+\(\):\s*$',
        r'public static void main.*\{\s*$',
    ]
    
    content_lower = content.lower()
    if 'placeholder' in content_lower and len(lines) < 50:
        return True
    
    # Check if it's just printing name and complexity
    if len(lines) < 20 and ('time complexity' in content_lower or 
                            'space complexity' in content_lower):
        return True
    
    return False

def find_all_placeholders():
    """Find all algorithms that need implementation."""
    placeholders = []
    implemented = []
    
    base = Path('.')
    for semester_dir in sorted(base.glob('semester_*')):
        if not semester_dir.is_dir():
            continue
        
        for lecture_dir in sorted(semester_dir.glob('lecture_*')):
            if not lecture_dir.is_dir():
                continue
            
            for algo_dir in sorted(lecture_dir.iterdir()):
                if not algo_dir.is_dir():
                    continue
                
                py_file = algo_dir / 'algorithm.py'
                java_file = algo_dir / 'Algorithm.java'
                
                py_placeholder = is_placeholder(py_file)
                java_placeholder = is_placeholder(java_file)
                
                rel_path = str(algo_dir.relative_to(base))
                
                if py_placeholder and java_placeholder:
                    placeholders.append(rel_path)
                else:
                    implemented.append(rel_path)
    
    return placeholders, implemented

if __name__ == '__main__':
    placeholders, implemented = find_all_placeholders()
    
    print(f"Total algorithms: {len(placeholders) + len(implemented)}")
    print(f"Implemented: {len(implemented)}")
    print(f"Placeholders: {len(placeholders)}")
    print(f"\nPlaceholders needing implementation ({len(placeholders)}):")
    for p in placeholders[:20]:  # Show first 20
        print(f"  {p}")
    if len(placeholders) > 20:
        print(f"  ... and {len(placeholders) - 20} more")

