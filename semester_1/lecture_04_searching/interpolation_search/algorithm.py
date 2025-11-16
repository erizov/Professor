#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interpolation Search implementation.

Search algorithm for uniformly distributed sorted arrays.
Uses position estimation based on value.
"""

import sys
from pathlib import Path
from typing import List
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


def interpolation_search(arr: List[int], target: int) -> int:
    """
    Search for target using interpolation search algorithm.
    
    Args:
        arr: Sorted list of integers to search in
        target: Element to find
        
    Returns:
        Index of target if found, -1 otherwise
        
    Time Complexity:
        Best: O(1)
        Average: O(log log n) for uniform distribution
        Worst: O(n) for non-uniform distribution
        
    Space Complexity: O(1)
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right and target >= arr[left] and target <= arr[right]:
        # If only one element left
        if left == right:
            if arr[left] == target:
                return left
            return -1
        
        # Estimate position using interpolation formula
        pos = left + int((target - arr[left]) / 
                        (arr[right] - arr[left]) * 
                        (right - left))
        
        # Target found
        if arr[pos] == target:
            return pos
        
        # Target is in right subarray
        if arr[pos] < target:
            left = pos + 1
        # Target is in left subarray
        else:
            right = pos - 1
    
    return -1


def interpolation_search_visualized(arr: List[int], target: int) -> int:
    """
    Interpolation search with visualization.
    
    Args:
        arr: Sorted list to search
        target: Element to find
        
    Returns:
        Index of target if found, -1 otherwise
    """
    logger.info(f"Array: {arr}")
    logger.info(f"Target: {target}")
    logger.info()
    
    left = 0
    right = len(arr) - 1
    iteration = 0
    
    while left <= right and target >= arr[left] and target <= arr[right]:
        iteration += 1
        logger.debug(f"Iteration {iteration}:")
        logger.info(f"  Range: [{left}, {right}]")
        logger.info(f"  arr[{left}] = {arr[left]}, arr[{right}] = {arr[right]}")
        
        if left == right:
            if arr[left] == target:
                logger.info(f"  Found at index {left}!")
                return left
            logger.info(f"  Not found.")
            return -1
        
        # Calculate interpolated position
        pos = left + int((target - arr[left]) / 
                        (arr[right] - arr[left]) * 
                        (right - left))
        
        logger.info(f"  Interpolated position: {pos}")
        logger.info(f"  arr[{pos}] = {arr[pos]}")
        
        if arr[pos] == target:
            logger.info(f"  Found at index {pos}!")
            return pos
        
        if arr[pos] < target:
            logger.info(f"  {arr[pos]} < {target}, search right half")
            left = pos + 1
        else:
            logger.info(f"  {arr[pos]} > {target}, search left half")
            right = pos - 1
        logger.info()
    
    logger.info("Target out of range or not found.")
    return -1


def main() -> None:
    """Demonstration of Interpolation Search."""
    logger.info("=" * 70)
    logger.info("INTERPOLATION SEARCH DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Uniformly distributed data
    logger.info("Example 1: Uniformly Distributed (Best Case)")
    logger.info("-" * 70)
    data1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    target1 = 70
    result1 = interpolation_search(data1, target1)
    logger.info(f"Array: {data1}")
    logger.info(f"Target: {target1}")
    logger.info(f"Result: Index {result1}")
    if result1 != -1:
        logger.info(f"Verification: arr[{result1}] = {data1[result1]}")
    logger.info()
    
    # Example 2: Element not found
    logger.info("Example 2: Element Not Found")
    logger.info("-" * 70)
    data2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    target2 = 35
    result2 = interpolation_search(data2, target2)
    logger.info(f"Array: {data2}")
    logger.info(f"Target: {target2}")
    logger.info(f"Result: {'Not found' if result2 == -1 else f'Index {result2}'}")
    logger.info()
    
    # Example 3: First element
    logger.info("Example 3: First Element")
    logger.info("-" * 70)
    data3 = [1, 5, 10, 15, 20, 25, 30, 35, 40]
    target3 = 1
    result3 = interpolation_search(data3, target3)
    logger.info(f"Array: {data3}")
    logger.info(f"Target: {target3}")
    logger.info(f"Result: Index {result3}")
    logger.info()
    
    # Example 4: Last element
    logger.info("Example 4: Last Element")
    logger.info("-" * 70)
    data4 = [1, 5, 10, 15, 20, 25, 30, 35, 40]
    target4 = 40
    result4 = interpolation_search(data4, target4)
    logger.info(f"Array: {data4}")
    logger.info(f"Target: {target4}")
    logger.info(f"Result: Index {result4}")
    logger.info()
    
    # Example 5: Visualization
    logger.info("Example 5: Visualized Interpolation Search")
    logger.info("-" * 70)
    data5 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    target5 = 55
    result5 = interpolation_search_visualized(data5, target5)
    logger.info()
    
    # Example 6: Performance comparison
    logger.info("Example 6: Performance Measurement")
    logger.info("-" * 70)
    logger.info("With uniformly distributed data:")
    
    timer = PerformanceTimer("Interpolation Search")
    
    sizes = [1000, 10000, 100000]
    for size in sizes:
        # Uniformly distributed
        data = list(range(0, size * 10, 10))
        target = random.choice(data)
        
        _, metrics = timer.measure(interpolation_search, data, target)
        logger.info(f"n={size:6d}: {metrics['execution_time_ms']:8.3f} ms")
    
    logger.info()
    timer.print_summary()
    
    logger.info("\n" + "=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(log log n) - uniform distribution (best case)")
    logger.info("         O(n) - non-uniform distribution (worst case)")
    logger.info("  Space: O(1)")
    logger.info("\nKey Points:")
    logger.info("  + Faster than binary search for uniform data")
    logger.info("  + O(log log n) average case")
    logger.info("  + Works on sorted arrays")
    logger.info("  + Good for large uniformly distributed datasets")
    logger.info("  - Requires uniformly distributed data")
    logger.info("  - Worst case O(n) for skewed data")
    logger.info("  - More complex than binary search")
    logger.info("\nComparison with other searches:")
    logger.info("  Linear Search:        O(n)")
    logger.info("  Jump Search:          O(√n)")
    logger.info("  Binary Search:        O(log n)")
    logger.info("  Interpolation Search: O(log log n) average")
    logger.info("\nWhen to use:")
    logger.info("  • Sorted array")
    logger.info("  • Uniformly distributed data")
    logger.info("  • Large datasets")
    logger.info("  • Need fastest possible search")
    logger.info("\nWhen NOT to use:")
    logger.info("  • Non-uniform distribution")
    logger.info("  • Small datasets")
    logger.info("  • Unsorted array")
    logger.info("  • Data with large gaps")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()