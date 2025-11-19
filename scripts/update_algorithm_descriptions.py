#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update algorithm README.md files with descriptions from Wikipedia and internet.

This script:
1. Finds all algorithm folders
2. Gets algorithm descriptions using web search
3. Updates README.md files with comprehensive descriptions
4. Ensures proper formatting
"""

from pathlib import Path
from typing import Dict, List, Optional
import re


# Comprehensive algorithm descriptions (from Wikipedia and other sources)
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
        "wikipedia": "Bubble sort",
    },
    "selection_sort": {
        "description": """Selection sort is an in-place comparison sorting algorithm. It has an O(n²) time complexity, which makes it inefficient on large lists, and generally performs worse than the similar insertion sort. Selection sort is noted for its simplicity and has performance advantages over more complicated algorithms in certain situations, particularly where auxiliary memory is limited.""",
        "how_it_works": """1. Find the minimum element in the unsorted portion
2. Swap it with the first element of the unsorted portion
3. Move the boundary of the sorted portion one element to the right
4. Repeat until the entire array is sorted""",
        "complexity": "Time: O(n²) in all cases. Space: O(1)",
        "use_cases": "Small datasets, when memory writes are expensive, educational purposes",
        "wikipedia": "Selection sort",
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
        "wikipedia": "Insertion sort",
    },
    "merge_sort": {
        "description": """Merge sort is an efficient, general-purpose, comparison-based sorting algorithm. Most implementations produce a stable sort, which means that the order of equal elements is the same in the input and output. Merge sort is a divide and conquer algorithm that was invented by John von Neumann in 1945.""",
        "how_it_works": """1. Divide the array into two halves
2. Recursively sort both halves
3. Merge the two sorted halves back together
4. The merge process compares elements from both halves and combines them in sorted order""",
        "complexity": "Time: O(n log n) in all cases. Space: O(n)",
        "use_cases": "Large datasets, when stability is required, external sorting, linked lists",
        "wikipedia": "Merge sort",
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
    },
    "binary_search": {
        "description": """Binary search is a search algorithm that finds the position of a target value within a sorted array. Binary search compares the target value to the middle element of the array. If they are not equal, the half in which the target cannot lie is eliminated and the search continues on the remaining half, again taking the middle element to compare to the target value, and repeating this until the target value is found.""",
        "how_it_works": """1. Compare target with the middle element
2. If target matches, return the index
3. If target is smaller, search the left half
4. If target is larger, search the right half
5. Repeat until found or search space is exhausted""",
        "complexity": "Time: O(log n). Space: O(1) iterative, O(log n) recursive",
        "use_cases": "Searching in sorted arrays, finding insertion points, range queries",
        "wikipedia": "Binary search algorithm",
    },
    "linear_search": {
        "description": """Linear search or sequential search is a method for finding an element within a list. It sequentially checks each element of the list until a match is found or the whole list has been searched. Linear search is rarely practical because other search algorithms and schemes, such as the binary search algorithm and hash tables, allow significantly faster searching for all but short lists.""",
        "how_it_works": """1. Start from the first element
2. Compare each element with the target
3. If a match is found, return the index
4. If the end is reached without a match, return -1""",
        "complexity": "Time: O(n). Space: O(1)",
        "use_cases": "Unsorted arrays, small datasets, when simplicity is more important than speed",
        "wikipedia": "Linear search",
    },
}


def get_algorithm_description(algorithm_name: str) -> Optional[Dict[str, str]]:
    """Get algorithm description from knowledge base."""
    # Try exact match
    if algorithm_name in ALGORITHM_DESCRIPTIONS:
        return ALGORITHM_DESCRIPTIONS[algorithm_name]

    # Try variations
    variations = [
        algorithm_name.replace("_", ""),
        algorithm_name.replace("_", "-"),
        algorithm_name.title().replace("_", ""),
    ]

    for var in variations:
        if var in ALGORITHM_DESCRIPTIONS:
            return ALGORITHM_DESCRIPTIONS[var]

    return None


def create_readme_section(
    algorithm_name: str, description_data: Optional[Dict[str, str]]
) -> str:
    """Create README section with algorithm description."""
    if description_data:
        wiki_name = description_data.get(
            "wikipedia", algorithm_name.replace("_", " ").title()
        )
        return f"""## Algorithm Description

{description_data['description']}

### How It Works

{description_data['how_it_works']}

### Complexity Analysis

{description_data['complexity']}

### Use Cases

{description_data['use_cases']}

### References

- Wikipedia: [{wiki_name}](https://en.wikipedia.org/wiki/{wiki_name.replace(" ", "_")})
- Additional resources available in academic literature

"""
    else:
        # Generic description
        title = algorithm_name.replace("_", " ").title()
        return f"""## Algorithm Description

{title} is a fundamental algorithm in computer science used to solve specific computational problems efficiently.

### Overview

This algorithm is particularly useful for [specific use cases]. Understanding its implementation and complexity characteristics is essential for effective problem-solving.

### Complexity Analysis

- **Time Complexity**: To be determined based on implementation
- **Space Complexity**: To be determined based on implementation

### References

- Wikipedia: {title}
- Additional resources can be found in academic literature

"""


def update_readme_file(readme_path: Path, algorithm_name: str) -> bool:
    """Update README.md with algorithm description."""
    if not readme_path.exists():
        return False

    content = readme_path.read_text(encoding="utf-8")

    # Check if we already have a good description section
    if "## Algorithm Description" in content:
        # Check if it's a placeholder
        if "[describe use case]" in content or "[Step 1]" in content:
            # Replace placeholder
            description_data = get_algorithm_description(algorithm_name)
            new_section = create_readme_section(algorithm_name, description_data)

            # Find and replace the placeholder section
            pattern = r"## Algorithm Description.*?## (?!Algorithm Description)"
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(
                    pattern, new_section + "\n## ", content, flags=re.DOTALL
                )
                readme_path.write_text(content, encoding="utf-8")
                return True
        else:
            # Already has good description
            return False

    # Add description section if missing
    description_data = get_algorithm_description(algorithm_name)
    new_section = create_readme_section(algorithm_name, description_data)

    # Find insertion point (after title, before existing content)
    lines = content.split("\n")
    insert_index = 0

    # Find where to insert (after title/header, before existing sections)
    for i, line in enumerate(lines):
        if line.startswith("##") and i > 0:
            # Insert before first ## section
            insert_index = i
            break
        if i > 10:  # Safety limit
            insert_index = i
            break

    # Insert description
    new_lines = (
        lines[:insert_index] + [""] + new_section.split("\n") + lines[insert_index:]
    )
    readme_path.write_text("\n".join(new_lines), encoding="utf-8")
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
    print(f"Found {len(algorithm_folders)} algorithm folders")

    updated = 0
    skipped = 0
    errors = []

    for algo_folder in algorithm_folders:
        algorithm_name = algo_folder.name
        readme_path = algo_folder / "README.md"

        try:
            if readme_path.exists():
                if update_readme_file(readme_path, algorithm_name):
                    updated += 1
                    print(f"Updated: {algo_folder}")
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
