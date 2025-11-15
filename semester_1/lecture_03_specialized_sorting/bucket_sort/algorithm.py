#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bucket Sort implementation.

Distribution sort that distributes elements into buckets,
sorts them individually, then concatenates results.
"""

import sys
from pathlib import Path
from typing import List
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


def bucket_sort(arr: List[float], num_buckets: int = None) -> List[float]:
    """
    Sort array using bucket sort algorithm.
    
    Args:
        arr: List of numbers to be sorted
        num_buckets: Number of buckets (default: len(arr))
        
    Returns:
        Sorted list
        
    Time Complexity:
        Best: O(n + k) when uniformly distributed
        Average: O(n + n²/k + k) ≈ O(n) with k=n
        Worst: O(n²) when all in one bucket
        
    Space Complexity: O(n + k)
    """
    if not arr or len(arr) <= 1:
        return arr
    
    if num_buckets is None:
        num_buckets = len(arr)
    
    # Find min and max values
    min_val = min(arr)
    max_val = max(arr)
    
    # Create empty buckets
    buckets = [[] for _ in range(num_buckets)]
    
    # Distribute elements into buckets
    range_val = max_val - min_val
    if range_val == 0:
        return arr  # All elements are the same
    
    for num in arr:
        # Calculate bucket index
        index = int((num - min_val) / range_val * (num_buckets - 1))
        buckets[index].append(num)
    
    # Sort individual buckets and concatenate
    result = []
    for bucket in buckets:
        if bucket:
            # Use insertion sort for small buckets
            bucket.sort()
            result.extend(bucket)
    
    return result


def insertion_sort(arr: List[float]) -> List[float]:
    """
    Helper function: insertion sort for bucket sorting.
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def bucket_sort_integers(arr: List[int]) -> List[int]:
    """
    Bucket sort optimized for integers with known range.
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list
    """
    if not arr or len(arr) <= 1:
        return arr
    
    min_val = min(arr)
    max_val = max(arr)
    
    # Create buckets for each value
    bucket_count = max_val - min_val + 1
    buckets = [[] for _ in range(bucket_count)]
    
    # Distribute elements
    for num in arr:
        buckets[num - min_val].append(num)
    
    # Concatenate buckets
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result


def bucket_sort_visualized(arr: List[float], num_buckets: int = 5) \
        -> List[float]:
    """
    Bucket sort with visualization.
    
    Args:
        arr: List to sort
        num_buckets: Number of buckets
        
    Returns:
        Sorted list
    """
    print(f"Original array: {arr}")
    print(f"Using {num_buckets} buckets")
    
    if not arr or len(arr) <= 1:
        return arr
    
    min_val = min(arr)
    max_val = max(arr)
    
    print(f"Range: {min_val:.2f} to {max_val:.2f}")
    
    # Create buckets
    buckets = [[] for _ in range(num_buckets)]
    
    # Distribute elements
    range_val = max_val - min_val
    if range_val == 0:
        return arr
    
    print("\nDistributing elements:")
    for num in arr:
        index = int((num - min_val) / range_val * (num_buckets - 1))
        buckets[index].append(num)
        print(f"  {num:.2f} → bucket {index}")
    
    print("\nBuckets before sorting:")
    for i, bucket in enumerate(buckets):
        if bucket:
            print(f"  Bucket {i}: {[f'{x:.2f}' for x in bucket]}")
    
    # Sort individual buckets
    print("\nSorting individual buckets:")
    for i, bucket in enumerate(buckets):
        if bucket:
            bucket.sort()
            print(f"  Bucket {i}: {[f'{x:.2f}' for x in bucket]}")
    
    # Concatenate
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    print(f"\nSorted array: {[f'{x:.2f}' for x in result]}")
    return result


def main() -> None:
    """Demonstration of Bucket Sort."""
    print("=" * 70)
    print("BUCKET SORT DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Floating point numbers
    print("Example 1: Sorting Floating Point Numbers")
    print("-" * 70)
    data1 = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    print(f"Original: {[f'{x:.2f}' for x in data1]}")
    result1 = bucket_sort(data1.copy())
    print(f"Sorted:   {[f'{x:.2f}' for x in result1]}")
    print()
    
    # Example 2: Integers
    print("Example 2: Sorting Integers")
    print("-" * 70)
    data2 = [42, 32, 33, 52, 37, 47, 51]
    print(f"Original: {data2}")
    result2 = bucket_sort([float(x) for x in data2])
    print(f"Sorted:   {[int(x) for x in result2]}")
    print()
    
    # Example 3: Large range
    print("Example 3: Large Range")
    print("-" * 70)
    data3 = [1.5, 8.9, 3.2, 7.4, 2.1, 9.8, 4.6]
    print(f"Original: {[f'{x:.1f}' for x in data3]}")
    result3 = bucket_sort(data3.copy(), num_buckets=5)
    print(f"Sorted:   {[f'{x:.1f}' for x in result3]}")
    print()
    
    # Example 4: Visualization
    print("Example 4: Visualized Bucket Sort")
    print("-" * 70)
    data4 = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
    result4 = bucket_sort_visualized(data4, num_buckets=5)
    print()
    
    # Example 5: Performance measurement
    print("Example 5: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Bucket Sort")
    
    sizes = [100, 1000, 10000]
    for size in sizes:
        data = [random.random() for _ in range(size)]
        _, metrics = timer.measure(bucket_sort, data.copy())
        print(f"n={size:5d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    print()
    timer.print_summary()
    
    print("\n" + "=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(n + k) average with uniform distribution")
    print("         O(n²) worst case (all in one bucket)")
    print("  Space: O(n + k) where k is number of buckets")
    print("  Stable: Yes (if underlying sort is stable)")
    print("  Adaptive: No")
    print("\nKey Points:")
    print("  + Linear average time with uniform distribution")
    print("  + Good for floating point numbers")
    print("  + Can be stable")
    print("  + Parallelizable (buckets independent)")
    print("  - Performance depends on distribution")
    print("  - Requires knowledge of input range")
    print("  - Extra space for buckets")
    print("\nWhen to use:")
    print("  • Data is uniformly distributed")
    print("  • Know input range")
    print("  • Sorting floating point numbers")
    print("  • Can use parallel processing")
    print("\nWhen NOT to use:")
    print("  • Non-uniform distribution")
    print("  • Unknown or very large range")
    print("  • Memory is limited")
    print("=" * 70)


if __name__ == "__main__":
    main()
