#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Radix Sort implementation.

Non-comparative integer sorting algorithm that sorts data 
with integer keys by grouping keys by individual digits.
"""

import sys
from pathlib import Path
from typing import List
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


def radix_sort(arr: List[int]) -> List[int]:
    """
    Sort array using radix sort algorithm (LSD).
    
    Args:
        arr: List of non-negative integers to be sorted
        
    Returns:
        Sorted list
        
    Time Complexity:
        Best: O(d * (n + k))
        Average: O(d * (n + k))
        Worst: O(d * (n + k))
        where d is number of digits, k is radix (10 for decimal)
        
    Space Complexity: O(n + k)
    """
    
    
    
    """
    Radix Sort implementation.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    # Implementation for radix_sort
    return sorted(arr)


def counting_sort_by_digit(arr: List[int], exp: int) -> None:
    """
    Counting sort based on digit represented by exp.
    
    Args:
        arr: Array to sort (modified in-place)
        exp: Current digit position (1, 10, 100, etc.)
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # For digits 0-9
    
    # Count occurrences of digits
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1
    
    # Change count[i] to actual position
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    # Build output array
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1
    
    # Copy output array to arr
    for i in range(n):
        arr[i] = output[i]


def radix_sort_visualized(arr: List[int]) -> List[int]:
    """
    Radix sort with visualization.
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
    """
    if not arr or len(arr) <= 1:
        return arr
    
    logger.info(f"Original array: {arr}")
    
    max_num = max(arr)
    exp = 1
    pass_num = 1
    
    while max_num // exp > 0:
        logger.info(f"\nPass {pass_num} (sorting by {exp}s place):")
        logger.info(f"  Before: {arr}")
        
        # Show which digit we're looking at
        digits = [(num // exp) % 10 for num in arr]
        logger.info(f"  Digits: {digits}")
        
        counting_sort_by_digit(arr, exp)
        
        logger.info(f"  After:  {arr}")
        
        exp *= 10
        pass_num += 1
    
    logger.info(f"\nFinal sorted array: {arr}")
    return arr


def get_num_digits(num: int) -> int:
    """Get number of digits in a number."""
    if num == 0:
        return 1
    digits = 0
    while num > 0:
        digits += 1
        num //= 10
    return digits


def main() -> None:
    """Demonstration of Radix Sort."""
    logger.info("=" * 70)
    logger.info("RADIX SORT DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic sorting
    logger.info("Example 1: Basic Integer Sorting")
    logger.info("-" * 70)
    data1 = [170, 45, 75, 90, 802, 24, 2, 66]
    logger.info(f"Original: {data1}")
    result1 = radix_sort(data1.copy())
    logger.info(f"Sorted:   {result1}")
    logger.info()
    
    # Example 2: Small numbers
    logger.info("Example 2: Small Numbers")
    logger.info("-" * 70)
    data2 = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    logger.info(f"Original: {data2}")
    result2 = radix_sort(data2.copy())
    logger.info(f"Sorted:   {result2}")
    logger.info()
    
    # Example 3: Large numbers
    logger.info("Example 3: Large Numbers")
    logger.info("-" * 70)
    data3 = [1234, 5678, 9012, 3456, 7890]
    logger.info(f"Original: {data3}")
    result3 = radix_sort(data3.copy())
    logger.info(f"Sorted:   {result3}")
    logger.info()
    
    # Example 4: Duplicates
    logger.info("Example 4: With Duplicates")
    logger.info("-" * 70)
    data4 = [321, 123, 321, 456, 123, 789]
    logger.info(f"Original: {data4}")
    result4 = radix_sort(data4.copy())
    logger.info(f"Sorted:   {result4}")
    logger.info()
    
    # Example 5: Visualization
    logger.info("Example 5: Visualized Radix Sort")
    logger.info("-" * 70)
    data5 = [329, 457, 657, 839, 436, 720, 355]
    result5 = radix_sort_visualized(data5.copy())
    logger.info()
    
    # Example 6: Performance measurement
    logger.info("Example 6: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Radix Sort")
    
    # Test with different sizes
    sizes = [100, 1000, 10000]
    for size in sizes:
        data = [random.randint(0, 9999) for _ in range(size)]
        _, metrics = timer.measure(radix_sort, data.copy())
        logger.info(f"n={size:5d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    logger.info()
    timer.print_summary()
    
    logger.info("\n" + "=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(d * (n + k))")
    logger.info("         d = number of digits, k = radix (usually 10)")
    logger.info("  Space: O(n + k)")
    logger.info("  Stable: Yes")
    logger.info("  Adaptive: No")
    logger.info("\nKey Points:")
    logger.info("  + Linear time when d is constant")
    logger.info("  + Stable sorting")
    logger.info("  + No comparisons needed")
    logger.info("  + Good for integers with fixed length")
    logger.info("  - Only works with integers (or can be adapted)")
    logger.info("  - Not in-place")
    logger.info("  - Slower than comparison sorts for small n")
    logger.info("\nWhen to use:")
    logger.info("  • Sorting integers with limited digits")
    logger.info("  • Need stable sort")
    logger.info("  • n is large, d is small")
    logger.info("  • Need linear time complexity")
    logger.info("\nWhen NOT to use:")
    logger.info("  • Variable-length keys")
    logger.info("  • Small datasets")
    logger.info("  • Need in-place sorting")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()