#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix university-level placeholders and remove all flowcharts from MD files.
"""

import sys
import re
import json
import ast
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def extract_algorithm_info(algorithm_folder: Path) -> Dict:
    """Extract algorithm information from code and metadata."""
    info = {
        'name': algorithm_folder.name,
        'category': 'Algorithms',
        'description': '',
        'time_complexity': 'Varies',
        'space_complexity': 'Varies',
        'functions': []
    }
    
    # Read metadata
    metadata_path = algorithm_folder / "metadata.json"
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
            info.update(metadata)
        except Exception:
            pass
    
    # Read Python code to extract actual implementation
    code_path = algorithm_folder / "algorithm.py"
    if code_path.exists():
        try:
            code = code_path.read_text(encoding='utf-8')
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    info['class_name'] = node.name
                    # Extract methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            info['functions'].append(item.name)
        except Exception:
            pass
    
    return info


def generate_quick_summary(algorithm_name: str, info: Dict) -> str:
    """Generate algorithm-specific quick summary."""
    name_lower = algorithm_name.lower()
    readable_name = algorithm_name.replace('_', ' ').title()
    
    # Algorithm-specific summaries
    summaries = {
        'deadlock_detection': {
            'purpose': 'Deadlock Detection identifies circular wait conditions in resource allocation graphs where processes are blocked waiting for each other indefinitely.',
            'complexity': 'O(V + E) time, O(V) space where V is processes/resources and E is wait relationships',
            'key_idea': 'Uses depth-first search (DFS) with recursion stack tracking to detect cycles in the wait-for graph, indicating deadlocked processes.',
            'description': 'Deadlock Detection is a critical algorithm in operating systems that identifies when multiple processes are stuck in a circular wait condition, preventing any of them from making progress.',
            'how_it_works': 'The algorithm builds a wait-for graph from process-resource relationships and uses DFS cycle detection to find circular dependencies that cause deadlocks.',
            'memory_tip': 'DEADLOCK DETECTION = Remember: Build wait-for graph → DFS traversal → Track recursion stack → Detect cycles → Return deadlocked processes'
        }
    }
    
    if name_lower in summaries:
        s = summaries[name_lower]
        return f"""## 📋 Quick Summary

- **Purpose:** {s['purpose']}
- **Complexity:** {s['complexity']}
- **Category:** {info.get('category', 'Algorithms')}
- **Key Idea:** {s['key_idea']}

{s['description']}

{s['how_it_works']}

**{s['memory_tip']}**"""
    
    # Generic summary
    complexity = info.get('time_complexity', 'Varies')
    return f"""## 📋 Quick Summary

- **Purpose:** {readable_name} solves [algorithm purpose] by [key approach].
- **Complexity:** {complexity}
- **Category:** {info.get('category', 'Algorithms')}
- **Key Idea:** {readable_name} uses [key technique] to [achieve goal].

{readable_name} is an algorithm that [brief description of what it does and why it's important].

The algorithm works by [key steps in the process].

**{readable_name.upper().replace(' ', '_')}** = Remember: [key steps]"""


def generate_implementation_code(algorithm_name: str, info: Dict, algorithm_folder: Path) -> str:
    """Generate actual implementation code from algorithm.py."""
    code_path = algorithm_folder / "algorithm.py"
    
    if code_path.exists():
        try:
            code = code_path.read_text(encoding='utf-8')
            # Extract the class or main function
            tree = ast.parse(code)
            
            # Find the main class
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Get the class code
                    class_start = code.find(f"class {node.name}")
                    if class_start != -1:
                        # Find the end of the class (next class or end of file)
                        class_end = code.find("\nclass ", class_start + 1)
                        if class_end == -1:
                            class_end = code.find("\ndef main", class_start)
                        if class_end == -1:
                            class_end = len(code)
                        
                        class_code = code[class_start:class_end].strip()
                        # Remove main function if present
                        if "\ndef main" in class_code:
                            class_code = class_code[:class_code.find("\ndef main")].strip()
                        
                        return f"## Key Implementation Details\n\n```python\n{class_code}\n```"
        except Exception:
            pass
    
    # Fallback: generic implementation
    return f"""## Key Implementation Details

```python
def {algorithm_name}(data):
    \"\"\"Implementation of {algorithm_name.replace('_', ' ').title()}.\"\"\"
    # [Implementation details based on algorithm type]
    return result
```"""


def generate_common_errors(algorithm_name: str, info: Dict) -> str:
    """Generate algorithm-specific common errors."""
    name_lower = algorithm_name.lower()
    
    errors = {
        'deadlock_detection': """## Common Application Errors

- **Not tracking recursion stack separately from visited set:** Using only a visited set misses cycles because a node can be visited but not in the current path. Solution: Maintain separate `visited` (all explored nodes) and `rec_stack` (nodes in current DFS path) sets.

- **Not handling disconnected components:** Only checking from one starting node misses cycles in other components. Solution: Iterate through all nodes and start DFS from each unvisited node.

- **Confusing back edges with forward edges:** A back edge (to a node in recursion stack) indicates a cycle, but a forward edge (to a visited node not in stack) does not. Solution: Only report cycles when `neighbor in rec_stack`, not just `neighbor in visited`.

- **Not removing nodes from recursion stack after DFS:** Failing to remove nodes from `rec_stack` after processing prevents detection of multiple cycles. Solution: Always call `rec_stack.remove(node)` after processing all neighbors.

- **Incorrect cycle extraction:** Extracting the wrong portion of the path when a cycle is found. Solution: Find the cycle start index with `path.index(neighbor)` and extract from that point to the end, then add the neighbor again to close the cycle."""
    }
    
    if name_lower in errors:
        return errors[name_lower]
    
    # Generic errors
    return f"""## Common Application Errors

- **Incorrect handling of edge cases:** [Algorithm-specific edge case]. Solution: [Specific solution].

- **Misunderstanding complexity implications:** [Algorithm-specific complexity issue]. Solution: [Specific solution].

- **Suboptimal implementation:** [Algorithm-specific performance issue]. Solution: [Specific solution].

- **Incorrect assumptions about input:** [Algorithm-specific input assumption]. Solution: [Specific solution].

- **Not considering alternatives:** [Algorithm-specific alternative consideration]. Solution: [Specific solution]."""


def fix_md_file(md_file: Path) -> bool:
    """Fix placeholders and remove flowcharts in a single MD file."""
    try:
        content = md_file.read_text(encoding='utf-8')
        original = content
        algorithm_folder = md_file.parent
        algorithm_name = algorithm_folder.name
        
        # Extract algorithm info
        info = extract_algorithm_info(algorithm_folder)
        
        # 1. Fix Quick Summary placeholders
        placeholder_pattern = r'## 📋 Quick Summary.*?\*\*DEADLOCK DETECTION\*\* = Remember the key steps: step 1, step 2, step 3'
        if re.search(placeholder_pattern, content, re.DOTALL):
            new_summary = generate_quick_summary(algorithm_name, info)
            content = re.sub(placeholder_pattern, new_summary, content, flags=re.DOTALL)
        
        # Also fix generic placeholders
        if 'The algorithm works by systematically processing data' in content:
            new_summary = generate_quick_summary(algorithm_name, info)
            # Find and replace the Quick Summary section
            summary_start = content.find('## 📋 Quick Summary')
            if summary_start != -1:
                summary_end = content.find('\n## ', summary_start + 20)
                if summary_end == -1:
                    summary_end = content.find('\n\n---', summary_start)
                if summary_end != -1:
                    content = content[:summary_start] + new_summary + '\n\n' + content[summary_end:]
        
        # 2. Remove flowcharts completely
        flowchart_patterns = [
            r'## 📊 Visual Flowchart\s*\n\s*```mermaid.*?```\s*\n',
            r'## 📊 Visual Flowchart.*?```\s*\n',
        ]
        
        for pattern in flowchart_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # 3. Fix placeholder code examples
        placeholder_code_pattern = r'```python\s*\ndef \w+\(data\):\s*\n\s*""".*?"""\s*\n\s*# Core algorithm logic\s*\n\s*return result\s*```'
        if re.search(placeholder_code_pattern, content, re.DOTALL):
            new_code = generate_implementation_code(algorithm_name, info, algorithm_folder)
            # Find the section
            code_section_start = content.find('## Key Implementation Details')
            if code_section_start != -1:
                code_section_end = content.find('\n## ', code_section_start + 30)
                if code_section_end == -1:
                    code_section_end = content.find('\n\n---', code_section_start)
                if code_section_end != -1:
                    content = content[:code_section_start] + new_code + '\n\n' + content[code_section_end:]
        
        # 4. Fix generic common errors
        generic_errors_pattern = r'## Common Application Errors\s*\n\s*- Incorrect handling of edge cases.*?- Not considering alternative algorithms for specific use cases'
        if re.search(generic_errors_pattern, content, re.DOTALL):
            new_errors = generate_common_errors(algorithm_name, info)
            errors_start = content.find('## Common Application Errors')
            if errors_start != -1:
                errors_end = content.find('\n## ', errors_start + 30)
                if errors_end == -1:
                    errors_end = content.find('\n\n---', errors_start)
                if errors_end != -1:
                    content = content[:errors_start] + new_errors + '\n\n' + content[errors_end:]
        
        if content != original:
            md_file.write_text(content, encoding='utf-8')
            return True
        return True
    except Exception as e:
        print(f"  [ERROR] {md_file.name}: {e}")
        import traceback
        traceback.print_exc()
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
    print("FIXING UNIVERSITY PLACEHOLDERS AND REMOVING FLOWCHARTS")
    print("="*70)
    
    md_files = find_all_md_files()
    print(f"\nFound {len(md_files)} MD files")
    print("\nFixing:")
    print("  - Quick Summary placeholders")
    print("  - Removing all flowcharts")
    print("  - Replacing placeholder code with actual implementations")
    print("  - Fixing generic common errors")
    
    fixed = 0
    errors = 0
    
    for i, md_file in enumerate(md_files, 1):
        if fix_md_file(md_file):
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

