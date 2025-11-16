#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Sort implementation.

Efficient divide-and-conquer sorting algorithm that picks a pivot
element and partitions the array around it.
"""

from typing import List, TypeVar
import random
from framework.logging_utils import get_logger
import logging

logger = get_logger(__name__)


T = TypeVar('T')


def quick_sort(
    arr: List[T],
    low: int = 0,
    high: int = None
) -> List[T]:
    """
    Sort array using quick sort algorithm.
    
    Args:
        arr: List to be sorted
        low: Starting index
        high: Ending index
        
    Returns:
        Sorted list (modifies in-place and returns)
        
    Time Complexity:
        Best: O(n log n)
        Average: O(n log n)
        Worst: O(n²) - when pivot is always min/max
        
    Space Complexity: O(log n) for recursion stack
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # Partition and get pivot index
        pivot_idx = partition(arr, low, high)
        
        # Recursively sort left and right subarrays
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
    
    return arr


def partition(arr: List[T], low: int, high: int) -> int:
    """
    Partition array around pivot.
    
    Args:
        arr: List to partition
        low: Starting index
        high: Ending index
        
    Returns:
        Final position of pivot
    """
    # Choose rightmost element as pivot
    pivot = arr[high]
    
    # Index of smaller element
    i = low - 1
    
    for j in range(low, high):
        # If current element is smaller than or equal to pivot
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Place pivot in correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_randomized(arr: List[T]) -> List[T]:
    """
    Quick sort with randomized pivot selection.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    def partition_random(arr: List[T], low: int, high: int) -> int:
        # Choose random pivot
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        return partition(arr, low, high)
    
    def sort_helper(arr: List[T], low: int, high: int) -> None:
        if low < high:
            pivot_idx = partition_random(arr, low, high)
            sort_helper(arr, low, pivot_idx - 1)
            sort_helper(arr, pivot_idx + 1, high)
    
    sort_helper(arr, 0, len(arr) - 1)
    return arr


def main() -> None:
    """Demonstration of Quick Sort."""
    logger.info("=" * 70)
    logger.info("QUICK SORT DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic sorting
    logger.info("Example 1: Basic Integer Sorting")
    logger.info("-" * 70)
    data1 = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]
    logger.info(f"Original: {data1}")
    result1 = quick_sort(data1.copy())
    logger.info(f"Sorted:   {result1}")
    logger.info()
    
    # Example 2: Already sorted
    logger.info("Example 2: Already Sorted")
    logger.info("-" * 70)
    data2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    logger.info(f"Original: {data2}")
    result2 = quick_sort(data2.copy())
    logger.info(f"Sorted:   {result2}")
    logger.info("Note: May have worst-case O(n²) performance")
    logger.info()
    
    # Example 3: Randomized pivot
    logger.info("Example 3: Randomized Pivot Selection")
    logger.info("-" * 70)
    data3 = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]
    logger.info(f"Original: {data3}")
    result3 = quick_sort_randomized(data3.copy())
    logger.info(f"Sorted:   {result3}")
    logger.info("Randomization helps avoid worst case")
    logger.info()
    
    # Example 4: Strings
    logger.info("Example 4: Sorting Strings")
    logger.info("-" * 70)
    data4 = ["banana", "apple", "cherry", "date", "elderberry"]
    logger.info(f"Original: {data4}")
    result4 = quick_sort(data4.copy())
    logger.info(f"Sorted:   {result4}")
    logger.info()
    
    # Example 5: Large dataset
    logger.info("Example 5: Large Random Dataset")
    logger.info("-" * 70)
    data5 = [random.randint(1, 1000) for _ in range(20)]
    logger.info(f"Original (20 elements): {data5[:10]}...")
    result5 = quick_sort(data5.copy())
    logger.info(f"Sorted (first 10):      {result5[:10]}...")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(n log n) average, O(n²) worst")
    logger.info("  Space: O(log n) recursion stack")
    logger.info("  Stable: No")
    logger.info("  In-place: Yes")
    logger.info("\nKey Points:")
    logger.info("  - Very fast in practice")
    logger.info("  - Randomized pivot avoids worst case")
    logger.info("  - Most common general-purpose sort")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()