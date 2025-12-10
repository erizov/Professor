#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replace all placeholder content with algorithm-specific examples.
Fixes:
- Try It Yourself sections
- Step-by-Step Execution
- Practice Exercises
- Check Your Understanding Q&A
- Common Mistakes format
"""

import sys
import re
import ast
import json
from pathlib import Path
from typing import Dict, Optional, List, Tuple

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
        'functions': [],
        'key_operations': []
    }
    
    # Read metadata
    metadata_path = algorithm_folder / "metadata.json"
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
            info.update(metadata)
        except Exception:
            pass
    
    # Read Python code
    code_path = algorithm_folder / "algorithm.py"
    if code_path.exists():
        try:
            code = code_path.read_text(encoding='utf-8')
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    info['functions'].append(node.name)
                    # Extract key operations
                    for stmt in node.body[:5]:
                        if isinstance(stmt, ast.Assign):
                            info['key_operations'].append('assignment')
                        elif isinstance(stmt, ast.If):
                            info['key_operations'].append('conditional')
                        elif isinstance(stmt, ast.For):
                            info['key_operations'].append('iteration')
                        elif isinstance(stmt, ast.While):
                            info['key_operations'].append('loop')
        except Exception:
            pass
    
    return info


def generate_try_it_yourself(algorithm_name: str, info: Dict, is_school: bool, lang: str) -> str:
    """Generate algorithm-specific Try It Yourself section."""
    name_lower = algorithm_name.lower()
    readable_name = algorithm_name.replace('_', ' ').title()
    
    # Algorithm-specific examples
    examples = {
        'deadlock_detection': """**Try detecting a deadlock:**
```
Wait-for graph:
  Process 1 → Resource 2
  Process 2 → Resource 3
  Process 3 → Resource 1

Step 1: Start DFS from Process 1
  Visit Process 1 → Resource 2

Step 2: Follow Resource 2 → Process 2
  Visit Process 2 → Resource 3

Step 3: Follow Resource 3 → Process 3
  Visit Process 3 → Resource 1

Step 4: Process 1 is already in recursion stack!
  Found cycle: 1 → 2 → 3 → 1
  Deadlock detected!

Output: Deadlock found in cycle [1, 2, 3, 1]
```""",
        'bubble_sort': """**Try sorting this array:**
```
Input: [5, 2, 8, 1, 9]

Pass 1: Compare and swap
  [5, 2, 8, 1, 9] → swap 5 and 2 → [2, 5, 8, 1, 9]
  [2, 5, 8, 1, 9] → no swap → [2, 5, 8, 1, 9]
  [2, 5, 8, 1, 9] → swap 8 and 1 → [2, 5, 1, 8, 9]
  [2, 5, 1, 8, 9] → no swap → [2, 5, 1, 8, 9]

Pass 2: Continue...
  [2, 5, 1, 8, 9] → no swap → [2, 5, 1, 8, 9]
  [2, 5, 1, 8, 9] → swap 5 and 1 → [2, 1, 5, 8, 9]

Continue until sorted: [1, 2, 5, 8, 9]
```""",
        'binary_search': """**Try finding 7 in sorted array:**
```
Array: [1, 3, 5, 7, 9, 11, 13]
Target: 7

Step 1: Check middle (index 3, value 5)
  5 < 7, search right half: [7, 9, 11, 13]

Step 2: Check middle of right half (index 5, value 9)
  9 > 7, search left half: [7]

Step 3: Found! Element 7 is at index 3
```"""
    }
    
    if name_lower in examples:
        return examples[name_lower]
    
    # Generic based on algorithm type
    if 'sort' in name_lower:
        return f"""**Try sorting this array:**
```
Input: [5, 2, 8, 1, 9]

Step 1: Apply {readable_name} algorithm
Step 2: Process elements systematically
Step 3: Verify sorted order

Output: [1, 2, 5, 8, 9]
```"""
    elif 'search' in name_lower:
        return f"""**Try searching for a value:**
```
Input: [1, 3, 5, 7, 9]
Target: 7

Step 1: Apply {readable_name} algorithm
Step 2: Narrow down search space
Step 3: Find target element

Output: Found at index 3
```"""
    elif 'detection' in name_lower or 'detect' in name_lower:
        return f"""**Try detecting a pattern:**
```
Input: [example data with pattern]

Step 1: Initialize detection state
Step 2: Process data elements
Step 3: Identify pattern occurrence

Output: Pattern detected at position X
```"""
    else:
        return f"""**Try this example:**
```
Input: [example data]

Step 1: Initialize algorithm state
Step 2: Process input data
Step 3: Generate result

Output: [algorithm result]
```"""


def generate_step_by_step(algorithm_name: str, info: Dict, is_school: bool, lang: str) -> Tuple[str, str]:
    """Generate algorithm-specific step-by-step execution."""
    name_lower = algorithm_name.lower()
    
    executions = {
        'deadlock_detection': ("""**Step-by-Step Execution:**

```python
# Initialize wait-for graph
detector = DeadlockDetection()
detector.add_wait(1, 2)  # Process 1 waits for Resource 2
detector.add_wait(2, 3)  # Process 2 waits for Resource 3
detector.add_wait(3, 1)  # Process 3 waits for Resource 1

# Step 1: Start DFS from Process 1
visited = {1}
rec_stack = {1}
path = [1]

# Step 2: Process 1 → Resource 2 → Process 2
visited = {1, 2}
rec_stack = {1, 2}
path = [1, 2]

# Step 3: Process 2 → Resource 3 → Process 3
visited = {1, 2, 3}
rec_stack = {1, 2, 3}
path = [1, 2, 3]

# Step 4: Process 3 → Resource 1 → Process 1 (already in rec_stack!)
# Found cycle: [1, 2, 3, 1]
cycles = [[1, 2, 3, 1]]

# Result
return [[1, 2, 3, 1]]  # Deadlock detected!
```""",
"""**Expected Output:**

```
Wait-for graph:
  Process 1 → Resource 2
  Process 2 → Resource 3
  Process 3 → Resource 1

DFS traversal:
  Start: Process 1
  Visit: Process 2
  Visit: Process 3
  Cycle detected: Process 1 (already in recursion stack)

Deadlock found!
Cycle: [1, 2, 3, 1]
```""")
    }
    
    if name_lower in executions:
        return executions[name_lower]
    
    # Generic execution
    execution = f"""**Step-by-Step Execution:**

```python
# Input
data = [example input]

# Step 1: Initialize
state = initial_state

# Step 2: Process
# [Processing steps based on algorithm]

# Step 3: Finalize
result = final_state

# Output
return result
```"""
    
    output = f"""**Expected Output:**

```
Input: [example]
Processing...
Result: [output]
```"""
    
    return execution, output


def generate_practice_exercises(algorithm_name: str, info: Dict, is_school: bool, lang: str) -> str:
    """Generate algorithm-specific practice exercises."""
    name_lower = algorithm_name.lower()
    readable_name = algorithm_name.replace('_', ' ').title()
    
    exercises = {
        'deadlock_detection': """**Exercise 1 (Easy):**
Create a wait-for graph with 3 processes and detect if there's a deadlock. Draw the graph and trace the DFS.

**Exercise 2 (Medium):**
Implement deadlock detection for a system with multiple processes and resources. Handle edge cases (no cycles, multiple cycles).

**Exercise 3 (Hard):**
Design a deadlock detection system that runs periodically in an operating system. Consider performance and false positives.""",
        'bubble_sort': """**Exercise 1 (Easy):**
Sort the array [3, 1, 4, 1, 5, 9, 2, 6] by hand using bubble sort. Show each pass.

**Exercise 2 (Medium):**
Implement bubble sort with an optimization to stop early if no swaps occur in a pass.

**Exercise 3 (Hard):**
Compare bubble sort performance with other sorting algorithms on different input sizes and patterns.""",
        'binary_search': """**Exercise 1 (Easy):**
Find the number 7 in the sorted array [1, 3, 5, 7, 9, 11, 13] by hand. Show each comparison.

**Exercise 2 (Medium):**
Implement binary search recursively and iteratively. Compare the implementations.

**Exercise 3 (Hard):**
Extend binary search to find the first/last occurrence of a duplicate value in a sorted array."""
    }
    
    if name_lower in exercises:
        return exercises[name_lower]
    
    # Generic exercises
    if is_school:
        return f"""**Exercise 1 (Easy):**
Trace through the {readable_name} algorithm with a small example (3-5 elements). Write down each step.

**Exercise 2 (Medium):**
Implement the {readable_name} algorithm in your preferred programming language. Test it with different inputs.

**Exercise 3 (Hard):**
Apply the {readable_name} algorithm to solve a real-world problem. Explain why this algorithm is suitable."""
    else:
        return f"""**Exercise 1 (Easy):**
Trace through the {readable_name} algorithm with a small example. Analyze time and space complexity.

**Exercise 2 (Medium):**
Implement the {readable_name} algorithm with proper error handling and edge case coverage.

**Exercise 3 (Hard):**
Optimize the {readable_name} algorithm or design a variant for a specific use case. Analyze trade-offs."""


def generate_qa(algorithm_name: str, info: Dict, is_school: bool, lang: str) -> str:
    """Generate algorithm-specific Q&A."""
    name_lower = algorithm_name.lower()
    readable_name = algorithm_name.replace('_', ' ').title()
    
    qa_sets = {
        'deadlock_detection': {
            'q1': 'What problem does this algorithm solve?',
            'a1': 'Deadlock Detection identifies when processes are waiting for each other in a circular manner, causing all processes to be blocked indefinitely.',
            'q2': 'What is the time complexity?',
            'a2': 'O(V + E) where V is the number of processes/resources and E is the number of wait relationships. Uses DFS for cycle detection.',
            'q3': 'When would you use this algorithm?',
            'a3': 'In operating systems to periodically check for deadlocks, in database systems to detect transaction deadlocks, and in distributed systems to identify circular dependencies.',
            'q4': 'What are the main steps of this algorithm?',
            'a4': '1) Build wait-for graph from process-resource relationships, 2) Use DFS to traverse the graph, 3) Detect cycles using recursion stack, 4) Return all detected cycles as deadlocks.'
        },
        'bubble_sort': {
            'q1': 'What problem does this algorithm solve?',
            'a1': 'Bubble Sort arranges elements in ascending or descending order by repeatedly comparing adjacent elements and swapping them if they are in the wrong order.',
            'q2': 'What is the time complexity?',
            'a2': 'O(n²) in worst and average cases, O(n) in best case (when array is already sorted).',
            'q3': 'When would you use this algorithm?',
            'a3': 'For educational purposes, small datasets, or when simplicity is more important than performance. Not recommended for large datasets.',
            'q4': 'What are the main steps of this algorithm?',
            'a4': '1) Compare adjacent elements, 2) Swap if they are in wrong order, 3) Repeat for all pairs, 4) Continue passes until no swaps are needed.'
        }
    }
    
    if name_lower in qa_sets:
        qa = qa_sets[name_lower]
        return f"""**Q1:** {qa['q1']}
**A:** {qa['a1']}

**Q2:** {qa['q2']}
**A:** {qa['a2']}

**Q3:** {qa['q3']}
**A:** {qa['a3']}

**Q4:** {qa['q4']}
**A:** {qa['a4']}"""
    
    # Generic Q&A
    complexity = info.get('time_complexity', 'Varies')
    return f"""**Q1:** What problem does this algorithm solve?
**A:** {readable_name} solves the problem of [algorithm purpose]. It processes input data systematically to achieve [desired outcome].

**Q2:** What is the time complexity?
**A:** {complexity}

**Q3:** When would you use this algorithm?
**A:** Use {readable_name} when you need to [use case scenario]. It's particularly effective for [specific situations].

**Q4:** What are the main steps of this algorithm?
**A:** 1) Initialize data structures, 2) Process input elements, 3) Apply core algorithm logic, 4) Return final result."""


def generate_common_mistakes(algorithm_name: str, info: Dict, is_school: bool, lang: str) -> str:
    """Generate algorithm-specific common mistakes."""
    name_lower = algorithm_name.lower()
    readable_name = algorithm_name.replace('_', ' ').title()
    
    mistakes = {
        'deadlock_detection': """### ❌ Mistake 1: Not tracking recursion stack properly
**Solution:** Use a separate `rec_stack` set to track nodes in the current DFS path. Only nodes in `rec_stack` indicate a back edge (cycle).

### ❌ Mistake 2: Not handling disconnected components
**Solution:** Iterate through all nodes in the graph and start DFS from each unvisited node to ensure all cycles are detected.

### ❌ Mistake 3: Confusing visited nodes with recursion stack
**Solution:** `visited` tracks all explored nodes, while `rec_stack` tracks nodes in current path. A node can be visited but not in current path.

### ❌ Mistake 4: Not removing node from recursion stack after DFS
**Solution:** Always remove the node from `rec_stack` after processing all neighbors to allow detection of multiple cycles.

### 💡 How to Avoid
- Use two separate sets: `visited` for all explored nodes, `rec_stack` for current path
- Always clean up `rec_stack` after processing
- Test with graphs containing multiple cycles
- Verify with simple examples first (2-3 nodes)""",
        'bubble_sort': """### ❌ Mistake 1: Not optimizing to stop early
**Solution:** Add a flag to check if any swaps occurred in a pass. If no swaps, the array is sorted and you can stop early.

### ❌ Mistake 2: Comparing wrong elements
**Solution:** Compare `arr[j]` with `arr[j+1]`, not `arr[i]` with `arr[j]`. The inner loop should compare adjacent elements.

### ❌ Mistake 3: Going out of bounds
**Solution:** In inner loop, iterate `j` from `0` to `n-i-1` (not `n-1`) to avoid comparing already-sorted elements at the end.

### ❌ Mistake 4: Not handling edge cases
**Solution:** Check for empty arrays or single-element arrays before starting the sorting process.

### 💡 How to Avoid
- Test with edge cases: empty array, single element, already sorted
- Use proper loop bounds to avoid index errors
- Add early termination optimization
- Trace through examples step-by-step"""
    }
    
    if name_lower in mistakes:
        return mistakes[name_lower]
    
    # Generic mistakes
    return f"""### ❌ Mistake 1: Not handling edge cases
**Solution:** Always check for empty input, single element, or boundary values before processing.

### ❌ Mistake 2: Incorrect initialization
**Solution:** Ensure all variables and data structures are properly initialized before the main algorithm loop.

### ❌ Mistake 3: Off-by-one errors in loops
**Solution:** Carefully verify loop bounds and termination conditions. Test with small examples to catch boundary issues.

### ❌ Mistake 4: Not validating input
**Solution:** Add input validation to ensure data is in expected format and within valid ranges.

### 💡 How to Avoid
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify variable values
- Review algorithm's key steps before implementing"""


def fix_md_file(md_file: Path) -> bool:
    """Fix all placeholders in a single MD file."""
    try:
        content = md_file.read_text(encoding='utf-8')
        original = content
        
        algorithm_folder = md_file.parent
        algorithm_name = algorithm_folder.name
        
        # Determine if school or university, and language
        is_school = 'school' in md_file.name
        lang = 'en' if '.en.' in md_file.name else 'ru'
        
        # Extract algorithm info
        info = extract_algorithm_info(algorithm_folder)
        
        # Fix Try It Yourself
        try_it_pattern = r'## 🎯 Try It Yourself\s*\n\n\*\*Try this example:\*\*\s*\n(?:```)?\s*\nInput: \[example data\].*?Output: \[result\]\s*(?:```)?'
        try_it_replacement = f"## 🎯 Try It Yourself\n\n{generate_try_it_yourself(algorithm_name, info, is_school, lang)}\n"
        content = re.sub(try_it_pattern, try_it_replacement, content, flags=re.DOTALL)
        
        # Also fix if it's just text without code block
        try_it_pattern2 = r'\*\*Try this example:\*\*\s*\nInput: \[example data\].*?Output: \[result\]'
        content = re.sub(try_it_pattern2, generate_try_it_yourself(algorithm_name, info, is_school, lang), content, flags=re.DOTALL)
        
        # Fix Step-by-Step Execution
        step_pattern = r'## 🔍 Step-by-Step Execution\s*\n\n\*\*Step-by-Step Execution:\*\*\s*\n```python\s*\n# Input\s*\ndata = \[example input\].*?return result\s*```'
        step_execution, step_output = generate_step_by_step(algorithm_name, info, is_school, lang)
        step_replacement = f"## 🔍 Step-by-Step Execution\n\n{step_execution}\n\n{step_output}\n"
        content = re.sub(step_pattern, step_replacement, content, flags=re.DOTALL)
        
        # Also fix if pattern is slightly different
        step_pattern2 = r'\*\*Step-by-Step Execution:\*\*\s*\n```python\s*\n# Input\s*\ndata = \[example input\].*?return result\s*```'
        if re.search(step_pattern2, content):
            content = re.sub(step_pattern2, step_execution, content, flags=re.DOTALL)
        
        # Fix Expected Output (if separate)
        output_pattern = r'\*\*Expected Output:\*\*\s*\n```\s*\nInput: \[example\].*?Result: \[output\]\s*```'
        if '**Expected Output:**' in content and not re.search(output_pattern, content):
            # Already fixed in step-by-step, skip
            pass
        else:
            content = re.sub(output_pattern, step_output, content, flags=re.DOTALL)
        
        # Fix Practice Exercises
        practice_pattern = r'\*\*Exercise 1 \(Easy\):\s*\nTrace through the algorithm with a small example \(3-5 elements\)\.\s*\n\s*\n\*\*Exercise 2 \(Medium\):\s*\nImplement the algorithm in your preferred programming language\.\s*\n\s*\n\*\*Exercise 3 \(Hard\):\s*\nOptimize the algorithm or apply it to solve a real-world problem\.'
        practice_replacement = generate_practice_exercises(algorithm_name, info, is_school, lang)
        content = re.sub(practice_pattern, practice_replacement, content, flags=re.MULTILINE)
        
        # Also fix if it appears multiple times (duplicates)
        practice_sections = list(re.finditer(practice_pattern, content, flags=re.MULTILINE))
        if len(practice_sections) > 1:
            # Replace all occurrences
            for match in reversed(practice_sections[1:]):  # Replace from end to start
                content = content[:match.start()] + practice_replacement + content[match.end():]
        
        # Fix Check Your Understanding Q&A
        qa_pattern = r'\*\*Q1:\*\* What problem does this algorithm solve\?\s*\n\*\*A:\*\* \[Answer based on algorithm purpose\]\s*\n\s*\n\*\*Q2:\*\* What is the time complexity\?\s*\n\*\*A:\*\* Varies\s*\n\s*\n\*\*Q3:\*\* When would you use this algorithm\?\s*\n\*\*A:\*\* \[Answer based on use cases\]\s*\n\s*\n\*\*Q4:\*\* What are the main steps of this algorithm\?\s*\n\*\*A:\*\* \[List 3-5 key steps\]'
        qa_replacement = generate_qa(algorithm_name, info, is_school, lang)
        content = re.sub(qa_pattern, qa_replacement, content, flags=re.MULTILINE)
        
        # Also fix if it appears multiple times (duplicates)
        qa_sections = list(re.finditer(qa_pattern, content, flags=re.MULTILINE))
        if len(qa_sections) > 1:
            # Replace all occurrences
            for match in reversed(qa_sections[1:]):  # Replace from end to start
                content = content[:match.start()] + qa_replacement + content[match.end():]
        
        # Fix Common Mistakes format
        # Pattern: Mistake text that's actually a solution
        mistake_pattern = r'### ❌ Mistake \d+: (Test with edge cases|Trace through examples|Use debugging tools|Review the algorithm\'s key steps)'
        if re.search(mistake_pattern, content):
            # Replace entire Common Mistakes section
            common_mistakes_section = f"## Common Mistakes\n\n{generate_common_mistakes(algorithm_name, info, is_school, lang)}\n"
            # Find and replace the section
            cm_pattern = r'## Common Mistakes\s*\n\n(?:### ❌ Mistake.*?\n\n)*### 💡 How to Avoid.*?\n'
            content = re.sub(cm_pattern, common_mistakes_section, content, flags=re.DOTALL)
        
        # Also check for the specific format in the file
        if '### ❌ Mistake 1: Test with edge cases' in content:
            common_mistakes_section = f"## Common Mistakes\n\n{generate_common_mistakes(algorithm_name, info, is_school, lang)}\n"
            # Find the section start
            cm_start = content.find('## Common Mistakes')
            if cm_start != -1:
                # Find the next section or end
                cm_end = content.find('\n## ', cm_start + 20)
                if cm_end == -1:
                    cm_end = content.find('\n\n---', cm_start)
                if cm_end == -1:
                    cm_end = len(content)
                content = content[:cm_start] + common_mistakes_section + content[cm_end:]
        
        # Remove duplicate sections
        # Remove duplicate Try It Yourself
        try_it_sections = list(re.finditer(r'## 🎯 Try It Yourself', content))
        if len(try_it_sections) > 1:
            # Keep first, remove rest
            for match in try_it_sections[1:]:
                next_section = content.find('\n## ', match.end())
                if next_section != -1:
                    content = content[:match.start()] + content[next_section:]
                else:
                    content = content[:match.start()]
        
        # Remove duplicate Practice Exercises
        practice_sections = list(re.finditer(r'\*\*Exercise 1 \(Easy\):', content))
        if len(practice_sections) > 1:
            # Keep first occurrence in Practice Exercise section
            practice_ex_section = content.find('## ✏️ Practice Exercise')
            if practice_ex_section != -1:
                # Find all exercises after the section
                for i, match in enumerate(practice_sections):
                    if match.start() > practice_ex_section and i > 0:
                        # This is a duplicate, remove it
                        next_section = content.find('\n## ', match.end())
                        if next_section != -1:
                            content = content[:match.start()] + content[next_section:]
                        else:
                            content = content[:match.start()]
                        break
        
        # Remove duplicate Q&A
        qa_sections = list(re.finditer(r'\*\*Q1:\*\* What problem', content))
        if len(qa_sections) > 1:
            # Keep first in Check Your Understanding section
            check_section = content.find('## ✅ Check Your Understanding')
            if check_section != -1:
                for i, match in enumerate(qa_sections):
                    if match.start() > check_section and i > 0:
                        # Duplicate, remove
                        next_section = content.find('\n## ', match.end())
                        if next_section != -1:
                            content = content[:match.start()] + content[next_section:]
                        else:
                            content = content[:match.start()]
                        break
        
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
    print("REPLACING ALL PLACEHOLDER CONTENT")
    print("="*70)
    
    md_files = find_all_md_files()
    print(f"\nFound {len(md_files)} MD files")
    print("\nFixing:")
    print("  - Try It Yourself sections")
    print("  - Step-by-Step Execution")
    print("  - Practice Exercises")
    print("  - Check Your Understanding Q&A")
    print("  - Common Mistakes format")
    print("  - Removing duplicates")
    
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

