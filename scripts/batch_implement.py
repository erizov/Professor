#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helper script to get list of all placeholders for batch implementation."""

from pathlib import Path
import re

def is_placeholder(file_path: Path) -> bool:
    """Check if file is a placeholder."""
    if not file_path.exists():
        return True
    
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    
    if len(lines) < 30:
        return True
    
    content_lower = content.lower()
    if 'placeholder' in content_lower and len(lines) < 50:
        return True
    
    if len(lines) < 20 and ('time complexity' in content_lower or 
                            'space complexity' in content_lower):
        return True
    
    return False

def get_all_placeholders():
    """Get all placeholder paths."""
    placeholders = []
    base = Path(__file__).resolve().parents[1]
    
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
                
                if py_placeholder and java_placeholder:
                    placeholders.append(str(algo_dir.relative_to(base)))
    
    return sorted(placeholders)

if __name__ == '__main__':
    placeholders = get_all_placeholders()
    print(f"Total placeholders: {len(placeholders)}")
    for p in placeholders:
        print(p)

