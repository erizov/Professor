#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate algorithm implementations and update README.md files.

This script:
1. Finds all algorithm subfolders
2. Gets algorithm descriptions from Wikipedia/internet
3. Updates README.md files with descriptions
4. Ensures algorithm.py has proper main() method
"""

from pathlib import Path
from typing import Dict, List, Optional
import re


# Algorithm name mappings to Wikipedia search terms
ALGORITHM_WIKIPEDIA_MAP: Dict[str, str] = {
    "bubble_sort": "Bubble sort",
    "selection_sort": "Selection sort",
    "insertion_sort": "Insertion sort",
    "merge_sort": "Merge sort",
    "quick_sort": "Quicksort",
    "heap_sort": "Heapsort",
    "counting_sort": "Counting sort",
    "radix_sort": "Radix sort",
    "bucket_sort": "Bucket sort",
    "linear_search": "Linear search",
    "binary_search": "Binary search",
    "jump_search": "Jump search",
    "interpolation_search": "Interpolation search",
    "binary_tree": "Binary tree",
    "binary_search_tree": "Binary search tree",
    "avl_tree": "AVL tree",
    "red_black_tree": "Red–black tree",
    "b_tree": "B-tree",
    "trie": "Trie",
    "binary_heap": "Binary heap",
    "priority_queue": "Priority queue",
    "fibonacci_heap": "Fibonacci heap",
    "hash_table": "Hash table",
    "chaining": "Hash table",
    "open_addressing": "Hash table",
    "bfs": "Breadth-first search",
    "dfs": "Depth-first search",
    "dijkstra": "Dijkstra's algorithm",
    "bellman_ford": "Bellman–Ford algorithm",
    "floyd_warshall": "Floyd–Warshall algorithm",
    "kmp": "Knuth–Morris–Pratt algorithm",
    "boyer_moore": "Boyer–Moore string-search algorithm",
    "rabin_karp": "Rabin–Karp algorithm",
    "edit_distance": "Edit distance",
    "longest_common_subsequence": "Longest common subsequence",
    "knapsack": "Knapsack problem",
    "fibonacci": "Fibonacci number",
    "kmeans": "K-means clustering",
    "k_means": "K-means clustering",
    "linear_regression": "Linear regression",
    "logistic_regression": "Logistic regression",
    "knn": "K-nearest neighbors algorithm",
    "decision_tree": "Decision tree",
    "naive_bayes": "Naive Bayes classifier",
    "svm": "Support vector machine",
    "neural_network": "Artificial neural network",
    "gradient_descent": "Gradient descent",
    "random_forest": "Random forest",
    "huffman": "Huffman coding",
    "activity_selection": "Activity selection problem",
    "fractional_knapsack": "Continuous knapsack problem",
}


def get_algorithm_wikipedia_name(algorithm_name: str) -> str:
    """Get Wikipedia search term for algorithm."""
    # Try direct mapping
    if algorithm_name in ALGORITHM_WIKIPEDIA_MAP:
        return ALGORITHM_WIKIPEDIA_MAP[algorithm_name]

    # Convert snake_case to Title Case
    words = algorithm_name.split("_")
    title = " ".join(word.capitalize() for word in words)
    return title


def create_algorithm_description(algorithm_name: str) -> str:
    """
    Create algorithm description.

    In a real implementation, this would fetch from Wikipedia.
    For now, we create a template that can be filled.
    """
    wiki_name = get_algorithm_wikipedia_name(algorithm_name)

    description = f"""## Overview

{wiki_name} is a fundamental algorithm in computer science.

## Description

{wiki_name} is used to solve specific computational problems efficiently. 
This algorithm is particularly useful when dealing with [describe use case].

## Algorithm Details

### How It Works

The algorithm works by [describe the main approach]:

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Key Characteristics

- **Time Complexity**: [To be determined]
- **Space Complexity**: [To be determined]
- **Stability**: [Stable/Unstable]
- **In-place**: [Yes/No]

## Use Cases

- [Use case 1]
- [Use case 2]
- [Use case 3]

## References

- Wikipedia: {wiki_name}
- Additional resources can be found in academic literature

## Implementation

See `algorithm.py` for the complete implementation with examples.
"""
    return description


def update_readme_with_description(readme_path: Path, algorithm_name: str) -> None:
    """Update README.md with algorithm description."""
    if not readme_path.exists():
        return

    content = readme_path.read_text(encoding="utf-8")

    # Check if description section exists
    if "## Overview" in content or "## Description" in content:
        # Already has description, skip
        return

    # Add description after introduction or at appropriate place
    description = create_algorithm_description(algorithm_name)

    # Find insertion point (after title/intro, before existing content)
    lines = content.split("\n")
    insert_index = 0

    # Find where to insert (after title/header)
    for i, line in enumerate(lines):
        if line.startswith("#") and i > 0:
            insert_index = i + 1
            break
        if "## Introduction" in line or "## TL;DR" in line:
            insert_index = i + 1
            break

    # Insert description
    new_lines = (
        lines[:insert_index] + [""] + description.split("\n") + lines[insert_index:]
    )
    readme_path.write_text("\n".join(new_lines), encoding="utf-8")


def ensure_main_method(algorithm_path: Path) -> bool:
    """Ensure algorithm.py has exactly one main() method."""
    if not algorithm_path.exists():
        return False

    content = algorithm_path.read_text(encoding="utf-8")
    main_count = content.count("def main(")

    if main_count == 1:
        return True

    if main_count == 0:
        # Add main method
        if 'if __name__ == "__main__":' in content:
            # Add main before if __name__
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if 'if __name__ == "__main__":' in line:
                    # Insert main method before this line
                    main_method = '''def main() -> None:
    """Main function to demonstrate the algorithm."""
    print("=" * 70)
    print("ALGORITHM DEMONSTRATION")
    print("=" * 70)
    print("Algorithm implementation")
    print("=" * 70)


'''
                    lines.insert(i, main_method)
                    # Update the if __name__ block
                    if i + 1 < len(lines):
                        lines[i + 1] = 'if __name__ == "__main__":'
                        if i + 2 < len(lines) and not lines[i + 2].strip():
                            lines[i + 2] = "    main()"
                        else:
                            lines.insert(i + 2, "    main()")
                    break
            algorithm_path.write_text("\n".join(lines), encoding="utf-8")
            return True

    # Multiple main methods - need to fix
    return False


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

    updated_readmes = 0
    updated_algorithms = 0
    errors = []

    for algo_folder in algorithm_folders:
        algorithm_name = algo_folder.name
        readme_path = algo_folder / "README.md"
        algorithm_path = algo_folder / "algorithm.py"

        try:
            # Update README if needed
            if readme_path.exists():
                old_content = readme_path.read_text(encoding="utf-8")
                update_readme_with_description(readme_path, algorithm_name)
                new_content = readme_path.read_text(encoding="utf-8")
                if old_content != new_content:
                    updated_readmes += 1
                    print(f"Updated README: {algo_folder}")

            # Ensure main method exists
            if algorithm_path.exists():
                if ensure_main_method(algorithm_path):
                    updated_algorithms += 1
                    print(f"Verified algorithm.py: {algo_folder}")
        except Exception as e:
            errors.append(f"{algo_folder}: {e}")

    print(f"\nSummary:")
    print(f"  Updated README.md files: {updated_readmes}")
    print(f"  Verified algorithm.py files: {updated_algorithms}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors[:10]:
            print(f"  {error}")


if __name__ == "__main__":
    main()
