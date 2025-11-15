#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Counting Sort implementation.

Integer sorting algorithm that counts occurrences of each value.
O(n+k) time complexity where k is the range of input.
"""

import sys
from pathlib import Path
from typing import List
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


def counting_sort(arr: List[int]) -> List[int]:
    """
    Sort array using counting sort algorithm.
    
    Args:
        arr: List of non-negative integers to be sorted
        
    Returns:
        Sorted list
        
    Time Complexity:
        Best: O(n + k)
        Average: O(n + k)
        Worst: O(n + k)
        where n is the number of elements, k is the range
        
    Space Complexity: O(n + k)
    """
    if not arr:
        return arr
    
    # Find range
    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1
    
    # Create count array
    count = [0] * range_size
    
    # Count occurrences
    for num in arr:
        count[num - min_val] += 1
    
    # Cumulative count
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    # Build output array
    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        num = arr[i]
        index = count[num - min_val] - 1
        output[index] = num
        count[num - min_val] -= 1
    
    return output


def counting_sort_simple(arr: List[int]) -> List[int]:
    """
    Simple counting sort (non-stable version).
    
    Args:
        arr: List of non-negative integers
        
    Returns:
        Sorted list
    """
    if not arr:
        return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1
    
    # Count occurrences
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1
    
    # Rebuild array
    result = []
    for i in range(range_size):
        result.extend([i + min_val] * count[i])
    
    return result


def counting_sort_visualized(arr: List[int]) -> List[int]:
    """
    Counting sort with visualization.
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
    """
    print(f"Original array: {arr}")
    
    if not arr:
        return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1
    
    print(f"Range: {min_val} to {max_val} (size {range_size})")
    
    # Count occurrences
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1
    
    print(f"\nCount array:")
    for i in range(range_size):
        if count[i] > 0:
            print(f"  {i + min_val}: {'*' * count[i]} ({count[i]})")
    
    # Cumulative count
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    print(f"\nCumulative count: {count}")
    
    # Build output array
    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        num = arr[i]
        index = count[num - min_val] - 1
        output[index] = num
        count[num - min_val] -= 1
    
    print(f"Sorted array: {output}")
    
    return output


def main() -> None:
    """Demonstration of Counting Sort."""
    print("=" * 70)
    print("COUNTING SORT DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic sorting
    print("Example 1: Basic Integer Sorting")
    print("-" * 70)
    data1 = [4, 2, 2, 8, 3, 3, 1]
    print(f"Original: {data1}")
    result1 = counting_sort(data1.copy())
    print(f"Sorted:   {result1}")
    print()
    
    # Example 2: Large range
    print("Example 2: Larger Range")
    print("-" * 70)
    data2 = [64, 34, 25, 12, 22, 11, 90, 88]
    print(f"Original: {data2}")
    result2 = counting_sort(data2.copy())
    print(f"Sorted:   {result2}")
    print()
    
    # Example 3: Negative numbers
    print("Example 3: With Negative Numbers")
    print("-" * 70)
    data3 = [3, -1, 2, -5, 0, 4, -3]
    print(f"Original: {data3}")
    result3 = counting_sort(data3.copy())
    print(f"Sorted:   {result3}")
    print()
    
    # Example 4: Duplicates
    print("Example 4: Many Duplicates")
    print("-" * 70)
    data4 = [5, 2, 2, 2, 9, 1, 5, 5, 5]
    print(f"Original: {data4}")
    result4 = counting_sort(data4.copy())
    print(f"Sorted:   {result4}")
    print()
    
    # Example 5: Visualization
    print("Example 5: Visualized Counting Sort")
    print("-" * 70)
    data5 = [1, 4, 1, 2, 7, 5, 2]
    result5 = counting_sort_visualized(data5)
    print()
    
    # Example 6: Performance measurement
    print("Example 6: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Counting Sort")
    
    # Test with small range
    sizes = [100, 1000, 10000]
    for size in sizes:
        data = [random.randint(0, 100) for _ in range(size)]
        _, metrics = timer.measure(counting_sort, data.copy())
        print(f"n={size:5d}, k=100: {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    print()
    timer.print_summary()
    
    print("\n" + "=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(n + k) where k is the range")
    print("  Space: O(n + k)")
    print("  Stable: Yes (standard implementation)")
    print("  Adaptive: No")
    print("\nKey Points:")
    print("  + Linear time complexity O(n+k)")
    print("  + Stable sorting")
    print("  + Good for small range of integers")
    print("  + No comparisons needed")
    print("  - Only works with integers")
    print("  - Inefficient for large ranges")
    print("  - Requires extra memory O(k)")
    print("\nWhen to use:")
    print("  • Sorting integers")
    print("  • Range k is not too large (k ≤ n)")
    print("  • Need linear time sort")
    print("  • Stable sort required")
    print("\nWhen NOT to use:")
    print("  • Range is very large (k >> n)")
    print("  • Sorting floats or strings")
    print("  • Memory is limited")
    print("=" * 70)


if __name__ == "__main__":
    main()
