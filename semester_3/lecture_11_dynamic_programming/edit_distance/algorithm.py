#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edit Distance (Levenshtein Distance) - Dynamic Programming.

Minimum number of single-character edits required to change one word into another.
This is a duplicate implementation for semester 3.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer

# Import from semester 1 implementation
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "semester_1" / "lecture_11_dynamic_programming" / "edit_distance"))
from algorithm import edit_distance, edit_distance_optimized, edit_operations, similarity


def main() -> None:
    """Demonstration of Edit Distance Algorithm."""
    print("=" * 70)
    print("EDIT DISTANCE (LEVENSHTEIN DISTANCE) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example: Basic edit distance
    test_cases = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("horse", "ros"),
    ]
    
    for s1, s2 in test_cases:
        distance = edit_distance(s1, s2)
        print(f"'{s1}' -> '{s2}': {distance} operations")
    print()
    
    print("=" * 70)
    print("\nComplexity: O(m * n)")
    print("=" * 70)


if __name__ == "__main__":
    main()
