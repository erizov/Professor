#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binary Search implementation.

Efficient search algorithm for sorted arrays using divide-and-conquer.
"""

from typing import List, TypeVar, Optional
from framework.logging_utils import get_logger
import logging

logger = get_logger(__name__)


T = TypeVar('T')


def binary_search(arr: List[T], target: T) -> int:
    """
    Search for target in sorted array using binary search.
    
    Args:
        arr: Sorted list to search in
        target: Element to find
        
    Returns:
        Index of target if found, -1 otherwise
        
    Time Complexity: O(log n)
    Space Complexity: O(1)
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def binary_search_recursive(
    arr: List[T],
    target: T,
    left: int = 0,
    right: int = None
) -> int:
    """
    Recursive binary search.
    
    Args:
        arr: Sorted list to search in
        target: Element to find
        left: Left boundary
        right: Right boundary
        
    Returns:
        Index of target if found, -1 otherwise
    """
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = left + (right - left) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)


def binary_search_leftmost(arr: List[T], target: T) -> int:
    """
    Find leftmost occurrence of target.
    
    Args:
        arr: Sorted list (may have duplicates)
        target: Element to find
        
    Returns:
        Index of leftmost occurrence, -1 if not found
    """
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def binary_search_rightmost(arr: List[T], target: T) -> int:
    """
    Find rightmost occurrence of target.
    
    Args:
        arr: Sorted list (may have duplicates)
        target: Element to find
        
    Returns:
        Index of rightmost occurrence, -1 if not found
    """
    left, right = 0, len(arr) - 1
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            result = mid
            left = mid + 1  # Continue searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result


def main() -> None:
    """Demonstration of Binary Search."""
    logger.info("=" * 70)
    logger.info("BINARY SEARCH DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic search
    logger.info("Example 1: Basic Search")
    logger.info("-" * 70)
    data1 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target1 = 7
    logger.info(f"Array:  {data1}")
    logger.info(f"Target: {target1}")
    result1 = binary_search(data1, target1)
    logger.info(f"Found at index: {result1}")
    logger.info()
    
    # Example 2: Not found
    logger.info("Example 2: Element Not Found")
    logger.info("-" * 70)
    target2 = 8
    logger.info(f"Array:  {data1}")
    logger.info(f"Target: {target2}")
    result2 = binary_search(data1, target2)
    logger.info(f"Result: {result2} (not found)")
    logger.info()
    
    # Example 3: Recursive
    logger.info("Example 3: Recursive Binary Search")
    logger.info("-" * 70)
    target3 = 15
    logger.info(f"Array:  {data1}")
    logger.info(f"Target: {target3}")
    result3 = binary_search_recursive(data1, target3)
    logger.info(f"Found at index: {result3}")
    logger.info()
    
    # Example 4: Duplicates - leftmost
    logger.info("Example 4: Find Leftmost Occurrence")
    logger.info("-" * 70)
    data4 = [1, 2, 2, 2, 3, 4, 5, 5, 5, 6]
    target4 = 5
    logger.info(f"Array:  {data4}")
    logger.info(f"Target: {target4}")
    result4 = binary_search_leftmost(data4, target4)
    logger.info(f"Leftmost index: {result4}")
    logger.info()
    
    # Example 5: Duplicates - rightmost
    logger.info("Example 5: Find Rightmost Occurrence")
    logger.info("-" * 70)
    logger.info(f"Array:  {data4}")
    logger.info(f"Target: {target4}")
    result5 = binary_search_rightmost(data4, target4)
    logger.info(f"Rightmost index: {result5}")
    logger.info()
    
    # Example 6: Strings
    logger.info("Example 6: Search in Strings")
    logger.info("-" * 70)
    data6 = ["apple", "banana", "cherry", "date", "elderberry"]
    target6 = "cherry"
    logger.info(f"Array:  {data6}")
    logger.info(f"Target: {target6}")
    result6 = binary_search(data6, target6)
    logger.info(f"Found at index: {result6}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(log n)")
    logger.info("  Space: O(1) iterative, O(log n) recursive")
    logger.info("\nKey Requirements:")
    logger.info("  - Array must be SORTED")
    logger.info("  - Random access required (arrays, not linked lists)")
    logger.info("\nAdvantages:")
    logger.info("  - Very fast for large datasets")
    logger.info("  - Simple and elegant")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()