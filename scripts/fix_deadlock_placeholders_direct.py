#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct fix for deadlock_detection placeholders as a test.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def fix_deadlock_file(md_file: Path) -> bool:
    """Fix deadlock detection file directly."""
    try:
        content = md_file.read_text(encoding='utf-8')
        original = content
        
        # Fix Try It Yourself - match flexible format
        # Find the section and replace content between markers
        try_it_start = content.find('## 🎯 Try It Yourself')
        if try_it_start != -1:
            try_it_end = content.find('\n---', try_it_start)
            if try_it_end == -1:
                try_it_end = content.find('\n## ', try_it_start + 20)
            if try_it_end != -1:
                old_try_it = content[try_it_start:try_it_end]
        
        new_try_it = """## 🎯 Try It Yourself

**Try detecting a deadlock:**
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
        
                content = content[:try_it_start] + new_try_it + content[try_it_end:]
        
        # Fix Step-by-Step Execution - find section
        step_start = content.find('## 🔍 Step-by-Step Execution')
        if step_start != -1:
            step_end = content.find('\n## ', step_start + 30)
            if step_end == -1:
                step_end = content.find('\n---', step_start + 30)
            if step_end == -1:
                step_end = len(content)
            old_step = content[step_start:step_end]
        
        new_step = """## 🔍 Step-by-Step Execution

**Step-by-Step Execution:**

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
```

**Expected Output:**

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
        
            content = content[:step_start] + new_step + content[step_end:]
        
        # Fix Practice Exercises
        old_practice = """**Exercise 1 (Easy):**
Trace through the algorithm with a small example (3-5 elements).

**Exercise 2 (Medium):**
Implement the algorithm in your preferred programming language.

**Exercise 3 (Hard):**
Optimize the algorithm or apply it to solve a real-world problem."""
        
        new_practice = """**Exercise 1 (Easy):**
Create a wait-for graph with 3 processes and detect if there's a deadlock. Draw the graph and trace the DFS.

**Exercise 2 (Medium):**
Implement deadlock detection for a system with multiple processes and resources. Handle edge cases (no cycles, multiple cycles).

**Exercise 3 (Hard):**
Design a deadlock detection system that runs periodically in an operating system. Consider performance and false positives."""
        
        content = content.replace(old_practice, new_practice)
        
        # Fix Q&A - replace all occurrences
        old_qa = """**Q1:** What problem does this algorithm solve?
**A:** [Answer based on algorithm purpose]

**Q2:** What is the time complexity?
**A:** Varies

**Q3:** When would you use this algorithm?
**A:** [Answer based on use cases]

**Q4:** What are the main steps of this algorithm?
**A:** [List 3-5 key steps]"""
        
        new_qa = """**Q1:** What problem does this algorithm solve?
**A:** Deadlock Detection identifies when processes are waiting for each other in a circular manner, causing all processes to be blocked indefinitely.

**Q2:** What is the time complexity?
**A:** O(V + E) where V is the number of processes/resources and E is the number of wait relationships. Uses DFS for cycle detection.

**Q3:** When would you use this algorithm?
**A:** In operating systems to periodically check for deadlocks, in database systems to detect transaction deadlocks, and in distributed systems to identify circular dependencies.

**Q4:** What are the main steps of this algorithm?
**A:** 1) Build wait-for graph from process-resource relationships, 2) Use DFS to traverse the graph, 3) Detect cycles using recursion stack, 4) Return all detected cycles as deadlocks."""
        
        content = content.replace(old_qa, new_qa)
        
        # Fix Common Mistakes
        old_mistakes = """## Common Mistakes

### ❌ Mistake 1: Test with edge cases (empty input, single element, boundary values)
**Solution:** Add validation: `if not data or len(data) <= 1: return data`

### ❌ Mistake 2: Trace through examples step-by-step
**Solution:** Manually trace through a small example (3-5 elements) to verify each step matches the algorithm logic

### ❌ Mistake 3: Use debugging tools to verify your logic
**Solution:** Use print statements or debugger to check variable values at each step, compare with expected behavior

### ❌ Mistake 4: Review the algorithm's key steps before implementing
**Solution:** Study the algorithm's pseudocode or description, identify the core steps, then implement one step at a time

### 💡 How to Avoid
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify your logic
- Review the algorithm's key steps before implementing"""
        
        new_mistakes = """## Common Mistakes

### ❌ Mistake 1: Not tracking recursion stack properly
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
        
        content = content.replace(old_mistakes, new_mistakes)
        
        # Remove duplicate sections
        # Remove duplicate "Try this example" that appears later
        lines = content.split('\n')
        new_lines = []
        skip_until_section = False
        for i, line in enumerate(lines):
            if line == '**Try this example:**' and i > 100:  # After first occurrence
                # Skip until next section
                skip_until_section = True
                continue
            if skip_until_section:
                if line.startswith('##') or line.startswith('---'):
                    skip_until_section = False
                    new_lines.append(line)
                continue
            new_lines.append(line)
        content = '\n'.join(new_lines)
        
        # Remove duplicate exercises
        exercise_count = 0
        new_lines = []
        for line in content.split('\n'):
            if line == '**Exercise 1 (Easy):**':
                exercise_count += 1
                if exercise_count > 1:
                    # Skip until next section
                    skip_until_section = True
                    continue
            if skip_until_section:
                if line.startswith('##') or line.startswith('---'):
                    skip_until_section = False
                    new_lines.append(line)
                continue
            new_lines.append(line)
        content = '\n'.join(new_lines)
        
        if content != original:
            md_file.write_text(content, encoding='utf-8')
            return True
        return True
    except Exception as e:
        print(f"  [ERROR] {md_file.name}: {e}")
        import traceback
        traceback.print_exc()
        return False


# Test on deadlock_detection file
deadlock_file = ROOT / "semester_07" / "lecture_39_operating_systems" / "deadlock_detection" / "school.en.md"
if deadlock_file.exists():
    print("Fixing deadlock_detection/school.en.md...")
    fix_deadlock_file(deadlock_file)
    print("Done!")
else:
    print(f"File not found: {deadlock_file}")

