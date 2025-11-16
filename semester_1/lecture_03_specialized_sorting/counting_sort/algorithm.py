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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info(f"Original array: {arr}")
    
    if not arr:
        return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_size = max_val - min_val + 1
    
    logger.info(f"Range: {min_val} to {max_val} (size {range_size})")
    
    # Count occurrences
    count = [0] * range_size
    for num in arr:
        count[num - min_val] += 1
    
    logger.info(f"\nCount array:")
    for i in range(range_size):
        if count[i] > 0:
            logger.info(f"  {i + min_val}: {'*' * count[i]} ({count[i]})")
    
    # Cumulative count
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    
    logger.info(f"\nCumulative count: {count}")
    
    # Build output array
    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        num = arr[i]
        index = count[num - min_val] - 1
        output[index] = num
        count[num - min_val] -= 1
    
    logger.info(f"Sorted array: {output}")
    
    return output


def main() -> None:
    """Demonstration of Counting Sort."""
    logger.info("=" * 70)
    logger.info("COUNTING SORT DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic sorting
    logger.info("Example 1: Basic Integer Sorting")
    logger.info("-" * 70)
    data1 = [4, 2, 2, 8, 3, 3, 1]
    logger.info(f"Original: {data1}")
    result1 = counting_sort(data1.copy())
    logger.info(f"Sorted:   {result1}")
    logger.info()
    
    # Example 2: Large range
    logger.info("Example 2: Larger Range")
    logger.info("-" * 70)
    data2 = [64, 34, 25, 12, 22, 11, 90, 88]
    logger.info(f"Original: {data2}")
    result2 = counting_sort(data2.copy())
    logger.info(f"Sorted:   {result2}")
    logger.info()
    
    # Example 3: Negative numbers
    logger.info("Example 3: With Negative Numbers")
    logger.info("-" * 70)
    data3 = [3, -1, 2, -5, 0, 4, -3]
    logger.info(f"Original: {data3}")
    result3 = counting_sort(data3.copy())
    logger.info(f"Sorted:   {result3}")
    logger.info()
    
    # Example 4: Duplicates
    logger.info("Example 4: Many Duplicates")
    logger.info("-" * 70)
    data4 = [5, 2, 2, 2, 9, 1, 5, 5, 5]
    logger.info(f"Original: {data4}")
    result4 = counting_sort(data4.copy())
    logger.info(f"Sorted:   {result4}")
    logger.info()
    
    # Example 5: Visualization
    logger.info("Example 5: Visualized Counting Sort")
    logger.info("-" * 70)
    data5 = [1, 4, 1, 2, 7, 5, 2]
    result5 = counting_sort_visualized(data5)
    logger.info()
    
    # Example 6: Performance measurement
    logger.info("Example 6: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Counting Sort")
    
    # Test with small range
    sizes = [100, 1000, 10000]
    for size in sizes:
        data = [random.randint(0, 100) for _ in range(size)]
        _, metrics = timer.measure(counting_sort, data.copy())
        logger.info(f"n={size:5d}, k=100: {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    logger.info()
    timer.print_summary()
    
    logger.info("\n" + "=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(n + k) where k is the range")
    logger.info("  Space: O(n + k)")
    logger.info("  Stable: Yes (standard implementation)")
    logger.info("  Adaptive: No")
    logger.info("\nKey Points:")
    logger.info("  + Linear time complexity O(n+k)")
    logger.info("  + Stable sorting")
    logger.info("  + Good for small range of integers")
    logger.info("  + No comparisons needed")
    logger.info("  - Only works with integers")
    logger.info("  - Inefficient for large ranges")
    logger.info("  - Requires extra memory O(k)")
    logger.info("\nWhen to use:")
    logger.info("  • Sorting integers")
    logger.info("  • Range k is not too large (k ≤ n)")
    logger.info("  • Need linear time sort")
    logger.info("  • Stable sort required")
    logger.info("\nWhen NOT to use:")
    logger.info("  • Range is very large (k >> n)")
    logger.info("  • Sorting floats or strings")
    logger.info("  • Memory is limited")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()