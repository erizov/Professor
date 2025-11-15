#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Merge Sort implementation.

Efficient divide-and-conquer sorting algorithm that divides the array
into halves, sorts them recursively, and merges the sorted halves.
"""

import sys
from pathlib import Path
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer

from typing import List, TypeVar

T = TypeVar('T')


def merge_sort(arr: List[T]) -> List[T]:
    """
    Sort array using merge sort algorithm.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
        
    Time Complexity: O(n log n) - all cases
    Space Complexity: O(n)
    """
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Conquer (merge)
    return merge(left, right)


def merge(left: List[T], right: List[T]) -> List[T]:
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
    
    # Compare elements from both arrays
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def merge_sort_inplace(arr: List[T], start: int = 0, 
                       end: int = None) -> None:
    """
    In-place merge sort (optimized for space).
    
    Args:
        arr: List to be sorted
        start: Starting index
        end: Ending index
    """
    if end is None:
        end = len(arr)
    
    if end - start <= 1:
        return
    
    mid = (start + end) // 2
    merge_sort_inplace(arr, start, mid)
    merge_sort_inplace(arr, mid, end)
    merge_inplace(arr, start, mid, end)


def merge_inplace(arr: List[T], start: int, mid: int, end: int) -> None:
    """Merge sorted subarrays in place."""
    left = arr[start:mid]
    right = arr[mid:end]
    
    i = j = 0
    k = start
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


def visualize_merge_sort(arr: List[int], depth: int = 0) -> List[int]:
    """
    Merge sort with visualization of the recursion process.
    
    Args:
        arr: List to sort
        depth: Current recursion depth (for indentation)
        
    Returns:
        Sorted list
    """
    indent = "  " * depth
    print(f"{indent}Sorting: {arr}")
    
    if len(arr) <= 1:
        print(f"{indent}Base case: {arr}")
        return arr
    
    mid = len(arr) // 2
    print(f"{indent}Dividing at index {mid}")
    
    left = visualize_merge_sort(arr[:mid], depth + 1)
    right = visualize_merge_sort(arr[mid:], depth + 1)
    
    result = merge(left, right)
    print(f"{indent}Merged: {result}")
    
    return result


def main() -> None:
    """Demonstration of Merge Sort."""
    print("=" * 70)
    print("MERGE SORT DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic sorting
    print("Example 1: Basic Integer Sorting")
    print("-" * 70)
    data1 = [64, 34, 25, 12, 22, 11, 90, 88]
    print(f"Original: {data1}")
    result1 = merge_sort(data1.copy())
    print(f"Sorted:   {result1}")
    print()
    
    # Example 2: Already sorted (best case)
    print("Example 2: Already Sorted Array")
    print("-" * 70)
    data2 = [1, 2, 3, 4, 5, 6, 7, 8]
    print(f"Original: {data2}")
    result2 = merge_sort(data2.copy())
    print(f"Sorted:   {result2}")
    print("Note: Still O(n log n) even when sorted!")
    print()
    
    # Example 3: Reverse sorted (worst case for some algorithms)
    print("Example 3: Reverse Sorted Array")
    print("-" * 70)
    data3 = [8, 7, 6, 5, 4, 3, 2, 1]
    print(f"Original: {data3}")
    result3 = merge_sort(data3.copy())
    print(f"Sorted:   {result3}")
    print()
    
    # Example 4: Strings
    print("Example 4: Sorting Strings")
    print("-" * 70)
    data4 = ["banana", "apple", "cherry", "date", "elderberry"]
    print(f"Original: {data4}")
    result4 = merge_sort(data4.copy())
    print(f"Sorted:   {result4}")
    print()
    
    # Example 5: Visualization
    print("Example 5: Visualized Merge Sort Process")
    print("-" * 70)
    data5 = [5, 2, 8, 1, 9, 3]
    print("Watch the divide-and-conquer process:\n")
    result5 = visualize_merge_sort(data5)
    print()
    
    # Example 6: Performance comparison
    print("Example 6: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Merge Sort")
    
    # Small dataset
    data_small = [random.randint(1, 100) for _ in range(100)]
    _, metrics_small = timer.measure(merge_sort, data_small.copy())
    print(f"Small (100 elements):")
    print(f"  Time: {metrics_small['execution_time_ms']:.3f} ms")
    print(f"  Memory: {metrics_small['memory_peak_kb']:.2f} KB")
    
    # Medium dataset
    data_medium = [random.randint(1, 1000) for _ in range(1000)]
    _, metrics_medium = timer.measure(merge_sort, data_medium.copy())
    print(f"\nMedium (1,000 elements):")
    print(f"  Time: {metrics_medium['execution_time_ms']:.3f} ms")
    print(f"  Memory: {metrics_medium['memory_peak_kb']:.2f} KB")
    
    # Large dataset
    data_large = [random.randint(1, 10000) for _ in range(10000)]
    _, metrics_large = timer.measure(merge_sort, data_large.copy())
    print(f"\nLarge (10,000 elements):")
    print(f"  Time: {metrics_large['execution_time_ms']:.3f} ms")
    print(f"  Memory: {metrics_large['memory_peak_kb']:.2f} KB")
    print()
    
    # Example 7: In-place version
    print("Example 7: In-place Merge Sort")
    print("-" * 70)
    data7 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {data7}")
    merge_sort_inplace(data7)
    print(f"Sorted:   {data7}")
    print("(Uses less memory but still O(n) auxiliary space)")
    print()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(n log n) - all cases (best, average, worst)")
    print("  Space: O(n) - requires auxiliary array")
    print("  Stable: Yes - preserves relative order")
    print("  Adaptive: No - always O(n log n)")
    print("\nKey Advantages:")
    print("  - Guaranteed O(n log n) performance")
    print("  - Stable sorting algorithm")
    print("  - Good for linked lists")
    print("  - Parallelizable")
    print("\nKey Disadvantages:")
    print("  - Requires O(n) extra space")
    print("  - Slower than quick sort in practice")
    print("  - Not in-place")
    print("=" * 70)


if __name__ == "__main__":
    main()
