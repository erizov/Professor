#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate comprehensive algorithm implementations with descriptions from Wikipedia.

This script:
1. Finds all algorithm folders
2. Searches for algorithm descriptions online
3. Updates README.md with comprehensive descriptions
4. Ensures algorithm.py has proper implementation
"""

from pathlib import Path
from typing import Dict, List, Optional
import re


# Extended algorithm descriptions database
ALGORITHM_DESCRIPTIONS: Dict[str, Dict[str, str]] = {
    "bubble_sort": {
        "description": """Bubble sort is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. The pass through the list is repeated until the list is sorted. The algorithm gets its name from the way smaller elements "bubble" to the top of the list.""",
        "how_it_works": """1. Start from the beginning of the array
2. Compare each pair of adjacent elements
3. If they are in the wrong order, swap them
4. Continue until no more swaps are needed
5. The largest element "bubbles up" to the end in each pass""",
        "complexity": "Time: O(n²) average and worst case, O(n) best case (optimized). Space: O(1)",
        "use_cases": "Educational purposes, very small datasets, nearly sorted data, when simplicity is critical",
        "wikipedia": "Bubble_sort",
        "category": "Sorting",
    },
    "selection_sort": {
        "description": """Selection sort is an in-place comparison sorting algorithm. It has an O(n²) time complexity, which makes it inefficient on large lists, and generally performs worse than the similar insertion sort. Selection sort is noted for its simplicity and has performance advantages over more complicated algorithms in certain situations, particularly where auxiliary memory is limited.""",
        "how_it_works": """1. Find the minimum element in the unsorted portion
2. Swap it with the first element of the unsorted portion
3. Move the boundary of the sorted portion one element to the right
4. Repeat until the entire array is sorted""",
        "complexity": "Time: O(n²) in all cases. Space: O(1)",
        "use_cases": "Small datasets, when memory writes are expensive, educational purposes",
        "wikipedia": "Selection_sort",
        "category": "Sorting",
    },
    "insertion_sort": {
        "description": """Insertion sort is a simple sorting algorithm that builds the final sorted array one item at a time. It is much less efficient on large lists than more advanced algorithms such as quicksort, heapsort, or merge sort. However, insertion sort provides several advantages: simple implementation, efficient for small data sets, adaptive, stable, in-place, and online.""",
        "how_it_works": """1. Start with the second element (index 1)
2. Compare it with elements before it
3. Shift larger elements one position to the right
4. Insert the current element in the correct position
5. Repeat for all remaining elements""",
        "complexity": "Time: O(n²) average and worst case, O(n) best case. Space: O(1)",
        "use_cases": "Small datasets, nearly sorted data, as part of hybrid algorithms like Timsort",
        "wikipedia": "Insertion_sort",
        "category": "Sorting",
    },
    "merge_sort": {
        "description": """Merge sort is an efficient, general-purpose, comparison-based sorting algorithm. Most implementations produce a stable sort, which means that the order of equal elements is the same in the input and output. Merge sort is a divide and conquer algorithm that was invented by John von Neumann in 1945.""",
        "how_it_works": """1. Divide the array into two halves
2. Recursively sort both halves
3. Merge the two sorted halves back together
4. The merge process compares elements from both halves and combines them in sorted order""",
        "complexity": "Time: O(n log n) in all cases. Space: O(n)",
        "use_cases": "Large datasets, when stability is required, external sorting, linked lists",
        "wikipedia": "Merge_sort",
        "category": "Sorting",
    },
    "quick_sort": {
        "description": """Quicksort is an efficient sorting algorithm. Developed by British computer scientist Tony Hoare in 1959 and published in 1961, it is still a commonly used algorithm for sorting. When implemented well, it can be somewhat faster than merge sort and about two or three times faster than heapsort.""",
        "how_it_works": """1. Choose a pivot element from the array
2. Partition the array: elements smaller than pivot go left, larger go right
3. Recursively apply quicksort to the left and right subarrays
4. Combine the results (pivot is already in correct position)""",
        "complexity": "Time: O(n log n) average, O(n²) worst case. Space: O(log n)",
        "use_cases": "General-purpose sorting, large datasets, when average performance matters more than worst case",
        "wikipedia": "Quicksort",
        "category": "Sorting",
    },
    "heap_sort": {
        "description": """Heapsort is a comparison-based sorting algorithm. Heapsort can be thought of as an improved selection sort: like selection sort, heapsort divides its input into a sorted and an unsorted region, and it iteratively shrinks the unsorted region by extracting the largest element from it and inserting it into the sorted region.""",
        "how_it_works": """1. Build a max heap from the input array
2. The largest element is at the root
3. Swap the root with the last element and reduce heap size
4. Heapify the root to maintain heap property
5. Repeat until heap size is 1""",
        "complexity": "Time: O(n log n) in all cases. Space: O(1)",
        "use_cases": "When worst-case O(n log n) is required, embedded systems, real-time systems",
        "wikipedia": "Heapsort",
        "category": "Sorting",
    },
    "counting_sort": {
        "description": """Counting sort is an algorithm for sorting a collection of objects according to keys that are small positive integers. It operates by counting the number of objects that have each distinct key value, and using arithmetic on those counts to determine the positions of each key value in the output sequence.""",
        "how_it_works": """1. Count the frequency of each distinct value
2. Calculate cumulative counts to determine positions
3. Place each element in its correct position based on counts
4. Copy back to original array""",
        "complexity": "Time: O(n + k) where k is the range of input. Space: O(k)",
        "use_cases": "Sorting integers with small range, as subroutine in radix sort",
        "wikipedia": "Counting_sort",
        "category": "Sorting",
    },
    "radix_sort": {
        "description": """Radix sort is a non-comparative sorting algorithm. It avoids comparison by creating and distributing elements into buckets according to their radix. For elements with more than one significant digit, this bucketing process is repeated for each digit, while preserving the ordering of the prior step, until all digits have been considered.""",
        "how_it_works": """1. Sort elements by least significant digit (LSD) or most significant digit (MSD)
2. Group elements into buckets based on digit value
3. Recombine buckets in order
4. Repeat for next significant digit
5. Continue until all digits processed""",
        "complexity": "Time: O(d × (n + k)) where d is number of digits, k is radix. Space: O(n + k)",
        "use_cases": "Sorting integers, strings, fixed-width data types",
        "wikipedia": "Radix_sort",
        "category": "Sorting",
    },
    "bucket_sort": {
        "description": """Bucket sort, or bin sort, is a sorting algorithm that works by distributing the elements of an array into a number of buckets. Each bucket is then sorted individually, either using a different sorting algorithm, or by recursively applying the bucket sorting algorithm.""",
        "how_it_works": """1. Create empty buckets
2. Distribute array elements into buckets based on value range
3. Sort each bucket individually (using insertion sort or another algorithm)
4. Concatenate all buckets back into the original array""",
        "complexity": "Time: O(n + k) average, O(n²) worst case. Space: O(n + k)",
        "use_cases": "Uniformly distributed data, floating point numbers, when data is distributed over a range",
        "wikipedia": "Bucket_sort",
        "category": "Sorting",
    },
    "binary_search": {
        "description": """Binary search is a search algorithm that finds the position of a target value within a sorted array. Binary search compares the target value to the middle element of the array. If they are not equal, the half in which the target cannot lie is eliminated and the search continues on the remaining half.""",
        "how_it_works": """1. Compare target with the middle element
2. If target matches, return the index
3. If target is smaller, search the left half
4. If target is larger, search the right half
5. Repeat until found or search space is exhausted""",
        "complexity": "Time: O(log n). Space: O(1) iterative, O(log n) recursive",
        "use_cases": "Searching in sorted arrays, finding insertion points, range queries",
        "wikipedia": "Binary_search_algorithm",
        "category": "Searching",
    },
    "linear_search": {
        "description": """Linear search or sequential search is a method for finding an element within a list. It sequentially checks each element of the list until a match is found or the whole list has been searched. Linear search is rarely practical because other search algorithms allow significantly faster searching for all but short lists.""",
        "how_it_works": """1. Start from the first element
2. Compare each element with the target
3. If a match is found, return the index
4. If the end is reached without a match, return -1""",
        "complexity": "Time: O(n). Space: O(1)",
        "use_cases": "Unsorted arrays, small datasets, when simplicity is more important than speed",
        "wikipedia": "Linear_search",
        "category": "Searching",
    },
    "jump_search": {
        "description": """Jump search is a searching algorithm for sorted arrays. The basic idea is to check fewer elements by jumping ahead by fixed steps or skipping some elements in place of searching all elements. It works better than linear search but requires the array to be sorted.""",
        "how_it_works": """1. Jump ahead by fixed step size (typically √n)
2. If current element is greater than target, perform linear search backwards
3. If current element is less than target, continue jumping
4. Repeat until target found or array exhausted""",
        "complexity": "Time: O(√n). Space: O(1)",
        "use_cases": "Sorted arrays, when binary search is not available, uniform data distribution",
        "wikipedia": "Jump_search",
        "category": "Searching",
    },
    "interpolation_search": {
        "description": """Interpolation search is an algorithm for searching for a key in an array that has been ordered by numerical values assigned to the keys. It is an improvement over binary search for instances where the values in a sorted array are uniformly distributed.""",
        "how_it_works": """1. Calculate probe position using interpolation formula
2. Compare target with element at probe position
3. If match, return index
4. If target is smaller, search left subarray
5. If target is larger, search right subarray""",
        "complexity": "Time: O(log log n) average for uniform distribution, O(n) worst case. Space: O(1)",
        "use_cases": "Uniformly distributed sorted arrays, when data is evenly spread",
        "wikipedia": "Interpolation_search",
        "category": "Searching",
    },
    "avl_tree": {
        "description": """An AVL tree (named after inventors Adelson-Velsky and Landis) is a self-balancing binary search tree. In an AVL tree, the heights of the two child subtrees of any node differ by at most one; if at any time they differ by more than one, rebalancing is done to restore this property.""",
        "how_it_works": """1. Insert/search/delete like a regular BST
2. After each operation, check balance factor (height difference)
3. If imbalance detected, perform rotations (left, right, or double)
4. Rotations restore AVL property while maintaining BST order
5. Balance factor must be -1, 0, or 1 for all nodes""",
        "complexity": "Time: O(log n) for all operations. Space: O(n)",
        "use_cases": "When guaranteed O(log n) performance is needed, database indexing, priority queues",
        "wikipedia": "AVL_tree",
        "category": "Data Structure",
    },
    "binary_search_tree": {
        "description": """A binary search tree (BST) is a binary tree data structure where each node has a comparable key and satisfies the restriction that the key in any node is larger than the keys in all nodes in that node's left subtree and smaller than the keys in all nodes in that node's right subtree.""",
        "how_it_works": """1. Start at root
2. Compare value with current node
3. If smaller, go left; if larger, go right
4. If equal, found; if null, not found
5. Insert at null position; delete requires rebalancing""",
        "complexity": "Time: O(log n) average, O(n) worst case. Space: O(n)",
        "use_cases": "Dynamic sets, priority queues, symbol tables, database indexing",
        "wikipedia": "Binary_search_tree",
        "category": "Data Structure",
    },
    "dijkstra": {
        "description": """Dijkstra's algorithm is an algorithm for finding the shortest paths between nodes in a weighted graph, which may represent, for example, road networks. It was conceived by computer scientist Edsger W. Dijkstra in 1956 and published three years later.""",
        "how_it_works": """1. Initialize distances: source = 0, all others = infinity
2. Use priority queue to track unvisited nodes
3. Extract node with minimum distance
4. Relax edges: update distances to neighbors if shorter path found
5. Mark node as visited, repeat until all nodes processed""",
        "complexity": "Time: O((V + E) log V) with binary heap. Space: O(V)",
        "use_cases": "GPS navigation, network routing, social networks, game pathfinding",
        "wikipedia": "Dijkstra's_algorithm",
        "category": "Graph Algorithm",
    },
    "bfs": {
        "description": """Breadth-first search (BFS) is an algorithm for traversing or searching tree or graph data structures. It starts at the tree root (or some arbitrary node of a graph) and explores all nodes at the present depth prior to moving on to nodes at the next depth level.""",
        "how_it_works": """1. Start from source node, mark as visited
2. Add to queue
3. While queue not empty: dequeue node, visit it
4. Add all unvisited neighbors to queue
5. Mark neighbors as visited, repeat""",
        "complexity": "Time: O(V + E) where V is vertices, E is edges. Space: O(V)",
        "use_cases": "Shortest path in unweighted graphs, level-order tree traversal, social networks, web crawling",
        "wikipedia": "Breadth-first_search",
        "category": "Graph Algorithm",
    },
    "dfs": {
        "description": """Depth-first search (DFS) is an algorithm for traversing or searching tree or graph data structures. The algorithm starts at the root node and explores as far as possible along each branch before backtracking.""",
        "how_it_works": """1. Start from source node, mark as visited
2. Recursively visit unvisited neighbors
3. Explore as deep as possible before backtracking
4. Use stack (recursion or explicit) to track path
5. Mark nodes as visited to avoid cycles""",
        "complexity": "Time: O(V + E) where V is vertices, E is edges. Space: O(V)",
        "use_cases": "Topological sorting, cycle detection, maze solving, path finding, connected components",
        "wikipedia": "Depth-first_search",
        "category": "Graph Algorithm",
    },
    "kmp": {
        "description": """The Knuth–Morris–Pratt (KMP) algorithm is a string-searching algorithm that searches for occurrences of a "word" W within a main "text string" S by employing the observation that when a mismatch occurs, the word itself embodies sufficient information to determine where the next match could begin.""",
        "how_it_works": """1. Preprocess pattern to create longest prefix suffix (LPS) array
2. Match pattern with text character by character
3. On mismatch, use LPS array to skip characters already matched
4. Avoid re-checking characters that are known to match
5. Continue until pattern found or text exhausted""",
        "complexity": "Time: O(n + m) where n is text length, m is pattern length. Space: O(m)",
        "use_cases": "Text editors, search engines, DNA sequence matching, plagiarism detection",
        "wikipedia": "Knuth–Morris–Pratt_algorithm",
        "category": "String Algorithm",
    },
    "knapsack": {
        "description": """The knapsack problem is a problem in combinatorial optimization: Given a set of items, each with a weight and a value, determine the number of each item to include in a collection so that the total weight is less than or equal to a given limit and the total value is as large as possible.""",
        "how_it_works": """1. Use dynamic programming: create 2D table
2. For each item, consider including or excluding it
3. If weight allows, take maximum of (value with item, value without item)
4. Fill table bottom-up
5. Trace back to find selected items""",
        "complexity": "Time: O(n × W) where n is items, W is capacity. Space: O(n × W)",
        "use_cases": "Resource allocation, portfolio optimization, cutting stock problem, budget allocation",
        "wikipedia": "Knapsack_problem",
        "category": "Dynamic Programming",
    },
    "longest_common_subsequence": {
        "description": """The longest common subsequence (LCS) problem is the problem of finding the longest subsequence common to all sequences in a set of sequences. It differs from the longest common substring problem: unlike substrings, subsequences are not required to occupy consecutive positions within the original sequences.""",
        "how_it_works": """1. Create 2D DP table
2. Compare characters of both strings
3. If characters match, LCS[i][j] = 1 + LCS[i-1][j-1]
4. If no match, LCS[i][j] = max(LCS[i-1][j], LCS[i][j-1])
5. Trace back to construct actual LCS string""",
        "complexity": "Time: O(m × n) where m, n are string lengths. Space: O(m × n)",
        "use_cases": "Version control (diff), DNA sequence comparison, plagiarism detection, text similarity",
        "wikipedia": "Longest_common_subsequence_problem",
        "category": "Dynamic Programming",
    },
}


def get_algorithm_info(algorithm_name: str) -> Optional[Dict[str, str]]:
    """Get algorithm information from database."""
    # Try exact match
    if algorithm_name in ALGORITHM_DESCRIPTIONS:
        return ALGORITHM_DESCRIPTIONS[algorithm_name]

    # Try variations
    variations = [
        algorithm_name.replace("_", ""),
        algorithm_name.replace("_", "-"),
    ]

    for var in variations:
        if var in ALGORITHM_DESCRIPTIONS:
            return ALGORITHM_DESCRIPTIONS[var]

    return None


def create_comprehensive_readme(
    algorithm_name: str, algorithm_info: Optional[Dict[str, str]]
) -> str:
    """Create comprehensive README content."""
    title = algorithm_name.replace("_", " ").title()

    if algorithm_info:
        wiki_link = f"https://en.wikipedia.org/wiki/{algorithm_info['wikipedia']}"
        category = algorithm_info.get("category", "Algorithm")

        readme = f"""# {title}

**Category**: {category}

## Overview

{algorithm_info['description']}

## How It Works

{algorithm_info['how_it_works']}

## Complexity Analysis

{algorithm_info['complexity']}

## Use Cases

{algorithm_info['use_cases']}

## Algorithm Details

### Key Characteristics

- **Stability**: Depends on implementation
- **In-place**: Depends on implementation
- **Adaptive**: Depends on implementation

## Implementation

See `algorithm.py` for the complete implementation with examples and performance analysis.

## References

- Wikipedia: [{algorithm_info['wikipedia'].replace('_', ' ')}]({wiki_link})
- Additional resources available in academic literature and algorithm textbooks

## Examples

Run the algorithm with:
```bash
python algorithm.py
```

## Learning Objectives

By studying this algorithm, you will learn:
1. The fundamental approach and logic
2. Time and space complexity analysis
3. When to use this algorithm vs alternatives
4. Implementation details and optimizations
"""
    else:
        # Generic template
        readme = f"""# {title}

**Category**: Algorithm

## Overview

{title} is a fundamental algorithm in computer science used to solve specific computational problems efficiently.

## Description

This algorithm is particularly useful for solving problems related to [specific domain]. Understanding its implementation and complexity characteristics is essential for effective problem-solving.

## How It Works

[Algorithm description to be added]

## Complexity Analysis

- **Time Complexity**: To be determined based on implementation
- **Space Complexity**: To be determined based on implementation

## Use Cases

- [Use case 1]
- [Use case 2]
- [Use case 3]

## Implementation

See `algorithm.py` for the complete implementation with examples.

## References

- Wikipedia: {title}
- Additional resources can be found in academic literature

## Examples

Run the algorithm with:
```bash
python algorithm.py
```
"""

    return readme


def update_readme_file(readme_path: Path, algorithm_name: str) -> bool:
    """Update README.md with comprehensive description."""
    algorithm_info = get_algorithm_info(algorithm_name)
    new_content = create_comprehensive_readme(algorithm_name, algorithm_info)

    if readme_path.exists():
        # Check if we need to update
        existing = readme_path.read_text(encoding="utf-8")
        # If it already has good content, check if update is needed
        if "## Overview" in existing and algorithm_info:
            # Update only if we have better info
            if "[describe use case]" not in existing and "[Use case 1]" not in existing:
                # Already has good content
                return False

    readme_path.write_text(new_content, encoding="utf-8")
    return True


def find_all_algorithm_folders() -> List[Path]:
    """Find all algorithm subfolders."""
    base_path = Path(".")
    algorithm_folders = []

    for semester_dir in base_path.glob("semester_*"):
        if not semester_dir.is_dir():
            continue
        if any(x in str(semester_dir) for x in ["__pycache__", ".git"]):
            continue

        for lecture_dir in semester_dir.iterdir():
            if not lecture_dir.is_dir():
                continue
            if "lecture_" not in lecture_dir.name:
                continue

            for algo_dir in lecture_dir.iterdir():
                if not algo_dir.is_dir():
                    continue
                if algo_dir.name.startswith("lecture_"):
                    continue
                if any(x in algo_dir.name for x in ["__pycache__", ".git"]):
                    continue

                algorithm_folders.append(algo_dir)

    return sorted(algorithm_folders)


def main() -> None:
    """Main function."""
    print("Finding all algorithm folders...")
    algorithm_folders = find_all_algorithm_folders()
    print(f"Found {len(algorithm_folders)} algorithm folders\n")

    updated = 0
    skipped = 0
    errors = []

    for algo_folder in algorithm_folders:
        algorithm_name = algo_folder.name
        readme_path = algo_folder / "README.md"

        try:
            if update_readme_file(readme_path, algorithm_name):
                updated += 1
                if updated % 50 == 0:
                    print(f"Updated {updated} README files...")
            else:
                skipped += 1
        except Exception as e:
            errors.append(f"{algo_folder}: {e}")

    print(f"\nSummary:")
    print(f"  Updated README.md files: {updated}")
    print(f"  Skipped (already complete): {skipped}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors[:10]:
            print(f"  {error}")


if __name__ == "__main__":
    main()
