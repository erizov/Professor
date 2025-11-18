#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Greedy Algorithms - Demonstration.

This lecture covers greedy algorithms including
activity selection, fractional knapsack, and Huffman coding.
"""


def activity_selection(start: list, finish: list) -> list:
    """Activity selection problem using greedy approach."""
    n = len(finish)
    selected = [0]
    j = 0
    for i in range(1, n):
        if start[i] >= finish[j]:
            selected.append(i)
            j = i
    return selected


def main() -> None:
    """Demonstrate greedy algorithms."""
    print("=" * 70)
    print("GREEDY ALGORITHMS")
    print("=" * 70)
    
    start = [1, 3, 0, 5, 8, 5]
    finish = [2, 4, 6, 7, 9, 9]
    result = activity_selection(start, finish)
    print(f"Selected activities: {result}")
    print("=" * 70)


if __name__ == "__main__":
    main()
