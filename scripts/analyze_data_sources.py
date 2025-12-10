#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze what data sources are actually available for algorithms.
Shows where we're getting (or not getting) algorithm-specific data.
"""

import sys
import json
import ast
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def analyze_algorithm_folder(algorithm_folder: Path) -> dict:
    """Analyze what data is available in an algorithm folder."""
    result = {
        'name': algorithm_folder.name,
        'has_metadata': False,
        'has_readme': False,
        'has_algorithm_py': False,
        'metadata_complexity': None,
        'docstring_complexity': None,
        'readme_description': False,
        'readme_use_cases': False,
    }
    
    # Check metadata.json
    metadata_path = algorithm_folder / "metadata.json"
    if metadata_path.exists():
        result['has_metadata'] = True
        try:
            metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
            if 'complexity' in metadata:
                if isinstance(metadata['complexity'], dict):
                    result['metadata_complexity'] = {
                        'time': metadata['complexity'].get('time'),
                        'space': metadata['complexity'].get('space')
                    }
        except Exception:
            pass
    
    # Check algorithm.py
    code_path = algorithm_folder / "algorithm.py"
    if code_path.exists():
        result['has_algorithm_py'] = True
        try:
            code = code_path.read_text(encoding='utf-8')
            # Check for complexity in docstrings
            docstring_pattern = r'"""(.*?)"""'
            docstrings = re.findall(docstring_pattern, code, re.DOTALL)
            for doc in docstrings:
                if 'Time Complexity' in doc or 'Space Complexity' in doc:
                    time_match = re.search(r'Time Complexity[:\s]+O\([^)]+\)', doc, re.IGNORECASE)
                    space_match = re.search(r'Space Complexity[:\s]+O\([^)]+\)', doc, re.IGNORECASE)
                    if time_match or space_match:
                        result['docstring_complexity'] = {
                            'time': time_match.group() if time_match else None,
                            'space': space_match.group() if space_match else None
                        }
                        break
        except Exception:
            pass
    
    # Check README.md
    readme_path = algorithm_folder / "README.md"
    if readme_path.exists():
        result['has_readme'] = True
        try:
            content = readme_path.read_text(encoding='utf-8')
            # Check for description (non-flowchart text)
            lines = content.split('\n')
            for line in lines[:50]:
                if (len(line.strip()) > 50 and 
                    not line.strip().startswith('#') and
                    not '┌' in line and not '│' in line and
                    not 'flowchart' in line.lower()):
                    result['readme_description'] = True
                    break
            
            # Check for use cases
            if 'Real-World Applications' in content or "Where It's Used" in content:
                result['readme_use_cases'] = True
        except Exception:
            pass
    
    return result


def main():
    """Analyze data sources across all algorithms."""
    print("="*70)
    print("ANALYZING DATA SOURCES FOR ALGORITHMS")
    print("="*70)
    print()
    
    stats = {
        'total': 0,
        'has_metadata': 0,
        'has_readme': 0,
        'has_algorithm_py': 0,
        'metadata_has_complexity': 0,
        'docstring_has_complexity': 0,
        'readme_has_description': 0,
        'readme_has_use_cases': 0,
    }
    
    # Sample algorithms from different semesters
    sample_folders = []
    for semester in range(1, 6):
        semester_path = ROOT / f"semester_{semester:02d}"
        if semester_path.exists():
            for lecture_path in semester_path.glob("lecture_*"):
                for algo_folder in lecture_path.glob("*"):
                    if algo_folder.is_dir() and not algo_folder.name.startswith('.'):
                        sample_folders.append(algo_folder)
                        if len(sample_folders) >= 20:  # Sample 20 algorithms
                            break
                if len(sample_folders) >= 20:
                    break
        if len(sample_folders) >= 20:
            break
    
    print(f"Analyzing {len(sample_folders)} sample algorithms...\n")
    
    for algo_folder in sample_folders:
        result = analyze_algorithm_folder(algo_folder)
        stats['total'] += 1
        
        if result['has_metadata']:
            stats['has_metadata'] += 1
            if result['metadata_complexity']:
                stats['metadata_has_complexity'] += 1
        
        if result['has_readme']:
            stats['has_readme'] += 1
            if result['readme_description']:
                stats['readme_has_description'] += 1
            if result['readme_use_cases']:
                stats['readme_has_use_cases'] += 1
        
        if result['has_algorithm_py']:
            stats['has_algorithm_py'] += 1
            if result['docstring_complexity']:
                stats['docstring_has_complexity'] += 1
    
    print("="*70)
    print("DATA SOURCE STATISTICS")
    print("="*70)
    print(f"Total algorithms analyzed: {stats['total']}")
    print()
    print(f"metadata.json:")
    print(f"  - Exists: {stats['has_metadata']}/{stats['total']} ({100*stats['has_metadata']/stats['total']:.1f}%)")
    print(f"  - Has complexity: {stats['metadata_has_complexity']}/{stats['has_metadata']} ({100*stats['metadata_has_complexity']/max(stats['has_metadata'],1):.1f}%)")
    print()
    print(f"algorithm.py:")
    print(f"  - Exists: {stats['has_algorithm_py']}/{stats['total']} ({100*stats['has_algorithm_py']/stats['total']:.1f}%)")
    print(f"  - Has complexity in docstrings: {stats['docstring_has_complexity']}/{stats['has_algorithm_py']} ({100*stats['docstring_has_complexity']/max(stats['has_algorithm_py'],1):.1f}%)")
    print()
    print(f"README.md:")
    print(f"  - Exists: {stats['has_readme']}/{stats['total']} ({100*stats['has_readme']/stats['total']:.1f}%)")
    print(f"  - Has description: {stats['readme_has_description']}/{stats['has_readme']} ({100*stats['readme_has_description']/max(stats['has_readme'],1):.1f}%)")
    print(f"  - Has use cases: {stats['readme_has_use_cases']}/{stats['has_readme']} ({100*stats['readme_has_use_cases']/max(stats['has_readme'],1):.1f}%)")
    print()
    print("="*70)
    print("CONCLUSION")
    print("="*70)
    print("This shows what data sources are ACTUALLY available.")
    print("If sources don't exist or don't have data, we can't extract it!")
    print("We need to either:")
    print("  1. Use what's available (metadata, docstrings, README)")
    print("  2. Generate content using Cursor AI based on code analysis")
    print("  3. Use algorithm name patterns to infer (fallback)")


if __name__ == "__main__":
    main()

