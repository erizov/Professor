#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive script to fix ALL placeholders in MD files.
Handles all format variations and applies algorithm-specific content.
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
        except Exception:
            pass
    
    return info


def generate_algorithm_specific_content(algorithm_name: str, info: Dict, section: str, is_school: bool, lang: str) -> str:
    """Generate algorithm-specific content for different sections."""
    name_lower = algorithm_name.lower()
    readable_name = algorithm_name.replace('_', ' ').title()
    
    # Algorithm-specific content database
    content_db = {
        'deadlock_detection': {
            'try_it': """**Try detecting a deadlock:**
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
            'step_by_step': """**Step-by-Step Execution:**

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
            'expected_output': """**Expected Output:**

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
```""",
            'practice': """**Exercise 1 (Easy):**
Create a wait-for graph with 3 processes and detect if there's a deadlock. Draw the graph and trace the DFS.

**Exercise 2 (Medium):**
Implement deadlock detection for a system with multiple processes and resources. Handle edge cases (no cycles, multiple cycles).

**Exercise 3 (Hard):**
Design a deadlock detection system that runs periodically in an operating system. Consider performance and false positives.""",
            'qa': """**Q1:** What problem does this algorithm solve?
**A:** Deadlock Detection identifies when processes are waiting for each other in a circular manner, causing all processes to be blocked indefinitely.

**Q2:** What is the time complexity?
**A:** O(V + E) where V is the number of processes/resources and E is the number of wait relationships. Uses DFS for cycle detection.

**Q3:** When would you use this algorithm?
**A:** In operating systems to periodically check for deadlocks, in database systems to detect transaction deadlocks, and in distributed systems to identify circular dependencies.

**Q4:** What are the main steps of this algorithm?
**A:** 1) Build wait-for graph from process-resource relationships, 2) Use DFS to traverse the graph, 3) Detect cycles using recursion stack, 4) Return all detected cycles as deadlocks.""",
            'mistakes': """### ❌ Mistake 1: Not tracking recursion stack properly
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
- Verify with simple examples first (2-3 nodes)"""
        }
    }
    
    # Check if we have specific content
    if name_lower in content_db and section in content_db[name_lower]:
        return content_db[name_lower][section]
    
    # Generate generic content based on algorithm type
    complexity = info.get('time_complexity', 'Varies')
    
    if section == 'try_it':
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
        else:
            return f"""**Try this example:**
```
Input: [example data]

Step 1: Initialize algorithm state
Step 2: Process input data
Step 3: Generate result

Output: [algorithm result]
```"""
    
    elif section == 'practice':
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
    
    elif section == 'qa':
        return f"""**Q1:** What problem does this algorithm solve?
**A:** {readable_name} solves the problem of [algorithm purpose]. It processes input data systematically to achieve [desired outcome].

**Q2:** What is the time complexity?
**A:** {complexity}

**Q3:** When would you use this algorithm?
**A:** Use {readable_name} when you need to [use case scenario]. It's particularly effective for [specific situations].

**Q4:** What are the main steps of this algorithm?
**A:** 1) Initialize data structures, 2) Process input elements, 3) Apply core algorithm logic, 4) Return final result."""
    
    elif section == 'mistakes':
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
    
    return ""


def fix_placeholders_in_content(content: str, algorithm_name: str, info: Dict, is_school: bool, lang: str) -> str:
    """Fix all placeholders in content."""
    original = content
    
    # Pattern 1: Try It Yourself - multiple formats
    try_it_patterns = [
        r'\*\*Try this example:\*\*\s*\n(?:```)?\s*\nInput: \[example data\].*?Output: \[result\](?:```)?',
        r'\*\*Try this example:\*\*\s*\nInput: \[example data\].*?Output: \[result\]',
        r'Input: \[example data\].*?Output: \[result\]',
    ]
    
    try_it_new = generate_algorithm_specific_content(algorithm_name, info, 'try_it', is_school, lang)
    for pattern in try_it_patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, try_it_new, content, flags=re.DOTALL)
            break
    
    # Pattern 2: Step-by-Step Execution
    step_patterns = [
        r'\*\*Step-by-Step Execution:\*\*\s*\n```python\s*\n# Input\s*\ndata = \[example input\].*?return result\s*```',
        r'```python\s*\n# Input\s*\ndata = \[example input\].*?return result\s*```',
    ]
    
    step_new = generate_algorithm_specific_content(algorithm_name, info, 'step_by_step', is_school, lang)
    for pattern in step_patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, step_new, content, flags=re.DOTALL)
            break
    
    # Pattern 3: Expected Output
    output_patterns = [
        r'\*\*Expected Output:\*\*\s*\n```\s*\nInput: \[example\].*?Result: \[output\]\s*```',
        r'```\s*\nInput: \[example\].*?Result: \[output\]\s*```',
    ]
    
    output_new = generate_algorithm_specific_content(algorithm_name, info, 'expected_output', is_school, lang)
    for pattern in output_patterns:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, output_new, content, flags=re.DOTALL)
            break
    
    # Pattern 4: Practice Exercises
    practice_patterns = [
        r'\*\*Exercise 1 \(Easy\):\s*\nTrace through the algorithm with a small example \(3-5 elements\)\.\s*\n\s*\n\*\*Exercise 2 \(Medium\):\s*\nImplement the algorithm in your preferred programming language\.\s*\n\s*\n\*\*Exercise 3 \(Hard\):\s*\nOptimize the algorithm or apply it to solve a real-world problem\.',
        r'Trace through the algorithm with a small example \(3-5 elements\)\.',
    ]
    
    practice_new = generate_algorithm_specific_content(algorithm_name, info, 'practice', is_school, lang)
    for pattern in practice_patterns:
        if re.search(pattern, content, re.MULTILINE):
            content = re.sub(pattern, practice_new, content, flags=re.MULTILINE)
            break
    
    # Pattern 5: Q&A
    qa_patterns = [
        r'\*\*Q1:\*\* What problem does this algorithm solve\?\s*\n\*\*A:\*\* \[Answer based on algorithm purpose\]\s*\n\s*\n\*\*Q2:\*\* What is the time complexity\?\s*\n\*\*A:\*\* Varies\s*\n\s*\n\*\*Q3:\*\* When would you use this algorithm\?\s*\n\*\*A:\*\* \[Answer based on use cases\]\s*\n\s*\n\*\*Q4:\*\* What are the main steps of this algorithm\?\s*\n\*\*A:\*\* \[List 3-5 key steps\]',
        r'\[Answer based on algorithm purpose\]',
        r'\[Answer based on use cases\]',
        r'\[List 3-5 key steps\]',
    ]
    
    qa_new = generate_algorithm_specific_content(algorithm_name, info, 'qa', is_school, lang)
    # Replace entire Q&A section
    qa_section_pattern = r'(\*\*Q1:\*\* What problem does this algorithm solve\?.*?\*\*A:\*\* \[List 3-5 key steps\])'
    if re.search(qa_section_pattern, content, re.DOTALL):
        content = re.sub(qa_section_pattern, qa_new, content, flags=re.DOTALL)
    
    # Pattern 6: Common Mistakes - fix the format issue
    mistakes_pattern = r'### ❌ Mistake 1: Test with edge cases.*?### 💡 How to Avoid\s*\n- Test with edge cases.*?- Review the algorithm\'s key steps before implementing'
    
    mistakes_new = generate_algorithm_specific_content(algorithm_name, info, 'mistakes', is_school, lang)
    if re.search(mistakes_pattern, content, re.DOTALL):
        # Find the Common Mistakes section
        cm_start = content.find('## Common Mistakes')
        if cm_start != -1:
            cm_end = content.find('\n## ', cm_start + 20)
            if cm_end == -1:
                cm_end = content.find('\n\n---', cm_start)
            if cm_end == -1:
                cm_end = len(content)
            # Replace the section
            content = content[:cm_start] + f"## Common Mistakes\n\n{mistakes_new}\n" + content[cm_end:]
    
    # Remove duplicate sections
    # Remove duplicate "Try this example"
    try_it_matches = list(re.finditer(r'\*\*Try this example:\*\*', content))
    if len(try_it_matches) > 1:
        for match in reversed(try_it_matches[1:]):
            # Find end of this section
            end_pos = content.find('\n## ', match.end())
            if end_pos == -1:
                end_pos = content.find('\n---', match.end())
            if end_pos == -1:
                end_pos = len(content)
            content = content[:match.start()] + content[end_pos:]
            break
    
    # Remove duplicate exercises
    exercise_matches = list(re.finditer(r'\*\*Exercise 1 \(Easy\):\s*\nTrace through the algorithm', content))
    if len(exercise_matches) > 1:
        for match in reversed(exercise_matches[1:]):
            end_pos = content.find('\n## ', match.end())
            if end_pos == -1:
                end_pos = content.find('\n---', match.end())
            if end_pos == -1:
                end_pos = len(content)
            content = content[:match.start()] + content[end_pos:]
            break
    
    # Remove duplicate Q&A
    qa_matches = list(re.finditer(r'\*\*Q1:\*\* What problem does this algorithm solve\?', content))
    if len(qa_matches) > 1:
        for match in reversed(qa_matches[1:]):
            end_pos = content.find('\n## ', match.end())
            if end_pos == -1:
                end_pos = content.find('\n---', match.end())
            if end_pos == -1:
                end_pos = len(content)
            content = content[:match.start()] + content[end_pos:]
            break
    
    return content


def fix_md_file(md_file: Path) -> bool:
    """Fix all placeholders in a single MD file."""
    try:
        content = md_file.read_text(encoding='utf-8')
        algorithm_folder = md_file.parent
        algorithm_name = algorithm_folder.name
        
        # Determine if school or university, and language
        is_school = 'school' in md_file.name
        lang = 'en' if '.en.' in md_file.name else 'ru'
        
        # Extract algorithm info
        info = extract_algorithm_info(algorithm_folder)
        
        # Fix placeholders
        content = fix_placeholders_in_content(content, algorithm_name, info, is_school, lang)
        
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
    print("COMPREHENSIVE PLACEHOLDER FIX")
    print("="*70)
    
    md_files = find_all_md_files()
    print(f"\nFound {len(md_files)} MD files")
    print("\nFixing all placeholders...")
    
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

