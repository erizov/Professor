#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insertion Sort implementation."""

from typing import List, TypeVar
from framework.logging_utils import get_logger
import logging

logger = get_logger(__name__)

T = TypeVar("T")


def insertion_sort(arr: List[T]) -> List[T]:
    """
    Sort array using insertion sort.

    Args:
        arr: List to be sorted

    Returns:
        Sorted list

    Time: O(n²) worst, O(n) best, Space: O(1)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Move elements greater than key one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


def main():
    """Demonstration."""
    import sys
    from framework.performance_timer import PerformanceTimer

    print("=" * 70)
    print("INSERTION SORT")
    print("=" * 70)

    # Example 1: Basic sorting
    data1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"\nExample 1: Basic Integer Sorting")
    print(f"Original: {data1}")

    with PerformanceTimer() as timer:
        result1 = insertion_sort(data1.copy())
    print(f"Sorted:   {result1}")
    print(f"Time: {timer.elapsed_time:.6f} seconds")

    # Example 2: Already sorted
    data2 = [1, 2, 3, 4, 5]
    print(f"\nExample 2: Already Sorted Array")
    print(f"Original: {data2}")
    result2 = insertion_sort(data2.copy())
    print(f"Sorted:   {result2}")

    # Example 3: Reverse sorted
    data3 = [5, 4, 3, 2, 1]
    print(f"\nExample 3: Reverse Sorted Array")
    print(f"Original: {data3}")
    result3 = insertion_sort(data3.copy())
    print(f"Sorted:   {result3}")

    print(f"\nComplexity: O(n²) worst, O(n) best, O(1) space")


if __name__ == "__main__":
    main()
