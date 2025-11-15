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
    
    print(f"Array: {arr}")
    print(f"Target: {target}")
    print(f"Jump size: {step} (√{n})")
    print()
    
    print("Jumping phase:")
    prev = 0
    jump_count = 0
    
    while arr[min(step, n) - 1] < target:
        print(f"  Jump {jump_count + 1}: "
              f"Check arr[{min(step, n) - 1}] = "
              f"{arr[min(step, n) - 1]} < {target}")
        prev = step
        step += int(math.sqrt(n))
        jump_count += 1
        
        if prev >= n:
            print(f"  Went beyond array. Target not found.")
            return -1
    
    print(f"  Found block: indices [{prev}:{min(step, n)}]")
    print()
    
    print("Linear search phase:")
    while arr[prev] < target:
        print(f"  Check arr[{prev}] = {arr[prev]} < {target}")
        prev += 1
        
        if prev == min(step, n):
            print(f"  Reached end of block. Target not found.")
            return -1
    
    if arr[prev] == target:
        print(f"  Found! arr[{prev}] = {target}")
        return prev
    else:
        print(f"  arr[{prev}] = {arr[prev]} > {target}. Not found.")
        return -1


def main() -> None:
    """Demonstration of Jump Search."""
    print("=" * 70)
    print("JUMP SEARCH DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic search - found
    print("Example 1: Element Found")
    print("-" * 70)
    data1 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target1 = 13
    result1 = jump_search(data1, target1)
    print(f"Array: {data1}")
    print(f"Target: {target1}")
    print(f"Result: Index {result1}")
    if result1 != -1:
        print(f"Verification: arr[{result1}] = {data1[result1]}")
    print()
    
    # Example 2: Element not found
    print("Example 2: Element Not Found")
    print("-" * 70)
    data2 = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target2 = 10
    result2 = jump_search(data2, target2)
    print(f"Array: {data2}")
    print(f"Target: {target2}")
    print(f"Result: {'Not found' if result2 == -1 else f'Index {result2}'}")
    print()
    
    # Example 3: First element
    print("Example 3: First Element")
    print("-" * 70)
    data3 = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    target3 = 10
    result3 = jump_search(data3, target3)
    print(f"Array: {data3}")
    print(f"Target: {target3}")
    print(f"Result: Index {result3}")
    print()
    
    # Example 4: Last element
    print("Example 4: Last Element")
    print("-" * 70)
    data4 = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    target4 = 90
    result4 = jump_search(data4, target4)
    print(f"Array: {data4}")
    print(f"Target: {target4}")
    print(f"Result: Index {result4}")
    print()
    
    # Example 5: Visualization
    print("Example 5: Visualized Jump Search")
    print("-" * 70)
    data5 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    target5 = 11
    result5 = jump_search_visualized(data5, target5)
    print()
    
    # Example 6: Performance comparison
    print("Example 6: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Jump Search")
    
    sizes = [1000, 10000, 100000]
    for size in sizes:
        data = list(range(0, size * 2, 2))  # Even numbers
        target = random.choice(data)
        
        _, metrics = timer.measure(jump_search, data, target)
        print(f"n={size:6d}: {metrics['execution_time_ms']:8.3f} ms")
    
    print()
    timer.print_summary()
    
    print("\n" + "=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(√n)")
    print("  Space: O(1)")
    print("\nKey Points:")
    print("  + Better than linear search O(n)")
    print("  + Simpler than binary search")
    print("  + Works well on sorted arrays")
    print("  + Good for systems with expensive comparisons")
    print("  - Requires sorted array")
    print("  - Slower than binary search O(log n)")
    print("  - Jump size affects performance")
    print("\nComparison with other searches:")
    print("  Linear Search:  O(n)")
    print("  Jump Search:    O(√n)")
    print("  Binary Search:  O(log n)")
    print("\nWhen to use:")
    print("  • Sorted array")
    print("  • Middle ground between linear and binary")
    print("  • Backward jumping not possible (tape storage)")
    print("\nWhen NOT to use:")
    print("  • Unsorted array")
    print("  • Need fastest possible search (use binary)")
    print("=" * 70)


if __name__ == "__main__":
    main()
