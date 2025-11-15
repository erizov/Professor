#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Linear Search implementation."""

from typing import List, TypeVar, Optional

T = TypeVar('T')


def linear_search(arr: List[T], target: T) -> Optional[int]:
    """
    Search for target using linear search.
    
    Args:
        arr: List to search in
        target: Element to find
        
    Returns:
        Index if found, None otherwise
        
    Time: O(n), Space: O(1)
    """
    for i, element in enumerate(arr):
        if element == target:
            return i
    return None


def main():
    """Demonstration."""
    print("=" * 70)
    print("LINEAR SEARCH")
    print("=" * 70)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    target = 22
    
    result = linear_search(data, target)
    print(f"Array: {data}")
    print(f"Target: {target}")
    print(f"Found at index: {result}")
    
    print("\nComplexity: O(n) time, O(1) space")


if __name__ == "__main__":
    main()
