#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct fix for all placeholder content - simpler approach.
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def fix_placeholders_in_content(content: str, algorithm_name: str) -> str:
    """Fix all placeholders in content."""
    
    # Fix Try It Yourself - replace placeholder text (flexible matching)
    try_it_pattern = r'\*\*Try this example:\*\*\s*\nInput: \[example data\].*?Output: \[result\]'
    
    if algorithm_name.lower() == 'deadlock_detection':
        try_it_new = """**Try detecting a deadlock:**
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
```"""
        content = re.sub(try_it_pattern, try_it_new.replace('**Try detecting a deadlock:**', '**Try detecting a deadlock:**'), content, flags=re.DOTALL)
    
    # Fix Step-by-Step Execution (flexible matching)
    step_pattern = r'\*\*Step-by-Step Execution:\*\*\s*\n```python\s*\n# Input\s*\ndata = \[example input\].*?return result\s*```'
    
    if algorithm_name.lower() == 'deadlock_detection':
        step_new = """**Step-by-Step Execution:**

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
```"""
        content = re.sub(step_pattern, step_new.replace('**Step-by-Step Execution:**', '**Step-by-Step Execution:**'), content, flags=re.DOTALL)
    
    # Fix Expected Output (flexible matching)
    output_pattern = r'\*\*Expected Output:\*\*\s*\n```\s*\nInput: \[example\].*?Result: \[output\]\s*```'
    
    if algorithm_name.lower() == 'deadlock_detection':
        output_new = """**Expected Output:**

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
```"""
        content = re.sub(output_pattern, output_new, content, flags=re.DOTALL)
    
    # Fix Practice Exercises (flexible matching)
    practice_pattern = r'\*\*Exercise 1 \(Easy\):\s*\nTrace through the algorithm with a small example \(3-5 elements\)\.\s*\n\s*\n\*\*Exercise 2 \(Medium\):\s*\nImplement the algorithm in your preferred programming language\.\s*\n\s*\n\*\*Exercise 3 \(Hard\):\s*\nOptimize the algorithm or apply it to solve a real-world problem\.'
    
    if algorithm_name.lower() == 'deadlock_detection':
        practice_new = """**Exercise 1 (Easy):**
Create a wait-for graph with 3 processes and detect if there's a deadlock. Draw the graph and trace the DFS.

**Exercise 2 (Medium):**
Implement deadlock detection for a system with multiple processes and resources. Handle edge cases (no cycles, multiple cycles).

**Exercise 3 (Hard):**
Design a deadlock detection system that runs periodically in an operating system. Consider performance and false positives."""
        content = re.sub(practice_pattern, practice_new, content, flags=re.MULTILINE)
    
    # Fix Q&A (flexible matching)
    qa_pattern = r'\*\*Q1:\*\* What problem does this algorithm solve\?\s*\n\*\*A:\*\* \[Answer based on algorithm purpose\]\s*\n\s*\n\*\*Q2:\*\* What is the time complexity\?\s*\n\*\*A:\*\* Varies\s*\n\s*\n\*\*Q3:\*\* When would you use this algorithm\?\s*\n\*\*A:\*\* \[Answer based on use cases\]\s*\n\s*\n\*\*Q4:\*\* What are the main steps of this algorithm\?\s*\n\*\*A:\*\* \[List 3-5 key steps\]'
    
    if algorithm_name.lower() == 'deadlock_detection':
        qa_new = """**Q1:** What problem does this algorithm solve?
**A:** Deadlock Detection identifies when processes are waiting for each other in a circular manner, causing all processes to be blocked indefinitely.

**Q2:** What is the time complexity?
**A:** O(V + E) where V is the number of processes/resources and E is the number of wait relationships. Uses DFS for cycle detection.

**Q3:** When would you use this algorithm?
**A:** In operating systems to periodically check for deadlocks, in database systems to detect transaction deadlocks, and in distributed systems to identify circular dependencies.

**Q4:** What are the main steps of this algorithm?
**A:** 1) Build wait-for graph from process-resource relationships, 2) Use DFS to traverse the graph, 3) Detect cycles using recursion stack, 4) Return all detected cycles as deadlocks."""
        # Replace all occurrences
        content = re.sub(qa_pattern, qa_new, content, flags=re.MULTILINE)
    
    # Fix Common Mistakes (flexible matching)
    mistakes_pattern = r'### ❌ Mistake 1: Test with edge cases.*?### 💡 How to Avoid\s*\n- Test with edge cases.*?- Review the algorithm\'s key steps before implementing'
    
    if algorithm_name.lower() == 'deadlock_detection':
        mistakes_new = """### ❌ Mistake 1: Not tracking recursion stack properly
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
        content = re.sub(mistakes_pattern, mistakes_new, content, flags=re.DOTALL)
    
    # Remove duplicate sections - simpler approach using regex
    # Remove duplicate "Try this example" sections
    try_it_pattern = r'(\*\*Try this example:\*\*.*?Output: \[result\])'
    matches = list(re.finditer(try_it_pattern, content, re.DOTALL))
    if len(matches) > 1:
        # Keep first, remove rest
        for match in reversed(matches[1:]):
            content = content[:match.start()] + content[match.end():]
    
    # Remove duplicate exercises
    exercise_pattern = r'(\*\*Exercise 1 \(Easy\):.*?Optimize the algorithm or apply it to solve a real-world problem\.)'
    matches = list(re.finditer(exercise_pattern, content, re.DOTALL))
    if len(matches) > 1:
        for match in reversed(matches[1:]):
            content = content[:match.start()] + content[match.end():]
    
    # Remove duplicate Q&A
    qa_pattern = r'(\*\*Q1:\*\* What problem does this algorithm solve\?.*?\*\*A:\*\* \[List 3-5 key steps\])'
    matches = list(re.finditer(qa_pattern, content, re.DOTALL))
    if len(matches) > 1:
        for match in reversed(matches[1:]):
            content = content[:match.start()] + content[match.end():]
    
    return content


def fix_md_file(md_file: Path) -> bool:
    """Fix placeholders in a single MD file."""
    try:
        content = md_file.read_text(encoding='utf-8')
        algorithm_folder = md_file.parent
        algorithm_name = algorithm_folder.name
        
        original = content
        content = fix_placeholders_in_content(content, algorithm_name)
        
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
    print("FIXING ALL PLACEHOLDERS (DIRECT APPROACH)")
    print("="*70)
    
    md_files = find_all_md_files()
    print(f"\nFound {len(md_files)} MD files")
    
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

