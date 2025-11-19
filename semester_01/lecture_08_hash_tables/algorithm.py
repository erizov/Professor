#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Searching Algorithms - Demonstration.

This lecture covers various searching algorithms including
linear search, binary search, and interpolation search.
"""

from typing import List, Optional


def binary_search(arr: List[int], target: int) -> Optional[int]:
    """Binary search algorithm."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None


def main() -> None:
    """Demonstrate searching algorithms."""
    print("=" * 70)
    print("SEARCHING ALGORITHMS")
    print("=" * 70)

    data = [11, 12, 22, 25, 34, 64, 90]
    target = 25
    print(f"Array: {data}")
    print(f"Searching for: {target}")

    result = binary_search(data, target)
    if result is not None:
        print(f"Found at index: {result}")
    else:
        print("Not found")
    print("=" * 70)


if __name__ == "__main__":
    main()
