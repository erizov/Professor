#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Counting Sort implementation.

This file contains the implementation of the Counting Sort algorithm.
"""

from typing import List, Optional, Dict, Set


def counting_sort(arr: List[int]) -> List[int]:
    """Counting sort algorithm."""
    if not arr:
        return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1
    
    count = [0] * range_val
    output = [0] * len(arr)
    
    for num in arr:
        count[num - min_val] += 1
    
    for i in range(1, range_val):
        count[i] += count[i - 1]
    
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
    
    return output


def main() -> None:
    """Demonstrate Counting Sort."""
    print("=" * 70)
    print("COUNTING SORT")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Counting Sort")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
