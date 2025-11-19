#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhance all algorithm README.md files with comprehensive explanations.
Ensures all READMEs have: steps, usage, advantages, disadvantages, examples.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
import json

ROOT = Path(__file__).resolve().parents[1]

# Required sections for comprehensive README
REQUIRED_SECTIONS = [
    "## TL;DR",
    "## Learning Objectives",
    "## Prerequisites",
    "## Introduction",
    "## Short Description",
    "## Algorithm Steps",
    "## Detailed Explanation",
    "## Usage Examples",
    "## Advantages",
    "## Disadvantages",
    "## Time Complexity",
    "## Space Complexity",
    "## Stability",
    "## When to Use",
    "## When NOT to Use",
    "## Real-World Applications",
    "## Common Mistakes",
    "## Implementation Notes",
    "## Related Algorithms",
    "## Further Reading",
]


def extract_algorithm_info(readme_path: Path) -> Dict:
    """Extract current information from README."""
    if not readme_path.exists():
        return {}

    content = readme_path.read_text(encoding="utf-8")
    info = {"name": readme_path.parent.name, "content": content, "sections": {}}

    # Extract existing sections
    for section in REQUIRED_SECTIONS:
        pattern = rf"{re.escape(section)}\s*\n\n(.*?)(?=\n##|\Z)"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            info["sections"][section] = match.group(1).strip()

    return info


def generate_algorithm_steps(algorithm_name: str, category: str) -> str:
    """Generate step-by-step algorithm explanation."""
    steps_templates = {
        "bubble_sort": """1. **Start**: Begin with the first element of the array
2. **Compare**: Compare the current element with the next element
3. **Swap if needed**: If current element is greater than next, swap them
4. **Move forward**: Move to the next pair of elements
5. **Repeat**: Continue until the end of the array
6. **Next pass**: Start again from the beginning (one less element each time)
7. **Terminate**: Stop when no swaps occur in a complete pass

**Visual Example**:
```
Initial: [64, 34, 25, 12, 22, 11, 90]
Pass 1:  [34, 25, 12, 22, 11, 64, 90]  (64 bubbles up)
Pass 2:  [25, 12, 22, 11, 34, 64, 90]  (34 bubbles up)
...
Final:   [11, 12, 22, 25, 34, 64, 90]
```""",
        "quick_sort": """1. **Choose pivot**: Select a pivot element (typically last element)
2. **Partition**: Rearrange array so elements < pivot are left, > pivot are right
3. **Place pivot**: Put pivot in its correct sorted position
4. **Recurse left**: Apply quick sort to left subarray (elements < pivot)
5. **Recurse right**: Apply quick sort to right subarray (elements > pivot)
6. **Base case**: When subarray has 0 or 1 element, it's already sorted

**Partition Process**:
```
Array: [10, 80, 30, 90, 40, 50, 70]
Pivot: 70
After partition: [10, 30, 40, 50, 70, 90, 80]
                  [< 70]  [70]  [> 70]
```""",
        "binary_search": """1. **Start**: Set left = 0, right = array.length - 1
2. **Calculate mid**: mid = (left + right) / 2
3. **Compare**: Compare target with array[mid]
4. **If equal**: Return mid (found!)
5. **If target < array[mid]**: Search left half (right = mid - 1)
6. **If target > array[mid]**: Search right half (left = mid + 1)
7. **Repeat**: Continue until left > right
8. **Not found**: Return -1 or None

**Example**:
```
Array: [1, 3, 5, 7, 9, 11, 13], Target: 7
Step 1: mid = 3, array[3] = 7, found!
```""",
        "bfs": """1. **Initialize**: Create queue, mark start node as visited
2. **Enqueue start**: Add start node to queue
3. **Dequeue**: Remove node from front of queue
4. **Process**: Visit current node
5. **Enqueue neighbors**: Add all unvisited neighbors to queue
6. **Mark visited**: Mark neighbors as visited
7. **Repeat**: Continue until queue is empty

**Level-order traversal**:
```
Level 0: A
Level 1: B, C
Level 2: D, E, F
```""",
    }

    # Try exact match first
    if algorithm_name in steps_templates:
        return steps_templates[algorithm_name]

    # Try partial match
    for key, template in steps_templates.items():
        if key in algorithm_name.lower():
            return template

    # Generic template
    return f"""1. **Initialization**: Set up initial state and data structures
2. **Main loop**: Process elements until termination condition
3. **Comparison/Operation**: Perform core algorithm operation
4. **Update state**: Modify data structures based on operation
5. **Check termination**: Verify if algorithm should continue
6. **Return result**: Output final result when complete

*Note: Specific steps depend on the algorithm implementation. See code for details.*"""


def generate_usage_examples(algorithm_name: str, category: str) -> str:
    """Generate comprehensive usage examples."""
    examples = {
        "sort": """### Example 1: Basic Sorting
```python
from semester_01.lecture_01_sorting_fundamentals.bubble_sort.algorithm import bubble_sort

# Sort a list of numbers
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers)
print(sorted_numbers)  # [11, 12, 22, 25, 34, 64, 90]
```

### Example 2: Sorting Custom Objects
```python
# Sort by custom key
students = [
    {'name': 'Alice', 'grade': 85},
    {'name': 'Bob', 'grade': 92},
    {'name': 'Charlie', 'grade': 78}
]
sorted_students = sorted(students, key=lambda x: x['grade'])
```

### Example 3: Real-World Application
```python
# Sorting products by price for e-commerce
products = get_products_from_database()
sorted_products = bubble_sort([p.price for p in products])
```""",
        "search": """### Example 1: Basic Search
```python
from semester_01.lecture_04_searching.binary_search.algorithm import binary_search

# Search in sorted array
sorted_array = [1, 3, 5, 7, 9, 11, 13, 15]
index = binary_search(sorted_array, 7)
print(f"Found at index: {index}")  # 3
```

### Example 2: Search with Custom Comparator
```python
# Search in list of objects
class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name

students = [Student(1, 'Alice'), Student(2, 'Bob'), Student(3, 'Charlie')]
target = binary_search([s.id for s in students], 2)
```

### Example 3: Real-World Application
```python
# Searching user database
user_ids = sorted([user.id for user in users])
user_index = binary_search(user_ids, target_user_id)
if user_index != -1:
    user = users[user_index]
```""",
        "graph": """### Example 1: Basic Graph Traversal
```python
from semester_01.lecture_09_graph_algorithms.bfs.algorithm import bfs

# Graph as adjacency list
graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 5],
    3: [1],
    4: [1, 5],
    5: [2, 4]
}

# BFS from node 0
visited = bfs(graph, 0)
print(visited)  # [0, 1, 2, 3, 4, 5]
```

### Example 2: Finding Shortest Path
```python
# Find shortest path in unweighted graph
path = bfs_shortest_path(graph, start=0, end=5)
print(path)  # [0, 2, 5]
```

### Example 3: Real-World Application
```python
# Social network friend recommendations
user_graph = build_social_graph(users)
recommendations = bfs(user_graph, current_user_id, depth=2)
```""",
    }

    # Determine category
    if "sort" in algorithm_name.lower() or "sort" in category.lower():
        return examples.get("sort", examples["sort"])
    elif "search" in algorithm_name.lower() or "search" in category.lower():
        return examples.get("search", examples["search"])
    elif "graph" in algorithm_name.lower() or "graph" in category.lower():
        return examples.get("graph", examples["graph"])

    return """### Example 1: Basic Usage
```python
from [algorithm_path].algorithm import [function_name]

# Basic example
result = [function_name](input_data)
print(result)
```

### Example 2: With Parameters
```python
# Advanced usage with options
result = [function_name](input_data, option1=True, option2=value)
```

### Example 3: Real-World Application
```python
# Practical use case
data = load_real_world_data()
processed = [function_name](data)
save_results(processed)
```"""


def generate_advantages(algorithm_name: str, category: str) -> str:
    """Generate advantages section."""
    advantages_templates = {
        "bubble_sort": """- **Simplicity**: Very easy to understand and implement
- **In-place sorting**: Requires only O(1) extra space
- **Stable**: Maintains relative order of equal elements
- **Adaptive**: Can detect if array is already sorted (optimized version)
- **No recursion**: Avoids stack overflow issues
- **Good for small datasets**: Efficient for small arrays (< 10 elements)""",
        "quick_sort": """- **Fast average case**: O(n log n) average time complexity
- **In-place sorting**: Low memory overhead
- **Cache efficient**: Good locality of reference
- **Widely used**: Standard sorting algorithm in many libraries
- **Parallelizable**: Can be easily parallelized
- **Efficient for large datasets**: Performs well on large arrays""",
        "binary_search": """- **Very fast**: O(log n) time complexity
- **Efficient**: Only examines log(n) elements
- **Memory efficient**: O(1) space complexity (iterative version)
- **Deterministic**: Always finds element if it exists
- **Scalable**: Performance doesn't degrade much with large arrays
- **Foundation**: Basis for many advanced algorithms""",
    }

    for key, template in advantages_templates.items():
        if key in algorithm_name.lower():
            return template

    return """- **Efficiency**: Optimized for specific use cases
- **Reliability**: Well-tested and proven approach
- **Scalability**: Handles large inputs effectively
- **Flexibility**: Can be adapted for various scenarios
- **Industry standard**: Widely recognized and used"""


def generate_disadvantages(algorithm_name: str, category: str) -> str:
    """Generate disadvantages section."""
    disadvantages_templates = {
        "bubble_sort": """- **Slow**: O(n²) time complexity makes it inefficient for large arrays
- **Many comparisons**: Compares every pair of elements
- **Not practical**: Rarely used in production code
- **Poor cache performance**: Not cache-friendly
- **Not optimal**: Better algorithms exist for most cases
- **Worst case**: Same as average case (no early termination benefit)""",
        "quick_sort": """- **Worst case**: O(n²) if pivot is always smallest/largest
- **Unstable**: May change relative order of equal elements
- **Pivot selection**: Performance depends on good pivot choice
- **Recursion overhead**: Stack space for recursive calls
- **Not adaptive**: Doesn't take advantage of partially sorted arrays
- **Complex implementation**: More complex than simple sorts""",
        "binary_search": """- **Requires sorted array**: Input must be sorted beforehand
- **Not suitable for unsorted data**: Cannot be used directly
- **Static data**: Less efficient if data changes frequently
- **Memory access**: May have poor cache performance
- **Integer overflow**: (left + right) / 2 can overflow (use left + (right - left) / 2)
- **Limited to arrays**: Not directly applicable to linked lists""",
    }

    for key, template in disadvantages_templates.items():
        if key in algorithm_name.lower():
            return template

    return """- **Limitations**: May not work for all input types
- **Complexity**: Can be complex to implement correctly
- **Trade-offs**: May sacrifice one aspect for another
- **Dependencies**: May require specific data structures
- **Edge cases**: Requires careful handling of edge cases"""


def enhance_readme(readme_path: Path) -> bool:
    """Enhance a single README file."""
    info = extract_algorithm_info(readme_path)
    if not info:
        return False

    algorithm_name = info["name"]
    content = info["content"]

    # Read metadata for category
    metadata_path = readme_path.parent / "metadata.json"
    category = "algorithm"
    if metadata_path.exists():
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            category = metadata.get("category", "algorithm")
        except:
            pass

    changes_made = False

    # Add missing sections
    sections_to_add = {}

    # Algorithm Steps
    if "## Algorithm Steps" not in content:
        sections_to_add["## Algorithm Steps"] = generate_algorithm_steps(
            algorithm_name, category
        )
        changes_made = True

    # Detailed Explanation (if missing)
    if "## Detailed Explanation" not in content and "## How It Works" not in content:
        sections_to_add[
            "## Detailed Explanation"
        ] = f"""The {algorithm_name.replace('_', ' ').title()} algorithm works by systematically processing the input data according to its specific strategy.

**Key Concepts**:
- Core principle: [Describe main idea]
- Data structures used: [List structures]
- Termination condition: [When algorithm stops]

**Process Flow**:
1. Initialize necessary data structures
2. Process input elements according to algorithm logic
3. Update state after each operation
4. Continue until termination condition is met
5. Return final result

For detailed implementation, see `algorithm.py` and `Algorithm.java`."""
        changes_made = True

    # Usage Examples
    if "## Usage Examples" not in content and "## Examples" not in content:
        sections_to_add["## Usage Examples"] = generate_usage_examples(
            algorithm_name, category
        )
        changes_made = True

    # Advantages
    if "## Advantages" not in content and "## Key Advantages" not in content:
        sections_to_add["## Advantages"] = generate_advantages(algorithm_name, category)
        changes_made = True

    # Disadvantages
    if "## Disadvantages" not in content and "## Key Disadvantages" not in content:
        sections_to_add["## Disadvantages"] = generate_disadvantages(
            algorithm_name, category
        )
        changes_made = True

    # When to Use
    if "## When to Use" not in content:
        sections_to_add[
            "## When to Use"
        ] = f"""Use {algorithm_name.replace('_', ' ').title()} when:

- **Specific scenario 1**: [When this is appropriate]
- **Specific scenario 2**: [Another use case]
- **Data characteristics**: [What kind of data works best]
- **Performance requirements**: [When performance is acceptable]
- **Constraints**: [When constraints are met]

**Ideal conditions**:
- Input size: [Small/Medium/Large]
- Data type: [Sorted/Unsorted, etc.]
- Memory constraints: [Available memory]
- Time constraints: [Acceptable time]"""
        changes_made = True

    # When NOT to Use
    if "## When NOT to Use" not in content:
        sections_to_add[
            "## When NOT to Use"
        ] = f"""Avoid {algorithm_name.replace('_', ' ').title()} when:

- **Scenario 1**: [When this is not appropriate]
- **Scenario 2**: [Another case to avoid]
- **Data characteristics**: [What kind of data doesn't work]
- **Performance requirements**: [When performance is insufficient]
- **Constraints**: [When constraints are not met]

**Poor fit conditions**:
- Input size: [Too large/small]
- Data type: [Incompatible data]
- Memory constraints: [Insufficient memory]
- Time constraints: [Too strict]"""
        changes_made = True

    # Insert new sections before "## Related Algorithms" or at end
    if sections_to_add:
        # Find insertion point (before Related Algorithms or at end)
        insertion_point = content.find("## Related Algorithms")
        if insertion_point == -1:
            insertion_point = content.find("## Further Reading")
        if insertion_point == -1:
            insertion_point = len(content)

        # Build new sections text
        new_sections = "\n\n".join(
            [f"{header}\n\n{body}" for header, body in sections_to_add.items()]
        )

        # Insert before insertion point
        content = (
            content[:insertion_point].rstrip()
            + "\n\n"
            + new_sections
            + "\n\n"
            + content[insertion_point:].lstrip()
        )

        readme_path.write_text(content, encoding="utf-8")

    return changes_made


def main():
    """Enhance all README files."""
    readme_files = list(ROOT.rglob("*/README.md"))
    total = len(readme_files)
    enhanced = 0

    print(f"Enhancing {total} README files...")

    for readme_path in readme_files:
        # Skip root README
        if readme_path.parent == ROOT:
            continue

        try:
            if enhance_readme(readme_path):
                enhanced += 1
                if enhanced % 50 == 0:
                    print(f"[PROGRESS] Enhanced {enhanced}/{total} README files...")
        except Exception as e:
            print(f"Error enhancing {readme_path}: {e}")

    print(f"\n[COMPLETE] Enhanced {enhanced} README files")


if __name__ == "__main__":
    main()
