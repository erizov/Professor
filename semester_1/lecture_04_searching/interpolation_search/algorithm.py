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
    print(f"Array: {arr}")
    print(f"Target: {target}")
    print()
    
    left = 0
    right = len(arr) - 1
    iteration = 0
    
    while left <= right and target >= arr[left] and target <= arr[right]:
        iteration += 1
        print(f"Iteration {iteration}:")
        print(f"  Range: [{left}, {right}]")
        print(f"  arr[{left}] = {arr[left]}, arr[{right}] = {arr[right]}")
        
        if left == right:
            if arr[left] == target:
                print(f"  Found at index {left}!")
                return left
            print(f"  Not found.")
            return -1
        
        # Calculate interpolated position
        pos = left + int((target - arr[left]) / 
                        (arr[right] - arr[left]) * 
                        (right - left))
        
        print(f"  Interpolated position: {pos}")
        print(f"  arr[{pos}] = {arr[pos]}")
        
        if arr[pos] == target:
            print(f"  Found at index {pos}!")
            return pos
        
        if arr[pos] < target:
            print(f"  {arr[pos]} < {target}, search right half")
            left = pos + 1
        else:
            print(f"  {arr[pos]} > {target}, search left half")
            right = pos - 1
        print()
    
    print("Target out of range or not found.")
    return -1


def main() -> None:
    """Demonstration of Interpolation Search."""
    print("=" * 70)
    print("INTERPOLATION SEARCH DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Uniformly distributed data
    print("Example 1: Uniformly Distributed (Best Case)")
    print("-" * 70)
    data1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    target1 = 70
    result1 = interpolation_search(data1, target1)
    print(f"Array: {data1}")
    print(f"Target: {target1}")
    print(f"Result: Index {result1}")
    if result1 != -1:
        print(f"Verification: arr[{result1}] = {data1[result1]}")
    print()
    
    # Example 2: Element not found
    print("Example 2: Element Not Found")
    print("-" * 70)
    data2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    target2 = 35
    result2 = interpolation_search(data2, target2)
    print(f"Array: {data2}")
    print(f"Target: {target2}")
    print(f"Result: {'Not found' if result2 == -1 else f'Index {result2}'}")
    print()
    
    # Example 3: First element
    print("Example 3: First Element")
    print("-" * 70)
    data3 = [1, 5, 10, 15, 20, 25, 30, 35, 40]
    target3 = 1
    result3 = interpolation_search(data3, target3)
    print(f"Array: {data3}")
    print(f"Target: {target3}")
    print(f"Result: Index {result3}")
    print()
    
    # Example 4: Last element
    print("Example 4: Last Element")
    print("-" * 70)
    data4 = [1, 5, 10, 15, 20, 25, 30, 35, 40]
    target4 = 40
    result4 = interpolation_search(data4, target4)
    print(f"Array: {data4}")
    print(f"Target: {target4}")
    print(f"Result: Index {result4}")
    print()
    
    # Example 5: Visualization
    print("Example 5: Visualized Interpolation Search")
    print("-" * 70)
    data5 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    target5 = 55
    result5 = interpolation_search_visualized(data5, target5)
    print()
    
    # Example 6: Performance comparison
    print("Example 6: Performance Measurement")
    print("-" * 70)
    print("With uniformly distributed data:")
    
    timer = PerformanceTimer("Interpolation Search")
    
    sizes = [1000, 10000, 100000]
    for size in sizes:
        # Uniformly distributed
        data = list(range(0, size * 10, 10))
        target = random.choice(data)
        
        _, metrics = timer.measure(interpolation_search, data, target)
        print(f"n={size:6d}: {metrics['execution_time_ms']:8.3f} ms")
    
    print()
    timer.print_summary()
    
    print("\n" + "=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(log log n) - uniform distribution (best case)")
    print("         O(n) - non-uniform distribution (worst case)")
    print("  Space: O(1)")
    print("\nKey Points:")
    print("  + Faster than binary search for uniform data")
    print("  + O(log log n) average case")
    print("  + Works on sorted arrays")
    print("  + Good for large uniformly distributed datasets")
    print("  - Requires uniformly distributed data")
    print("  - Worst case O(n) for skewed data")
    print("  - More complex than binary search")
    print("\nComparison with other searches:")
    print("  Linear Search:        O(n)")
    print("  Jump Search:          O(√n)")
    print("  Binary Search:        O(log n)")
    print("  Interpolation Search: O(log log n) average")
    print("\nWhen to use:")
    print("  • Sorted array")
    print("  • Uniformly distributed data")
    print("  • Large datasets")
    print("  • Need fastest possible search")
    print("\nWhen NOT to use:")
    print("  • Non-uniform distribution")
    print("  • Small datasets")
    print("  • Unsorted array")
    print("  • Data with large gaps")
    print("=" * 70)


if __name__ == "__main__":
    main()
