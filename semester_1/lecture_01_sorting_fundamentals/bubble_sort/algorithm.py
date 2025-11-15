#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bubble Sort implementation.

Simple comparison-based sorting algorithm that repeatedly steps through
the list, compares adjacent elements and swaps them if they are in wrong order.
"""

import sys
from pathlib import Path
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer

from typing import List, TypeVar

T = TypeVar('T')


def bubble_sort(arr: List[T]) -> List[T]:
    """
    Sort array using bubble sort algorithm.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list (modifies in-place and returns)
        
    Time Complexity: O(n²) - average and worst case
    Space Complexity: O(1)
    """
    n = len(arr)
    
    for i in range(n):
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swapping occurred, array is sorted
        if not swapped:
            break
    
    return arr


def bubble_sort_visualized(arr: List[int]) -> List[int]:
    """
    Bubble sort with step-by-step visualization.
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
    """
    n = len(arr)
    print(f"Initial array: {arr}")
    print()
    
    for i in range(n):
        swapped = False
        print(f"Pass {i + 1}:")
        
        for j in range(0, n - i - 1):
            print(f"  Comparing {arr[j]} and {arr[j + 1]}", end="")
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                print(f" → Swapped: {arr}")
            else:
                print(f" → No swap")
        
        if not swapped:
            print(f"  No swaps in this pass. Array is sorted!")
            break
        print()
    
    print(f"Final sorted array: {arr}")
    return arr


def main() -> None:
    """Demonstration of Bubble Sort."""
    print("=" * 70)
    print("BUBBLE SORT DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic sorting
    print("Example 1: Basic Integer Sorting")
    print("-" * 70)
    data1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {data1}")
    result1 = bubble_sort(data1.copy())
    print(f"Sorted:   {result1}")
    print()
    
    # Example 2: Already sorted (best case)
    print("Example 2: Already Sorted Array (Best Case)")
    print("-" * 70)
    data2 = [1, 2, 3, 4, 5, 6, 7]
    print(f"Original: {data2}")
    result2 = bubble_sort(data2.copy())
    print(f"Sorted:   {result2}")
    print("Note: O(n) with early termination optimization!")
    print()
    
    # Example 3: Reverse sorted (worst case)
    print("Example 3: Reverse Sorted Array (Worst Case)")
    print("-" * 70)
    data3 = [7, 6, 5, 4, 3, 2, 1]
    print(f"Original: {data3}")
    result3 = bubble_sort(data3.copy())
    print(f"Sorted:   {result3}")
    print()
    
    # Example 4: Visualization
    print("Example 4: Visualized Bubble Sort Process")
    print("-" * 70)
    data4 = [5, 2, 8, 1, 9]
    bubble_sort_visualized(data4.copy())
    print()
    
    # Example 5: Performance measurement
    print("Example 5: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Bubble Sort")
    
    # Small dataset
    data_small = [random.randint(1, 100) for _ in range(100)]
    _, metrics_small = timer.measure(bubble_sort, data_small.copy())
    print(f"Small (100 elements):")
    print(f"  Time: {metrics_small['execution_time_ms']:.3f} ms")
    print(f"  Memory: {metrics_small['memory_peak_kb']:.2f} KB")
    
    # Medium dataset
    data_medium = [random.randint(1, 1000) for _ in range(1000)]
    _, metrics_medium = timer.measure(bubble_sort, data_medium.copy())
    print(f"\nMedium (1,000 elements):")
    print(f"  Time: {metrics_medium['execution_time_ms']:.3f} ms")
    print(f"  Memory: {metrics_medium['memory_peak_kb']:.2f} KB")
    
    print()
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(n²) - average and worst case")
    print("         O(n) - best case (with optimization)")
    print("  Space: O(1) - in-place sorting")
    print("  Stable: Yes - preserves relative order")
    print("  Adaptive: Yes - detects sorted data")
    print("\nKey Advantages:")
    print("  - Simple to understand and implement")
    print("  - Adaptive - detects sorted data")
    print("  - Stable sort")
    print("  - In-place sorting")
    print("\nKey Disadvantages:")
    print("  - Very slow on large datasets")
    print("  - O(n²) average and worst case")
    print("  - Not suitable for production use on large data")
    print("\nWhen to Use:")
    print("  - Educational purposes")
    print("  - Very small datasets (n < 10)")
    print("  - Nearly sorted data")
    print("  - When simplicity is critical")
    print("\nWhen NOT to Use:")
    print("  - Large datasets")
    print("  - Performance-critical applications")
    print("  - When O(n log n) algorithms are available")
    print("=" * 70)


if __name__ == "__main__":
    main()
