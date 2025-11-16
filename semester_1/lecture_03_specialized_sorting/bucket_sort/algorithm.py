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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info(f"Original array: {arr}")
    logger.info(f"Using {num_buckets} buckets")
    
    if not arr or len(arr) <= 1:
        return arr
    
    min_val = min(arr)
    max_val = max(arr)
    
    logger.info(f"Range: {min_val:.2f} to {max_val:.2f}")
    
    # Create buckets
    buckets = [[] for _ in range(num_buckets)]
    
    # Distribute elements
    range_val = max_val - min_val
    if range_val == 0:
        return arr
    
    logger.info("\nDistributing elements:")
    for num in arr:
        index = int((num - min_val) / range_val * (num_buckets - 1))
        buckets[index].append(num)
        logger.info(f"  {num:.2f} → bucket {index}")
    
    logger.info("\nBuckets before sorting:")
    for i, bucket in enumerate(buckets):
        if bucket:
            logger.info(f"  Bucket {i}: {[f'{x:.2f}' for x in bucket]}")
    
    # Sort individual buckets
    logger.info("\nSorting individual buckets:")
    for i, bucket in enumerate(buckets):
        if bucket:
            bucket.sort()
            logger.info(f"  Bucket {i}: {[f'{x:.2f}' for x in bucket]}")
    
    # Concatenate
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    logger.info(f"\nSorted array: {[f'{x:.2f}' for x in result]}")
    return result


def main() -> None:
    """Demonstration of Bucket Sort."""
    logger.info("=" * 70)
    logger.info("BUCKET SORT DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Floating point numbers
    logger.info("Example 1: Sorting Floating Point Numbers")
    logger.info("-" * 70)
    data1 = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    logger.info(f"Original: {[f'{x:.2f}' for x in data1]}")
    result1 = bucket_sort(data1.copy())
    logger.info(f"Sorted:   {[f'{x:.2f}' for x in result1]}")
    logger.info()
    
    # Example 2: Integers
    logger.info("Example 2: Sorting Integers")
    logger.info("-" * 70)
    data2 = [42, 32, 33, 52, 37, 47, 51]
    logger.info(f"Original: {data2}")
    result2 = bucket_sort([float(x) for x in data2])
    logger.info(f"Sorted:   {[int(x) for x in result2]}")
    logger.info()
    
    # Example 3: Large range
    logger.info("Example 3: Large Range")
    logger.info("-" * 70)
    data3 = [1.5, 8.9, 3.2, 7.4, 2.1, 9.8, 4.6]
    logger.info(f"Original: {[f'{x:.1f}' for x in data3]}")
    result3 = bucket_sort(data3.copy(), num_buckets=5)
    logger.info(f"Sorted:   {[f'{x:.1f}' for x in result3]}")
    logger.info()
    
    # Example 4: Visualization
    logger.info("Example 4: Visualized Bucket Sort")
    logger.info("-" * 70)
    data4 = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51]
    result4 = bucket_sort_visualized(data4, num_buckets=5)
    logger.info()
    
    # Example 5: Performance measurement
    logger.info("Example 5: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Bucket Sort")
    
    sizes = [100, 1000, 10000]
    for size in sizes:
        data = [random.random() for _ in range(size)]
        _, metrics = timer.measure(bucket_sort, data.copy())
        logger.info(f"n={size:5d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    logger.info()
    timer.print_summary()
    
    logger.info("\n" + "=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(n + k) average with uniform distribution")
    logger.info("         O(n²) worst case (all in one bucket)")
    logger.info("  Space: O(n + k) where k is number of buckets")
    logger.info("  Stable: Yes (if underlying sort is stable)")
    logger.info("  Adaptive: No")
    logger.info("\nKey Points:")
    logger.info("  + Linear average time with uniform distribution")
    logger.info("  + Good for floating point numbers")
    logger.info("  + Can be stable")
    logger.info("  + Parallelizable (buckets independent)")
    logger.info("  - Performance depends on distribution")
    logger.info("  - Requires knowledge of input range")
    logger.info("  - Extra space for buckets")
    logger.info("\nWhen to use:")
    logger.info("  • Data is uniformly distributed")
    logger.info("  • Know input range")
    logger.info("  • Sorting floating point numbers")
    logger.info("  • Can use parallel processing")
    logger.info("\nWhen NOT to use:")
    logger.info("  • Non-uniform distribution")
    logger.info("  • Unknown or very large range")
    logger.info("  • Memory is limited")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()