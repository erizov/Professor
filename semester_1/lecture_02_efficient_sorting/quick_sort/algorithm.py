#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Sort implementation.

Efficient divide-and-conquer sorting algorithm that picks a pivot
element and partitions the array around it.
"""

from typing import List, TypeVar
import random


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
    print("=" * 70)
    print("QUICK SORT DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic sorting
    print("Example 1: Basic Integer Sorting")
    print("-" * 70)
    data1 = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]
    print(f"Original: {data1}")
    result1 = quick_sort(data1.copy())
    print(f"Sorted:   {result1}")
    print()
    
    # Example 2: Already sorted
    print("Example 2: Already Sorted")
    print("-" * 70)
    data2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Original: {data2}")
    result2 = quick_sort(data2.copy())
    print(f"Sorted:   {result2}")
    print("Note: May have worst-case O(n²) performance")
    print()
    
    # Example 3: Randomized pivot
    print("Example 3: Randomized Pivot Selection")
    print("-" * 70)
    data3 = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]
    print(f"Original: {data3}")
    result3 = quick_sort_randomized(data3.copy())
    print(f"Sorted:   {result3}")
    print("Randomization helps avoid worst case")
    print()
    
    # Example 4: Strings
    print("Example 4: Sorting Strings")
    print("-" * 70)
    data4 = ["banana", "apple", "cherry", "date", "elderberry"]
    print(f"Original: {data4}")
    result4 = quick_sort(data4.copy())
    print(f"Sorted:   {result4}")
    print()
    
    # Example 5: Large dataset
    print("Example 5: Large Random Dataset")
    print("-" * 70)
    data5 = [random.randint(1, 1000) for _ in range(20)]
    print(f"Original (20 elements): {data5[:10]}...")
    result5 = quick_sort(data5.copy())
    print(f"Sorted (first 10):      {result5[:10]}...")
    print()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(n log n) average, O(n²) worst")
    print("  Space: O(log n) recursion stack")
    print("  Stable: No")
    print("  In-place: Yes")
    print("\nKey Points:")
    print("  - Very fast in practice")
    print("  - Randomized pivot avoids worst case")
    print("  - Most common general-purpose sort")
    print("=" * 70)


if __name__ == "__main__":
    main()
