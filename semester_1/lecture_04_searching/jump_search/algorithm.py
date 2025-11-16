#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jump Search implementation.

Search algorithm for sorted arrays that works by jumping
ahead by fixed steps and then performing linear search.
"""

import sys
from pathlib import Path
from typing import List, TypeVar
import random
import math

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


T = TypeVar('T')


def jump_search(arr: List[T], target: T) -> int:
    """
    Search for target using jump search algorithm.
    
    Args:
        arr: Sorted list to search in
        target: Element to find
        
    Returns:
        Index of target if found, -1 otherwise
        
    Time Complexity:
        Best: O(1)
        Average: O(√n)
        Worst: O(√n)
        
    Space Complexity: O(1)
    """
    n = len(arr)
    if n == 0:
        return -1
    
    # Calculate optimal jump size (√n)
    step = int(math.sqrt(n))
    
    # Jump to find block where element might be
    prev = 0
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        
        # If we've gone beyond the array
        if prev >= n:
            return -1
    
    # Linear search in the identified block
    while arr[prev] < target:
        prev += 1
        
        # If we've reached next block or end
        if prev == min(step, n):
            return -1
    
    # If element found
    if arr[prev] == target:
        return prev
    
    return -1


def jump_search_visualized(arr: List[int], target: int) -> int:
    """
    Jump search with visualization of the jumping process.
    
    Args:
        arr: Sorted list to search
        target: Element to find
        
    Returns:
        Index of target if found, -1 otherwise
    """
    n = len(arr)
    step = int(math.sqrt(n))
    
    logger.info(f"Array: {arr}")
    logger.info(f"Target: {target}")
    logger.debug(f"Jump size: {step} (√{n})")
    logger.info()
    
    logger.info("Jumping phase:")
    prev = 0
    jump_count = 0
    
    while arr[min(step, n) - 1] < target:
        logger.info(f"  Jump {jump_count + 1}: "
              f"Check arr[{min(step, n) - 1}] = "
              f"{arr[min(step, n) - 1]} < {target}")
        prev = step
        step += int(math.sqrt(n))
        jump_count += 1
        
        if prev >= n:
            logger.info(f"  Went beyond array. Target not found.")
            return -1
    
    logger.debug(f"  Found block: indices [{prev}:{min(step, n)}]")
    logger.info()
    
    logger.info("Linear search phase:")
    while arr[prev] < target:
        logger.info(f"  Check arr[{prev}] = {arr[prev]} < {target}")
        prev += 1
        
        if prev == min(step, n):
            logger.info(f"  Reached end of block. Target not found.")
            return -1
    
    if arr[prev] == target:
        logger.info(f"  Found! arr[{prev}] = {target}")
        return prev
    else:
        logger.info(f"  arr[{prev}] = {arr[prev]} > {target}. Not found.")
        return -1


def main() -> None:
    """Demonstration of Jump Search."""
    logger.info("=" * 70)
    logger.info("JUMP SEARCH DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic search - found
    logger.info("Example 1: Element Found")
    logger.info("-" * 70)
    data1 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target1 = 13
    result1 = jump_search(data1, target1)
    logger.info(f"Array: {data1}")
    logger.info(f"Target: {target1}")
    logger.info(f"Result: Index {result1}")
    if result1 != -1:
        logger.info(f"Verification: arr[{result1}] = {data1[result1]}")
    logger.info()
    
    # Example 2: Element not found
    logger.info("Example 2: Element Not Found")
    logger.info("-" * 70)
    data2 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target2 = 10
    result2 = jump_search(data2, target2)
    logger.info(f"Array: {data2}")
    logger.info(f"Target: {target2}")
    logger.info(f"Result: {'Not found' if result2 == -1 else f'Index {result2}'}")
    logger.info()
    
    # Example 3: First element
    logger.info("Example 3: First Element")
    logger.info("-" * 70)
    data3 = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    target3 = 10
    result3 = jump_search(data3, target3)
    logger.info(f"Array: {data3}")
    logger.info(f"Target: {target3}")
    logger.info(f"Result: Index {result3}")
    logger.info()
    
    # Example 4: Last element
    logger.info("Example 4: Last Element")
    logger.info("-" * 70)
    data4 = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    target4 = 90
    result4 = jump_search(data4, target4)
    logger.info(f"Array: {data4}")
    logger.info(f"Target: {target4}")
    logger.info(f"Result: Index {result4}")
    logger.info()
    
    # Example 5: Visualization
    logger.info("Example 5: Visualized Jump Search")
    logger.info("-" * 70)
    data5 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    target5 = 11
    result5 = jump_search_visualized(data5, target5)
    logger.info()
    
    # Example 6: Performance comparison
    logger.info("Example 6: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Jump Search")
    
    sizes = [1000, 10000, 100000]
    for size in sizes:
        data = list(range(0, size * 2, 2))  # Even numbers
        target = random.choice(data)
        
        _, metrics = timer.measure(jump_search, data, target)
        logger.info(f"n={size:6d}: {metrics['execution_time_ms']:8.3f} ms")
    
    logger.info()
    timer.print_summary()
    
    logger.info("\n" + "=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(√n)")
    logger.info("  Space: O(1)")
    logger.info("\nKey Points:")
    logger.info("  + Better than linear search O(n)")
    logger.info("  + Simpler than binary search")
    logger.info("  + Works well on sorted arrays")
    logger.info("  + Good for systems with expensive comparisons")
    logger.info("  - Requires sorted array")
    logger.info("  - Slower than binary search O(log n)")
    logger.info("  - Jump size affects performance")
    logger.info("\nComparison with other searches:")
    logger.info("  Linear Search:  O(n)")
    logger.info("  Jump Search:    O(√n)")
    logger.info("  Binary Search:  O(log n)")
    logger.info("\nWhen to use:")
    logger.info("  • Sorted array")
    logger.info("  • Middle ground between linear and binary")
    logger.info("  • Backward jumping not possible (tape storage)")
    logger.info("\nWhen NOT to use:")
    logger.info("  • Unsorted array")
    logger.info("  • Need fastest possible search (use binary)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()