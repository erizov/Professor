#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sorting Fundamentals - Demonstration.

This lecture covers fundamental sorting algorithms including
bubble sort, selection sort, and insertion sort.
"""

from typing import List


def bubble_sort(arr: List[int]) -> List[int]:
    """Bubble sort algorithm."""
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def main() -> None:
    """Demonstrate sorting fundamentals."""
    print("=" * 70)
    print("SORTING FUNDAMENTALS")
    print("=" * 70)

    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {data}")

    sorted_data = bubble_sort(data)
    print(f"Sorted array: {sorted_data}")
    print("=" * 70)


if __name__ == "__main__":
    main()
