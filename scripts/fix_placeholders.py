#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix placeholders in algorithm descriptions:
- [How to fix this mistake] in Common Mistakes sections
- Generic descriptions that need algorithm-specific content
- Empty or placeholder sections
"""

import sys
import re
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def get_mistake_solution(algorithm_name: str, mistake_num: int, 
                        mistake_text: str) -> str:
    """Generate specific solution for a common mistake."""
    name_lower = algorithm_name.lower()
    mistake_lower = mistake_text.lower()
    
    # Algorithm-specific solutions
    solutions = {
        'bubble_sort': {
            1: "Add edge case checks: `if not data or len(data) <= 1: return data`",
            2: "Use `range(len(data) - i - 1)` to avoid comparing already sorted elements",
            3: "Add early termination: `swapped = False` and break if no swaps occur",
            4: "Remember: bubble sort is O(n²) - use only for small datasets or educational purposes"
        },
        'quick_sort': {
            1: "Always check: `if start >= end: return` to prevent infinite recursion",
            2: "Choose pivot carefully - middle element is safer than first/last",
            3: "Handle duplicate elements correctly in partition function",
            4: "For small arrays (n < 10), use insertion sort instead"
        },
        'binary_search': {
            1: "Verify array is sorted: `if data != sorted(data): raise ValueError`",
            2: "Use `mid = (left + right) // 2` to avoid integer overflow",
            3: "Update bounds correctly: `left = mid + 1` or `right = mid - 1` (not `mid`)",
            4: "Check bounds: `if left > right: return -1` before accessing `data[mid]`"
        },
        'merge_sort': {
            1: "Check base case: `if len(data) <= 1: return data`",
            2: "Create temporary arrays for left/right halves, don't modify original",
            3: "Merge correctly: compare elements and add smaller one first",
            4: "Remember space complexity is O(n) - allocate merge arrays properly"
        },
        'dijkstra': {
            1: "Initialize distances: `dist[start] = 0`, all others to infinity",
            2: "Use priority queue (heap) for O(V log V) complexity, not list",
            3: "Mark nodes as visited to avoid revisiting",
            4: "Handle negative weights: Dijkstra doesn't work - use Bellman-Ford"
        },
        'fibonacci': {
            1: "Use base cases: `if n <= 1: return n`",
            2: "Store previous results (memoization) to avoid exponential recursion",
            3: "Use iterative approach for O(n) time, O(1) space",
            4: "Check for negative numbers: `if n < 0: raise ValueError`"
        }
    }
    
    # Check for specific algorithm
    for algo_key, algo_solutions in solutions.items():
        if algo_key in name_lower:
            if mistake_num in algo_solutions:
                return algo_solutions[mistake_num]
    
    # Generic solutions based on mistake type
    if 'edge case' in mistake_lower or 'empty' in mistake_lower:
        return "Add validation: `if not data or len(data) <= 1: return data`"
    elif 'index' in mistake_lower or 'bound' in mistake_lower or 'range' in mistake_lower:
        return "Check bounds before accessing: `if 0 <= index < len(data): ...`"
    elif 'complexity' in mistake_lower or 'performance' in mistake_lower:
        return "Understand time/space complexity - choose appropriate algorithm for data size"
    elif 'recursion' in mistake_lower or 'base case' in mistake_lower:
        return "Always include base case: `if base_condition: return base_value`"
    elif 'implementation' in mistake_lower or 'logic' in mistake_lower:
        return "Trace through example step-by-step, verify each step matches algorithm logic"
    else:
        return "Review algorithm steps carefully, test with known examples, use debugging tools"


def fix_common_mistakes_placeholders(content: str, algorithm_name: str) -> str:
    """Fix placeholders in Common Mistakes section."""
    if "[How to fix this mistake]" not in content:
        # Also check for mistakes without solutions
        if "### ❌ Mistake" in content and "**Solution:**" not in content:
            # Need to add solutions
            pass
        else:
            return content
    
    # Find Common Mistakes section
    mistakes_start = content.find("## Common Mistakes")
    if mistakes_start == -1:
        mistakes_start = content.find("## ❌")
    
    if mistakes_start == -1:
        return content
    
    # Find end of Common Mistakes section
    next_section = content.find("\n## ", mistakes_start + 1)
    if next_section == -1:
        mistakes_section = content[mistakes_start:]
        rest = ""
    else:
        mistakes_section = content[mistakes_start:next_section]
        rest = content[next_section:]
    
    # Fix each placeholder
    lines = mistakes_section.split('\n')
    fixed_lines = []
    mistake_num = 0
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a mistake header
        if "### ❌ Mistake" in line:
            mistake_num += 1
            mistake_text = line
            fixed_lines.append(line)
            i += 1
            
            # Check if next line has solution
            if i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith("**Solution:**"):
                    # Check if it's a placeholder or empty
                    solution_text = next_line[len("**Solution:**"):].strip()
                    if "[How to fix this mistake]" in solution_text or not solution_text:
                        solution = get_mistake_solution(algorithm_name, mistake_num, mistake_text)
                        fixed_lines.append(f"**Solution:** {solution}")
                        i += 1
                        continue
                    else:
                        # Solution exists, keep it
                        fixed_lines.append(lines[i])
                        i += 1
                        continue
                elif next_line.startswith("### ❌") or next_line.startswith("### 💡") or next_line.startswith("## "):
                    # Next mistake or section, add solution for current one
                    solution = get_mistake_solution(algorithm_name, mistake_num, mistake_text)
                    fixed_lines.append(f"**Solution:** {solution}")
                    fixed_lines.append("")
                    continue
                else:
                    # No solution, add one
                    solution = get_mistake_solution(algorithm_name, mistake_num, mistake_text)
                    fixed_lines.append(f"**Solution:** {solution}")
                    fixed_lines.append("")
                    continue
        elif "[How to fix this mistake]" in line:
            mistake_num += 1
            # Get the mistake text from previous lines
            mistake_text = ""
            for j in range(max(0, len(fixed_lines)-3), len(fixed_lines)):
                if j < len(fixed_lines) and ("### ❌" in fixed_lines[j] or "**❌" in fixed_lines[j]):
                    mistake_text = fixed_lines[j]
                    break
            
            solution = get_mistake_solution(algorithm_name, mistake_num, mistake_text)
            fixed_line = line.replace("[How to fix this mistake]", solution)
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
        
        i += 1
    
    return content[:mistakes_start] + '\n'.join(fixed_lines) + rest


def fix_generic_descriptions(content: str, algorithm_name: str, 
                            files: Dict) -> str:
    """Fix generic descriptions like 'systematically processing data'."""
    name_lower = algorithm_name.lower()
    readable_name = algorithm_name.replace('_', ' ').title()
    
    # Check for generic patterns
    generic_patterns = [
        "systematically processing data according to a specific strategy",
        "works by systematically processing data",
        "The algorithm works by systematically processing data"
    ]
    
    # Fix duplicate/repetitive text patterns
    # Pattern 1: "Algorithm Name: Algorithm Name is..."
    duplicate_pattern1 = re.compile(
        re.escape(readable_name) + r':\s+' + re.escape(readable_name) + r'\s+is',
        re.IGNORECASE
    )
    content = duplicate_pattern1.sub(
        f"{readable_name}: {readable_name} is", content
    )
    
    # Pattern 2: "The algorithm works by Algorithm Name is..."
    duplicate_pattern2 = re.compile(
        r'The algorithm works by\s+' + re.escape(readable_name) + r'\s+is',
        re.IGNORECASE
    )
    content = duplicate_pattern2.sub(
        f"{readable_name} is", content
    )
    
    # Pattern 3: "Algorithm Name: The algorithm works by Algorithm Name is..."
    duplicate_pattern3 = re.compile(
        re.escape(readable_name) + r':\s+The algorithm works by\s+' + re.escape(readable_name) + r'\s+is',
        re.IGNORECASE
    )
    content = duplicate_pattern3.sub(
        f"{readable_name}: {readable_name} is", content
    )
    
    has_generic = any(pattern in content for pattern in generic_patterns)
    
    if not has_generic:
        return content
    
    # Try to get better description from README
    better_description = None
    if files.get('readme'):
        readme = files['readme']
        # Extract first meaningful paragraph
        lines = readme.split('\n')
        for line in lines:
            if len(line.strip()) > 50 and not line.strip().startswith('#'):
                if 'flowchart' not in line.lower() and 'step-by-step execution' not in line.lower():
                    better_description = line.strip()
                    break
    
    # Algorithm-specific descriptions
    specific_descriptions = {
        'grover': f"{readable_name} is a quantum search algorithm that finds a marked item in an unsorted database with O(√N) queries, providing quadratic speedup over classical search.",
        'shor': f"{readable_name} is a quantum algorithm for integer factorization, exponentially faster than classical methods.",
        'quantum': f"{readable_name} leverages quantum superposition and entanglement to solve problems faster than classical algorithms.",
    }
    
    for key, desc in specific_descriptions.items():
        if key in name_lower:
            # Replace generic descriptions
            for pattern in generic_patterns:
                content = content.replace(pattern, desc)
            return content
    
    # Use better description if found
    if better_description:
        for pattern in generic_patterns:
            content = content.replace(pattern, better_description)
    
    return content


def read_algorithm_files(algorithm_folder: Path) -> Dict:
    """Read algorithm files."""
    files = {
        'readme': None,
        'algorithm_py': None,
        'metadata': None
    }
    
    readme_path = algorithm_folder / "README.md"
    if readme_path.exists():
        try:
            files['readme'] = readme_path.read_text(encoding='utf-8')
        except:
            pass
    
    algo_path = algorithm_folder / "algorithm.py"
    if algo_path.exists():
        try:
            files['algorithm_py'] = algo_path.read_text(encoding='utf-8')
        except:
            pass
    
    metadata_path = algorithm_folder / "metadata.json"
    if metadata_path.exists():
        try:
            import json
            files['metadata'] = json.loads(metadata_path.read_text(encoding='utf-8'))
        except:
            pass
    
    return files


def fix_file(md_file: Path) -> bool:
    """Fix placeholders in a single MD file."""
    try:
        content = md_file.read_text(encoding='utf-8')
        
        # Get algorithm name from path
        algorithm_folder = md_file.parent
        algorithm_name = algorithm_folder.name
        
        # Read algorithm files for context
        files = read_algorithm_files(algorithm_folder)
        
        # Fix placeholders
        content = fix_common_mistakes_placeholders(content, algorithm_name)
        content = fix_generic_descriptions(content, algorithm_name, files)
        
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
    print("FIXING PLACEHOLDERS IN ALGORITHM DESCRIPTIONS")
    print("="*70)
    
    md_files = find_all_md_files()
    print(f"\nFound {len(md_files)} MD files")
    print("\nFixing:")
    print("  - [How to fix this mistake] placeholders")
    print("  - Generic descriptions")
    print("  - Empty placeholder sections")
    
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

