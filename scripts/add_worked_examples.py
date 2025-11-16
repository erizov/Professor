#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add worked examples section to algorithm README files.
Creates step-by-step walkthroughs for better understanding.
"""

import re
from pathlib import Path
from typing import Dict, Optional

ROOT = Path(__file__).resolve().parents[1]

# Worked examples for specific algorithms
WORKED_EXAMPLES: Dict[str, str] = {
    "quick_sort": """## Worked Example: Sorting [5, 2, 8, 1, 9] with Quick Sort

**Step 1: Choose Pivot**
- Array: [5, 2, 8, 1, 9]
- Pivot: 5 (first element)
- Why: Simple choice for demonstration

**Step 2: Partition**
- Compare 2 < 5? Yes → move to left
- Compare 8 < 5? No → move to right
- Compare 1 < 5? Yes → move to left
- Compare 9 < 5? No → move to right
- Result: [2, 1] [5] [8, 9]

**Step 3: Recursively Sort Left Subarray [2, 1]**
- Pivot: 2
- Partition: [1] [2] []
- Left [1] is sorted (single element)
- Result: [1, 2]

**Step 4: Recursively Sort Right Subarray [8, 9]**
- Pivot: 8
- Partition: [] [8] [9]
- Right [9] is sorted (single element)
- Result: [8, 9]

**Step 5: Combine**
- Left: [1, 2]
- Pivot: [5]
- Right: [8, 9]
- Final: [1, 2, 5, 8, 9]

**Key Insight**: Each partition places the pivot in its final position, then we recursively sort the subarrays.""",

    "merge_sort": """## Worked Example: Sorting [5, 2, 8, 1] with Merge Sort

**Step 1: Divide**
- Split [5, 2, 8, 1] into [5, 2] and [8, 1]
- Split [5, 2] into [5] and [2]
- Split [8, 1] into [8] and [1]

**Step 2: Conquer (Base Case)**
- Single elements are already sorted: [5], [2], [8], [1]

**Step 3: Merge [5] and [2]**
- Compare 5 and 2: 2 < 5 → [2, 5]

**Step 4: Merge [8] and [1]**
- Compare 8 and 1: 1 < 8 → [1, 8]

**Step 5: Merge [2, 5] and [1, 8]**
- Compare 2 and 1: 1 < 2 → [1]
- Compare 2 and 8: 2 < 8 → [1, 2]
- Compare 5 and 8: 5 < 8 → [1, 2, 5]
- Add remaining: [1, 2, 5, 8]

**Key Insight**: Merge sort guarantees O(n log n) by always dividing in half and merging in linear time.""",

    "binary_search": """## Worked Example: Finding 7 in [1, 3, 5, 7, 9, 11, 13]

**Step 1: Initialize**
- Array: [1, 3, 5, 7, 9, 11, 13]
- Target: 7
- Left: 0, Right: 6

**Step 2: First Iteration**
- Middle: (0 + 6) / 2 = 3
- Array[3] = 7
- 7 == 7? Yes → Found at index 3!

**Example: Finding 4 (not present)**
- Step 1: Left=0, Right=6, Middle=3, Array[3]=7
- 4 < 7 → search left: Left=0, Right=2
- Step 2: Middle=1, Array[1]=3
- 4 > 3 → search right: Left=2, Right=2
- Step 3: Middle=2, Array[2]=5
- 4 < 5 → search left: Left=2, Right=1
- Left > Right → Not found

**Key Insight**: Each comparison eliminates half the search space, giving O(log n) performance.""",

    "bfs": """## Worked Example: BFS on Graph

Graph:
```
     A
    / \\
   B   C
  / \\ / \\
 D   E   F
```

**Step 1: Start at A**
- Queue: [A]
- Visited: {A}
- Result: [A]

**Step 2: Process A**
- Neighbors: B, C
- Queue: [B, C]
- Visited: {A, B, C}
- Result: [A, B, C]

**Step 3: Process B**
- Neighbors: D, E (A already visited)
- Queue: [C, D, E]
- Visited: {A, B, C, D, E}
- Result: [A, B, C, D, E]

**Step 4: Process C**
- Neighbors: E, F (A already visited)
- E already visited, add F
- Queue: [D, E, F]
- Visited: {A, B, C, D, E, F}
- Result: [A, B, C, D, E, F]

**Step 5: Process Remaining**
- D, E, F have no unvisited neighbors
- Queue becomes empty
- Final: [A, B, C, D, E, F]

**Key Insight**: BFS explores level by level, ensuring shortest path discovery in unweighted graphs.""",

    "dijkstra": """## Worked Example: Dijkstra's Shortest Path

Graph (weighted):
```
    A --3-- B
    |       |
    1       2
    |       |
    C --4-- D
```

Find shortest path from A to all nodes.

**Step 1: Initialize**
- Distances: A=0, B=∞, C=∞, D=∞
- Priority Queue: [(0, A)]
- Visited: {}

**Step 2: Process A (distance 0)**
- Neighbors: B (weight 3), C (weight 1)
- Update: B = min(∞, 0+3) = 3, C = min(∞, 0+1) = 1
- Queue: [(1, C), (3, B)]
- Visited: {A}

**Step 3: Process C (distance 1)**
- Neighbors: A (visited), D (weight 4)
- Update: D = min(∞, 1+4) = 5
- Queue: [(3, B), (5, D)]
- Visited: {A, C}

**Step 4: Process B (distance 3)**
- Neighbors: A (visited), D (weight 2)
- Update: D = min(5, 3+2) = 5 (no change)
- Queue: [(5, D)]
- Visited: {A, C, B}

**Step 5: Process D (distance 5)**
- All neighbors visited
- Final distances: A=0, B=3, C=1, D=5

**Key Insight**: Always process the closest unvisited vertex first, guaranteeing shortest paths.""",
}

def get_worked_example(algorithm_name: str) -> Optional[str]:
    """Get worked example for algorithm."""
    normalized = algorithm_name.lower().replace("-", "_")
    return WORKED_EXAMPLES.get(normalized)

def add_worked_example_section(readme_path: Path, algorithm_name: str) -> bool:
    """Add worked example section to README."""
    try:
        content = readme_path.read_text(encoding="utf-8")
        example = get_worked_example(algorithm_name)
        
        if not example:
            return False
        
        # Check if section already exists
        if "## Worked Example" in content or "## Worked Examples" in content:
            return False
        
        # Find insertion point - after Algorithm Visualization or before Practice Exercises
        insertion_points = [
            (r"(## Algorithm Visualization[^\n]*\n[^\n]*\n)", r"\1\n" + example + "\n\n"),
            (r"(## Practice Exercises)", example + "\n\n\1"),
        ]
        
        for pattern, replacement in insertion_points:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                readme_path.write_text(content, encoding="utf-8")
                return True
        
        # If no insertion point found, add before Practice Exercises
        if "## Practice Exercises" in content:
            content = content.replace(
                "## Practice Exercises",
                example + "\n\n## Practice Exercises"
            )
            readme_path.write_text(content, encoding="utf-8")
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {readme_path}: {e}")
        return False

def main():
    """Add worked examples to algorithms."""
    updated_count = 0
    
    # Top 20 algorithms for worked examples
    top_algorithms = [
        ("semester_1/lecture_02_efficient_sorting/quick_sort", "quick_sort"),
        ("semester_1/lecture_02_efficient_sorting/merge_sort", "merge_sort"),
        ("semester_1/lecture_04_searching/binary_search", "binary_search"),
        ("semester_1/lecture_09_graph_algorithms/bfs", "bfs"),
        ("semester_1/lecture_09_graph_algorithms/dijkstra", "dijkstra"),
    ]
    
    for algo_path, algo_name in top_algorithms:
        readme_path = ROOT / algo_path / "README.md"
        if readme_path.exists():
            if add_worked_example_section(readme_path, algo_name):
                updated_count += 1
                print(f"Added worked example to {algo_name}")
    
    print(f"\nAdded worked examples to {updated_count} algorithms")

if __name__ == "__main__":
    main()

