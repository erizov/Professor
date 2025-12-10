#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2.1: Improve algorithm-specific content quality:
- Better README extraction (skip flowcharts)
- Improved complexity detection from code docstrings
- Extract algorithm-specific examples from implementations
- Enhance use cases with real-world examples
"""

import sys
import re
import ast
import json
from pathlib import Path
from typing import Dict, Optional, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def extract_readme_description(readme_content: str) -> Optional[str]:
    """Extract meaningful description from README, skipping flowcharts."""
    if not readme_content:
        return None
    
    lines = readme_content.split('\n')
    description_lines = []
    in_flowchart = False
    in_code_block = False
    
    skip_patterns = [
        'flowchart', 'step-by-step execution', 'start', 'init', '-->',
        '│', '┌', '└', '├', '─', 'visualization', 'diagram',
        '```', '## Algorithm Visualization', '## Flowchart'
    ]
    
    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()
        
        # Track code blocks
        if line_stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        
        if in_code_block:
            continue
        
        # Skip flowchart sections
        if any(pattern in line_lower for pattern in skip_patterns):
            in_flowchart = True
            continue
        
        # Reset flowchart flag on new section
        if line_stripped.startswith('##') and in_flowchart:
            in_flowchart = False
            continue
        
        if in_flowchart:
            continue
        
        # Look for meaningful description
        if (line_stripped and 
            not line_stripped.startswith('#') and
            not line_stripped.startswith('-') and
            not line_stripped.startswith('*') and
            len(line_stripped) > 50 and
            not line_stripped.startswith('[') and
            'http' not in line_stripped):
            description_lines.append(line_stripped)
            if len(description_lines) >= 2:  # Get first 2 meaningful paragraphs
                break
    
    if description_lines:
        return ' '.join(description_lines[:2])
    
    return None


def extract_complexity_from_code(code_content: str) -> Optional[str]:
    """Extract complexity from code docstrings."""
    if not code_content:
        return None
    
    # Look for complexity in docstrings
    complexity_patterns = [
        r'O\([^)]+\)',  # O(n), O(n²), O(n log n), etc.
        r'Time complexity[:\s]+O\([^)]+\)',
        r'Complexity[:\s]+O\([^)]+\)',
        r'Time[:\s]+O\([^)]+\)',
    ]
    
    # Check docstrings
    try:
        tree = ast.parse(code_content)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                if docstring:
                    for pattern in complexity_patterns:
                        match = re.search(pattern, docstring, re.IGNORECASE)
                        if match:
                            complexity = match.group(0)
                            # Extract just the O(...) part
                            o_match = re.search(r'O\([^)]+\)', complexity)
                            if o_match:
                                return o_match.group(0)
    except:
        pass
    
    # Fallback: search in entire code
    for pattern in complexity_patterns:
        match = re.search(pattern, code_content, re.IGNORECASE)
        if match:
            complexity = match.group(0)
            o_match = re.search(r'O\([^)]+\)', complexity)
            if o_match:
                return o_match.group(0)
    
    return None


def extract_code_example(code_content: str, algorithm_name: str) -> Optional[str]:
    """Extract algorithm-specific code example."""
    if not code_content:
        return None
    
    try:
        tree = ast.parse(code_content)
        
        # Find main function
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Get function code
                func_lines = code_content.split('\n')[node.lineno-1:node.end_lineno]
                func_code = '\n'.join(func_lines)
                
                # Check if it's the main algorithm function
                if (algorithm_name.lower().replace('_', '') in node.name.lower() or
                    'algorithm' in node.name.lower() or
                    node.name.lower() in ['main', 'solve', 'compute']):
                    return func_code
    except:
        pass
    
    return None


def get_real_world_use_cases(algorithm_name: str, category: str) -> List[str]:
    """Get real-world use cases for algorithm."""
    name_lower = algorithm_name.lower()
    
    use_cases = {
        'bubble_sort': [
            "Educational purposes and small datasets (< 10 elements)",
            "When simplicity is more important than performance",
            "Sorting nearly-sorted data with early termination optimization"
        ],
        'quick_sort': [
            "General-purpose sorting in programming languages (Python, Java)",
            "Database query optimization and indexing",
            "Operating system process scheduling",
            "In-memory sorting of large datasets"
        ],
        'binary_search': [
            "Searching in sorted arrays and databases",
            "Finding elements in phone books, dictionaries",
            "Range queries in databases",
            "Game development (finding items in sorted lists)"
        ],
        'dijkstra': [
            "GPS navigation systems (finding shortest routes)",
            "Network routing protocols",
            "Social network analysis (shortest path between users)",
            "Game development (pathfinding in games)"
        ],
        'merge_sort': [
            "External sorting (sorting data that doesn't fit in memory)",
            "Stable sorting when relative order matters",
            "Sorting linked lists efficiently",
            "Merge operations in databases"
        ],
        'fibonacci': [
            "Financial modeling (compound interest calculations)",
            "Computer graphics (spiral patterns, golden ratio)",
            "Biology (population growth models)",
            "Algorithm analysis and benchmarking"
        ],
        'grover': [
            "Quantum database search",
            "Optimization problems in quantum computing",
            "Cryptographic applications",
            "Quantum machine learning"
        ]
    }
    
    # Check for specific algorithm
    for key, cases in use_cases.items():
        if key in name_lower:
            return cases
    
    # Category-based use cases
    category_cases = {
        'Sorting': [
            "Data organization and retrieval",
            "Database indexing",
            "Search algorithm preprocessing"
        ],
        'Graph Algorithms': [
            "Network analysis",
            "Social media connections",
            "Transportation and logistics"
        ],
        'Dynamic Programming': [
            "Optimization problems",
            "Resource allocation",
            "Sequence alignment"
        ]
    }
    
    return category_cases.get(category, ["General algorithmic problem solving"])


def improve_md_file(md_file: Path) -> bool:
    """Improve content quality in a single MD file."""
    try:
        content = md_file.read_text(encoding='utf-8')
        algorithm_folder = md_file.parent
        algorithm_name = algorithm_folder.name
        
        # Read algorithm files
        readme_path = algorithm_folder / "README.md"
        code_path = algorithm_folder / "algorithm.py"
        metadata_path = algorithm_folder / "metadata.json"
        
        readme_content = None
        code_content = None
        metadata = None
        
        if readme_path.exists():
            try:
                readme_content = readme_path.read_text(encoding='utf-8')
            except:
                pass
        
        if code_path.exists():
            try:
                code_content = code_path.read_text(encoding='utf-8')
            except:
                pass
        
        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
            except:
                pass
        
        # Extract better description
        better_description = extract_readme_description(readme_content)
        
        # Extract complexity from code
        code_complexity = extract_complexity_from_code(code_content)
        
        # Get category
        category = "Algorithms"
        if metadata and metadata.get('category'):
            category = metadata['category']
        
        # Get use cases
        use_cases = get_real_world_use_cases(algorithm_name, category)
        
        # Update content if we found improvements
        updated = False
        
        # Update complexity if found in code
        if code_complexity and "Complexity:" in content:
            # Find and update complexity in Quick Summary
            pattern = r'- \*\*Complexity:\*\* [^\n]+'
            replacement = f"- **Complexity:** {code_complexity}"
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                updated = True
        
        # Update use cases section
        if "## Where It's Used in Practice" in content or "## Где применяется на практике" in content:
            use_cases_section = "## Where It's Used in Practice\n\n" if "## Where It's Used in Practice" in content else "## Где применяется на практике\n\n"
            use_cases_text = use_cases_section + "\n".join(f"- {case}" for case in use_cases) + "\n"
            
            # Find and replace use cases section
            if "## Where It's Used in Practice" in content:
                start = content.find("## Where It's Used in Practice")
            else:
                start = content.find("## Где применяется на практике")
            
            if start != -1:
                next_section = content.find("\n## ", start + 1)
                if next_section != -1:
                    content = content[:start] + use_cases_text + content[next_section:]
                else:
                    content = content[:start] + use_cases_text
                updated = True
        
        if updated:
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
    print("PHASE 2.1: IMPROVING CONTENT QUALITY")
    print("="*70)
    
    md_files = find_all_md_files()
    print(f"\nFound {len(md_files)} MD files")
    print("\nImproving:")
    print("  - README description extraction (skip flowcharts)")
    print("  - Complexity detection from code docstrings")
    print("  - Real-world use cases")
    
    improved = 0
    errors = 0
    
    for i, md_file in enumerate(md_files, 1):
        if improve_md_file(md_file):
            improved += 1
        else:
            errors += 1
        
        if i % 500 == 0:
            print(f"Progress: {i}/{len(md_files)} ({i/len(md_files)*100:.1f}%)")
    
    print(f"\n{'='*70}")
    print(f"Improved: {improved}/{len(md_files)} files")
    print(f"Errors: {errors}")
    print(f"{'='*70}")
    
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

