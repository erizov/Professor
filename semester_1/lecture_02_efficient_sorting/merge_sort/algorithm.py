#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge Sort implementation.

Efficient divide-and-conquer sorting algorithm with guaranteed
O(n log n) performance.
"""

import sys
from pathlib import Path
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


def merge_sort(arr: list) -> list:
    """
    Sort array using merge sort algorithm.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
        
    Time Complexity: O(n log n) in all cases
    Space Complexity: O(n) auxiliary space
    """
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Conquer
    return merge(left, right)


def merge(left: list, right: list) -> list:
    """
    Merge two sorted arrays into one sorted array.
    
    Args:
        left: First sorted array
        right: Second sorted array
        
    Returns:
        Merged sorted array
    """
    result = []
    i = j = 0
    
    # Merge elements in sorted order
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Append remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def merge_sort_inplace(arr: list, left: int, right: int) -> None:
    """
    In-place merge sort (uses less memory for recursion).
    
    Args:
        arr: List to be sorted
        left: Left index
        right: Right index
    """
    if left < right:
        mid = (left + right) // 2
        
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid + 1, right)
        merge_inplace(arr, left, mid, right)


def merge_inplace(arr: list, left: int, mid: int, right: int) -> None:
    """Merge two sorted subarrays in-place."""
    # Create temporary arrays
    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1


def main() -> None:
    """Demonstration of Merge Sort."""
    print("=" * 70)
    print("MERGE SORT DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic sorting
    print("Example 1: Basic Integer Sorting")
    print("-" * 70)
    data1 = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50]
    print(f"Original: {data1}")
    result1 = merge_sort(data1.copy())
    print(f"Sorted:   {result1}")
    print()
    
    # Example 2: Already sorted (best case)
    print("Example 2: Already Sorted Data")
    print("-" * 70)
    data2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Original: {data2}")
    result2 = merge_sort(data2.copy())
    print(f"Sorted:   {result2}")
    print("Note: Still O(n log n) - no best case optimization")
    print()
    
    # Example 3: Reverse sorted (worst case)
    print("Example 3: Reverse Sorted Data")
    print("-" * 70)
    data3 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"Original: {data3}")
    result3 = merge_sort(data3.copy())
    print(f"Sorted:   {result3}")
    print()
    
    # Example 4: In-place variant
    print("Example 4: In-Place Merge Sort")
    print("-" * 70)
    data4 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {data4}")
    merge_sort_inplace(data4, 0, len(data4) - 1)
    print(f"Sorted:   {data4}")
    print()
    
    # Example 5: Strings
    print("Example 5: Sorting Strings")
    print("-" * 70)
    data5 = ["banana", "apple", "cherry", "date", "elderberry"]
    print(f"Original: {data5}")
    result5 = merge_sort(data5.copy())
    print(f"Sorted:   {result5}")
    print()
    
    # Example 6: Performance measurement
    print("Example 6: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Merge Sort")
    
    # Test with different sizes
    for size in [100, 1000, 5000]:
        data = [random.randint(1, 1000) for _ in range(size)]
        _, metrics = timer.measure(merge_sort, data.copy())
        
        print(f"n={size:5d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    print()
    timer.print_summary()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(n log n) in all cases (best, average, worst)")
    print("  Space: O(n) auxiliary space")
    print("  Stable: Yes - maintains relative order of equal elements")
    print("  Adaptive: No - always performs same number of comparisons")
    print("\nKey Points:")
    print("  ✓ Guaranteed O(n log n) performance")
    print("  ✓ Stable sort (preserves order)")
    print("  ✓ Parallelizable (divide step)")
    print("  ✗ Requires O(n) extra space")
    print("  ✗ Not adaptive (doesn't benefit from sorted data)")
    print("\nBest For:")
    print("  - Large datasets requiring guaranteed performance")
    print("  - When stability is important")
    print("  - External sorting (disk-based)")
    print("  - Linked lists (no random access needed)")
    print("=" * 70)


if __name__ == "__main__":
    main()
