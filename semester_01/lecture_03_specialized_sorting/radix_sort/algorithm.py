#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Radix Sort implementation.

This file contains the implementation of the Radix Sort algorithm.
"""

from typing import List, Optional, Dict, Set


def radix_sort(arr: List[int]) -> List[int]:
    """Radix sort algorithm."""
    def counting_sort_radix(arr: List[int], exp: int) -> List[int]:
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        
        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1
        
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        i = n - 1
        while i >= 0:
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1
        
        return output
    
    if not arr:
        return arr
    
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        arr = counting_sort_radix(arr, exp)
        exp *= 10
    
    return arr


def main() -> None:
    """Demonstrate Radix Sort."""
    print("=" * 70)
    print("RADIX SORT")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Radix Sort")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
