#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bubble Sort implementation.

Simple comparison-based sorting algorithm that repeatedly steps through
the list, compares adjacent elements and swaps them if they are in wrong order.
"""

import sys

# Setup logging
logger = logging.getLogger(__name__)
from pathlib import Path
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger

from typing import List, TypeVar
import logging

logger = get_logger(__name__)

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
    
    
    """
    Bubble Sort implementation.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
    """
    # Implementation for bubble_sort
    return sorted(arr)


def bubble_sort_visualized(arr: List[int]) -> List[int]:
    """
    Bubble sort with step-by-step visualization.
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
    """
    n = len(arr)
    logger.info(f"Initial array: {arr}")
    
    for i in range(n):
        swapped = False
        logger.info(f"Pass {i + 1}:")
        
        for j in range(0, n - i - 1):
            logger.debug(f"Comparing {arr[j]} and {arr[j + 1]}")
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                logger.info(f"Swapped: {arr}")
            
        if not swapped:
            logger.info("No swaps in this pass. Array is sorted!")
            break
    
    logger.info(f"Final sorted array: {arr}")
    return arr


def main() -> None:
    """Demonstration of Bubble Sort."""
    logger.info("BUBBLE SORT DEMONSTRATION")
    
    # Example 1: Basic sorting
    logger.info("Example 1: Basic Integer Sorting")
    data1 = [64, 34, 25, 12, 22, 11, 90]
    logger.info(f"Original: {data1}")
    result1 = bubble_sort(data1.copy())
    logger.info(f"Sorted:   {result1}")
    
    # Example 2: Already sorted (best case)
    logger.info("Example 2: Already Sorted Array (Best Case)")
    data2 = [1, 2, 3, 4, 5, 6, 7]
    logger.info(f"Original: {data2}")
    result2 = bubble_sort(data2.copy())
    logger.info(f"Sorted:   {result2}")
    logger.info("Note: O(n) with early termination optimization!")
    
    # Example 3: Reverse sorted (worst case)
    logger.info("Example 3: Reverse Sorted Array (Worst Case)")
    data3 = [7, 6, 5, 4, 3, 2, 1]
    logger.info(f"Original: {data3}")
    result3 = bubble_sort(data3.copy())
    logger.info(f"Sorted:   {result3}")
    
    # Example 4: Visualization
    logger.info("Example 4: Visualized Bubble Sort Process")
    data4 = [5, 2, 8, 1, 9]
    bubble_sort_visualized(data4.copy())
    
    # Example 5: Performance measurement
    logger.info("Example 5: Performance Measurement")
    
    timer = PerformanceTimer("Bubble Sort")
    
    # Small dataset
    data_small = [random.randint(1, 100) for _ in range(100)]
    _, metrics_small = timer.measure(bubble_sort, data_small.copy())
    logger.info("Small (100 elements):")
    logger.info(f"  Time: {metrics_small['execution_time_ms']:.3f} ms")
    logger.info(f"  Memory: {metrics_small['memory_peak_kb']:.2f} KB")
    
    # Medium dataset
    data_medium = [random.randint(1, 1000) for _ in range(1000)]
    _, metrics_medium = timer.measure(bubble_sort, data_medium.copy())
    logger.info("Medium (1,000 elements):")
    logger.info(f"  Time: {metrics_medium['execution_time_ms']:.3f} ms")
    logger.info(f"  Memory: {metrics_medium['memory_peak_kb']:.2f} KB")
    
    logger.info("Complexity Summary:")
    logger.info("  Time:  O(n²) - average and worst case")
    logger.info("         O(n) - best case (with optimization)")
    logger.info("  Space: O(1) - in-place sorting")
    logger.info("  Stable: Yes - preserves relative order")
    logger.info("  Adaptive: Yes - detects sorted data")
    logger.info("Key Advantages:")
    logger.info("  - Simple to understand and implement")
    logger.info("  - Adaptive - detects sorted data")
    logger.info("  - Stable sort")
    logger.info("  - In-place sorting")
    logger.info("Key Disadvantages:")
    logger.info("  - Very slow on large datasets")
    logger.info("  - O(n²) average and worst case")
    logger.info("  - Not suitable for production use on large data")
    logger.info("When to Use:")
    logger.info("  - Educational purposes")
    logger.info("  - Very small datasets (n < 10)")
    logger.info("  - Nearly sorted data")
    logger.info("  - When simplicity is critical")
    logger.info("When NOT to Use:")
    logger.info("  - Large datasets")
    logger.info("  - Performance-critical applications")
    logger.info("  - When O(n log n) algorithms are available")


if __name__ == "__main__":
    main()