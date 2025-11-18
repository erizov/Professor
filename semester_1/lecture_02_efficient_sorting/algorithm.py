#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Efficient Sorting - Demonstration.

This lecture covers efficient sorting algorithms including
merge sort, quick sort, and heap sort.
"""

from typing import List


def quick_sort(arr: List[int]) -> List[int]:
    """Quick sort algorithm."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def main() -> None:
    """Demonstrate efficient sorting."""
    print("=" * 70)
    print("EFFICIENT SORTING")
    print("=" * 70)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {data}")
    
    sorted_data = quick_sort(data)
    print(f"Sorted array: {sorted_data}")
    print("=" * 70)


if __name__ == "__main__":
    main()
