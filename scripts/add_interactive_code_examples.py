#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2.3: Add Interactive Code Examples:
- Step-by-step execution traces
- Variable state tracking
- Code output examples
- Execution walkthrough sections
"""

import sys
import re
import ast
from pathlib import Path
from typing import Dict, Optional, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, encoding='utf-8', errors='replace'
    )


def generate_step_by_step_execution(algorithm_name: str, category: str) -> str:
    """Generate step-by-step execution trace."""
    name_lower = algorithm_name.lower()
    readable_name = algorithm_name.replace('_', ' ').title()
    
    # Algorithm-specific execution traces
    executions = {
        'bubble_sort': """**Step-by-Step Execution:**

```python
# Input
arr = [5, 2, 8, 1, 9]
n = len(arr)  # n = 5

# Pass 1 (i = 0)
j = 0: Compare arr[0]=5 and arr[1]=2 → 5 > 2, swap → arr = [2, 5, 8, 1, 9]
j = 1: Compare arr[1]=5 and arr[2]=8 → 5 < 8, no swap → arr = [2, 5, 8, 1, 9]
j = 2: Compare arr[2]=8 and arr[3]=1 → 8 > 1, swap → arr = [2, 5, 1, 8, 9]
j = 3: Compare arr[3]=8 and arr[4]=9 → 8 < 9, no swap → arr = [2, 5, 1, 8, 9]
# Largest element (9) is now at the end

# Pass 2 (i = 1)
j = 0: Compare arr[0]=2 and arr[1]=5 → 2 < 5, no swap → arr = [2, 5, 1, 8, 9]
j = 1: Compare arr[1]=5 and arr[2]=1 → 5 > 1, swap → arr = [2, 1, 5, 8, 9]
j = 2: Compare arr[2]=5 and arr[3]=8 → 5 < 8, no swap → arr = [2, 1, 5, 8, 9]

# Pass 3 (i = 2)
j = 0: Compare arr[0]=2 and arr[1]=1 → 2 > 1, swap → arr = [1, 2, 5, 8, 9]
j = 1: Compare arr[1]=2 and arr[2]=5 → 2 < 5, no swap → arr = [1, 2, 5, 8, 9]

# Result
arr = [1, 2, 5, 8, 9]  # Sorted!
```""",
        'binary_search': """**Step-by-Step Execution:**

```python
# Input
arr = [1, 3, 5, 7, 9, 11, 13]
target = 7
left = 0
right = 6

# Iteration 1
mid = (0 + 6) // 2 = 3
arr[mid] = arr[3] = 7
7 == 7? Yes! Found at index 3

# Result
return 3
```

**Variable States:**
```
Iteration | left | right | mid | arr[mid] | Comparison | Action
----------|------|-------|-----|----------|------------|--------
    1     |  0   |   6   |  3  |    7     | 7 == 7     | Found!
```""",
        'quick_sort': """**Step-by-Step Execution:**

```python
# Input
arr = [5, 2, 8, 1, 9]

# Step 1: Choose pivot (middle element)
pivot = arr[2] = 8

# Step 2: Partition
# Elements < 8: [5, 2, 1]
# Elements = 8: [8]
# Elements > 8: [9]
left = [5, 2, 1]
right = [9]

# Step 3: Recursively sort left
quick_sort([5, 2, 1])
  → pivot = 2
  → left = [1], right = [5]
  → sorted_left = [1, 2, 5]

# Step 4: Combine
result = [1, 2, 5] + [8] + [9] = [1, 2, 5, 8, 9]
```""",
        'merge_sort': """**Step-by-Step Execution:**

```python
# Input
arr = [5, 2, 8, 1, 9]

# Step 1: Split
left = [5, 2, 8]
right = [1, 9]

# Step 2: Recursively sort halves
merge_sort([5, 2, 8])
  → Split: [5, 2] and [8]
  → Sort [5, 2]: [2, 5]
  → Merge: [2, 5, 8]
left_sorted = [2, 5, 8]

merge_sort([1, 9])
  → Already sorted
right_sorted = [1, 9]

# Step 3: Merge sorted halves
result = []
Compare 2 and 1 → 1 < 2, add 1 → result = [1]
Compare 2 and 9 → 2 < 9, add 2 → result = [1, 2]
Compare 5 and 9 → 5 < 9, add 5 → result = [1, 2, 5]
Compare 8 and 9 → 8 < 9, add 8 → result = [1, 2, 5, 8]
Add remaining 9 → result = [1, 2, 5, 8, 9]
```""",
        'fibonacci': """**Step-by-Step Execution (Dynamic Programming):**

```python
# Input
n = 5
memo = {}

# Step 1: Base cases
memo[0] = 0
memo[1] = 1

# Step 2: Build up
memo[2] = memo[1] + memo[0] = 1 + 0 = 1
memo[3] = memo[2] + memo[1] = 1 + 1 = 2
memo[4] = memo[3] + memo[2] = 2 + 1 = 3
memo[5] = memo[4] + memo[3] = 3 + 2 = 5

# Result
return memo[5] = 5
```

**Variable States:**
```
Step | memo[0] | memo[1] | memo[2] | memo[3] | memo[4] | memo[5]
-----|---------|---------|---------|---------|---------|--------
Init |    0    |    1    |    -    |    -    |    -    |    -
  1  |    0    |    1    |    1    |    -    |    -    |    -
  2  |    0    |    1    |    1    |    2    |    -    |    -
  3  |    0    |    1    |    1    |    2    |    3    |    -
  4  |    0    |    1    |    1    |    2    |    3    |    5
```"""
    }
    
    # Check for specific algorithm
    for key, execution in executions.items():
        if key in name_lower:
            return execution
    
    # Generic execution trace
    return f"""**Step-by-Step Execution:**

```python
# Input
data = [example input]

# Step 1: Initialize
state = initial_state

# Step 2: Process
# [Processing steps]

# Step 3: Finalize
result = final_state

# Output
return result
```"""


def generate_code_output(algorithm_name: str, category: str) -> str:
    """Generate expected code output."""
    name_lower = algorithm_name.lower()
    
    outputs = {
        'bubble_sort': """**Expected Output:**

```
Input: [5, 2, 8, 1, 9]
Pass 1: [2, 5, 8, 1, 9] (swapped 5 and 2)
Pass 2: [2, 5, 1, 8, 9] (swapped 8 and 1)
Pass 3: [2, 1, 5, 8, 9] (swapped 5 and 1)
Pass 4: [1, 2, 5, 8, 9] (swapped 2 and 1)
Sorted: [1, 2, 5, 8, 9]
```""",
        'binary_search': """**Expected Output:**

```
Searching for 7 in [1, 3, 5, 7, 9, 11, 13]
Checking index 3: value = 7
Found at index 3!
```""",
        'fibonacci': """**Expected Output:**

```
Computing Fibonacci(5):
F(0) = 0
F(1) = 1
F(2) = 1
F(3) = 2
F(4) = 3
F(5) = 5
Result: 5
```"""
    }
    
    if name_lower in outputs:
        return outputs[name_lower]
    
    return f"""**Expected Output:**

```
Input: [example]
Processing...
Result: [output]
```"""


def add_execution_section(content: str, algorithm_name: str, category: str) -> str:
    """Add step-by-step execution section."""
    # Check if section already exists
    if "## 🔍 Step-by-Step Execution" in content or "## Step-by-Step Execution" in content:
        return content
    
    execution = generate_step_by_step_execution(algorithm_name, category)
    output = generate_code_output(algorithm_name, category)
    
    # Find insertion point (after "Try It Yourself" or before "Practice Exercise")
    insert_positions = [
        ('## ✏️ Practice Exercise', 'before'),
        ('## ✅ Check Your Understanding', 'before'),
        ('## 🎯 Try It Yourself', 'after')
    ]
    
    section = f"\n## 🔍 Step-by-Step Execution\n\n{execution}\n\n{output}\n\n"
    
    for marker, position in insert_positions:
        if marker in content:
            pos = content.find(marker)
            if position == 'before':
                content = content[:pos] + section + content[pos:]
            else:
                # Find end of section
                next_section = content.find('\n## ', pos + len(marker))
                if next_section != -1:
                    content = content[:next_section] + section + content[next_section:]
                else:
                    content = content + section
            return content
    
    # If no good position, add before Practice Exercise
    if "## ✏️" in content:
        pos = content.find("## ✏️")
        content = content[:pos] + section + content[pos:]
    else:
        # Add at end
        content = content + section
    
    return content


def improve_md_file(md_file: Path) -> bool:
    """Add interactive code examples to a single MD file."""
    try:
        content = md_file.read_text(encoding='utf-8')
        algorithm_folder = md_file.parent
        algorithm_name = algorithm_folder.name
        
        # Get category
        metadata_path = algorithm_folder / "metadata.json"
        category = "Algorithms"
        if metadata_path.exists():
            try:
                import json
                metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
                if metadata.get('category'):
                    category = metadata['category']
            except:
                pass
        
        # Add execution section
        content = add_execution_section(content, algorithm_name, category)
        
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
    print("PHASE 2.3: ADDING INTERACTIVE CODE EXAMPLES")
    print("="*70)
    
    md_files = find_all_md_files()
    print(f"\nFound {len(md_files)} MD files")
    print("\nAdding:")
    print("  - Step-by-step execution traces")
    print("  - Variable state tracking")
    print("  - Code output examples")
    print("  - Execution walkthrough sections")
    
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

