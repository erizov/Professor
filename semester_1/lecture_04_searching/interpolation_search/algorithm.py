#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interpolation Search implementation.

This file contains the implementation of the Interpolation Search algorithm.
"""

from typing import List, Optional, Dict, Set


def interpolation_search(arr: List[int], target: int) -> Optional[int]:
    """Interpolation search algorithm."""
    left, right = 0, len(arr) - 1
    
    while left <= right and arr[left] <= target <= arr[right]:
        if left == right:
            if arr[left] == target:
                return left
            return None
        
        pos = left + ((target - arr[left]) * (right - left)) // (arr[right] - arr[left])
        
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1
    
    return None


def main() -> None:
    """Demonstrate Interpolation Search."""
    print("=" * 70)
    print("INTERPOLATION SEARCH")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Interpolation Search")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
