#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced algorithm information extraction.
Extracts from metadata.json, algorithm.py, README.md, and docstrings.
"""

import sys
import re
import json
import ast
from pathlib import Path
from typing import Dict, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def extract_description_from_readme(readme_path: Path) -> str:
    """Extract description from README.md, skipping flowcharts."""
    if not readme_path.exists():
        return ""
    
    try:
        content = readme_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        description_parts = []
        
        # Skip title and find first meaningful paragraph
        found_title = False
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Skip empty lines
            if not line_stripped:
                continue
            
            # Mark when we find title
            if line_stripped.startswith('#') and len(line_stripped) <= 50:
                found_title = True
                continue
            
            # Skip markdown elements and flowcharts
            if (line_stripped.startswith('-') or 
                line_stripped.startswith('*') or
                line_stripped.startswith('[') or
                line_stripped.startswith('!') or
                '```' in line_stripped or
                '┌' in line_stripped or
                '│' in line_stripped or
                'flowchart' in line_stripped.lower()):
                continue
            
            # Collect meaningful description (after title or in first 30 lines)
            if (found_title or i < 30) and len(line_stripped) > 30:
                if not line_stripped.startswith('##'):
                    description_parts.append(line_stripped)
                    if len(description_parts) >= 2:  # Get first 2 paragraphs
                        break
        
        return ' '.join(description_parts) if description_parts else ""
    except Exception:
        return ""


def extract_complexity_from_docstring(code: str) -> Tuple[str, str]:
    """Extract complexity from docstrings in algorithm.py."""
    time_complexity = None
    space_complexity = None
    
    # Find all docstrings
    docstring_pattern = r'"""(.*?)"""'
    docstrings = re.findall(docstring_pattern, code, re.DOTALL)
    
    for doc in docstrings:
        # Time complexity patterns
        time_patterns = [
            r'Time Complexity[:\s]+O\([^)]+\)',
            r'Time[:\s]+O\([^)]+\)',
            r'O\([^)]+\)[^\n]*time',
            r'complexity[^\n]*O\([^)]+\)'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, doc, re.IGNORECASE)
            if match:
                comp_match = re.search(r'O\([^)]+\)', match.group())
                if comp_match:
                    time_complexity = comp_match.group()
                    break
        
        # Space complexity patterns
        space_patterns = [
            r'Space Complexity[:\s]+O\([^)]+\)',
            r'Space[:\s]+O\([^)]+\)',
            r'O\([^)]+\)[^\n]*space',
            r'memory[^\n]*O\([^)]+\)'
        ]
        
        for pattern in space_patterns:
            match = re.search(pattern, doc, re.IGNORECASE)
            if match:
                comp_match = re.search(r'O\([^)]+\)', match.group())
                if comp_match:
                    space_complexity = comp_match.group()
                    break
        
        if time_complexity and space_complexity:
            break
    
    return time_complexity, space_complexity


def extract_use_cases_from_readme(readme_path: Path) -> list:
    """Extract use cases from README.md."""
    if not readme_path.exists():
        return []
    
    try:
        content = readme_path.read_text(encoding='utf-8')
        use_cases = []
        
        # Look for "Real-World Applications" or "Where It's Used" sections
        sections = [
            r'## Real-World Applications\s*\n(.*?)(?=\n##|\Z)',
            r'## Where It\'s Used\s*\n(.*?)(?=\n##|\Z)',
            r'## Применение\s*\n(.*?)(?=\n##|\Z)',
        ]
        
        for pattern in sections:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                section_content = match.group(1)
                # Extract list items
                items = re.findall(r'[-*]\s+(.+?)(?:\n|$)', section_content)
                use_cases.extend([item.strip() for item in items if len(item.strip()) > 10])
                if use_cases:
                    break
        
        return use_cases[:5]  # Return first 5
    except Exception:
        return []


def analyze_algorithm_type(code: str, algorithm_name: str) -> Dict:
    """Analyze code to understand algorithm type and approach."""
    analysis = {
        'type': 'unknown',
        'data_structures': [],
        'key_operations': []
    }
    
    name_lower = algorithm_name.lower()
    
    # Determine type from name
    if 'sort' in name_lower:
        analysis['type'] = 'sorting'
    elif 'search' in name_lower:
        analysis['type'] = 'searching'
    elif 'graph' in name_lower or 'dfs' in name_lower or 'bfs' in name_lower:
        analysis['type'] = 'graph'
    elif 'tree' in name_lower or 'heap' in name_lower:
        analysis['type'] = 'tree'
    elif 'hash' in name_lower:
        analysis['type'] = 'hashing'
    elif 'dynamic' in name_lower or 'dp' in name_lower:
        analysis['type'] = 'dynamic_programming'
    elif 'greedy' in name_lower:
        analysis['type'] = 'greedy'
    
    # Analyze code for data structures
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = getattr(node.func, 'id', '')
                if 'List' in str(node) or 'list' in func_name.lower():
                    if 'List' not in analysis['data_structures']:
                        analysis['data_structures'].append('List')
                if 'Dict' in str(node) or 'dict' in func_name.lower() or 'Map' in str(node):
                    if 'Dictionary' not in analysis['data_structures']:
                        analysis['data_structures'].append('Dictionary')
                if 'Set' in str(node) or 'set' in func_name.lower():
                    if 'Set' not in analysis['data_structures']:
                        analysis['data_structures'].append('Set')
                if 'Queue' in str(node) or 'queue' in func_name.lower():
                    if 'Queue' not in analysis['data_structures']:
                        analysis['data_structures'].append('Queue')
    except Exception:
        pass
    
    return analysis


def enhanced_extract_algorithm_info(algorithm_folder: Path) -> Dict:
    """Enhanced extraction from all available sources."""
    info = {
        'name': algorithm_folder.name,
        'category': 'Algorithms',
        'description': '',
        'time_complexity': 'Varies',
        'space_complexity': 'Varies',
        'functions': [],
        'class_name': None,
        'use_cases': [],
        'algorithm_type': 'unknown',
        'data_structures': []
    }
    
    # 1. Read metadata.json
    metadata_path = algorithm_folder / "metadata.json"
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
            info.update(metadata)
            
            # Handle nested complexity structure
            if 'complexity' in metadata and isinstance(metadata['complexity'], dict):
                if 'time' in metadata['complexity']:
                    info['time_complexity'] = metadata['complexity']['time']
                if 'space' in metadata['complexity']:
                    info['space_complexity'] = metadata['complexity']['space']
        except Exception:
            pass
    
    # 2. Read algorithm.py for code structure and docstrings
    code_path = algorithm_folder / "algorithm.py"
    if code_path.exists():
        try:
            code = code_path.read_text(encoding='utf-8')
            tree = ast.parse(code)
            
            # Extract class and function names
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    info['class_name'] = node.name
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            info['functions'].append(item.name)
                elif isinstance(node, ast.FunctionDef):
                    info['functions'].append(node.name)
            
            # Extract complexity from docstrings
            time_comp, space_comp = extract_complexity_from_docstring(code)
            if time_comp:
                info['time_complexity'] = time_comp
            if space_comp:
                info['space_complexity'] = space_comp
            
            # Analyze algorithm type
            analysis = analyze_algorithm_type(code, algorithm_folder.name)
            info.update(analysis)
        except Exception:
            pass
    
    # 3. Read README.md for descriptions and use cases
    readme_path = algorithm_folder / "README.md"
    if readme_path.exists():
        # Extract description
        description = extract_description_from_readme(readme_path)
        if description:
            info['description'] = description
        
        # Extract use cases
        use_cases = extract_use_cases_from_readme(readme_path)
        if use_cases:
            info['use_cases'] = use_cases
    
    return info


def main():
    """Test the enhanced extraction."""
    # Test with bubble_sort
    test_folder = ROOT / "semester_01" / "lecture_01_sorting_fundamentals" / "bubble_sort"
    
    if test_folder.exists():
        info = enhanced_extract_algorithm_info(test_folder)
        print("Enhanced Algorithm Info Extraction Test")
        print("=" * 70)
        print(f"Algorithm: {info['name']}")
        print(f"Category: {info['category']}")
        print(f"Time Complexity: {info['time_complexity']}")
        print(f"Space Complexity: {info['space_complexity']}")
        print(f"Description: {info['description'][:100]}..." if info['description'] else "Description: (none)")
        print(f"Use Cases: {info['use_cases']}")
        print(f"Algorithm Type: {info['algorithm_type']}")
        print(f"Data Structures: {info['data_structures']}")
        print(f"Class: {info['class_name']}")
        print(f"Functions: {info['functions']}")
    else:
        print(f"Test folder not found: {test_folder}")


if __name__ == "__main__":
    main()

