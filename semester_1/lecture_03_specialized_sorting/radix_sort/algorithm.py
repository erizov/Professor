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
    if not arr or len(arr) <= 1:
        return arr
    
    # Find maximum number to know number of digits
    max_num = max(arr)
    
    # Do counting sort for every digit
    exp = 1  # Current digit (1 for ones, 10 for tens, etc.)
    while max_num // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr


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
    
    print(f"Original array: {arr}")
    
    max_num = max(arr)
    exp = 1
    pass_num = 1
    
    while max_num // exp > 0:
        print(f"\nPass {pass_num} (sorting by {exp}s place):")
        print(f"  Before: {arr}")
        
        # Show which digit we're looking at
        digits = [(num // exp) % 10 for num in arr]
        print(f"  Digits: {digits}")
        
        counting_sort_by_digit(arr, exp)
        
        print(f"  After:  {arr}")
        
        exp *= 10
        pass_num += 1
    
    print(f"\nFinal sorted array: {arr}")
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
    print("=" * 70)
    print("RADIX SORT DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic sorting
    print("Example 1: Basic Integer Sorting")
    print("-" * 70)
    data1 = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"Original: {data1}")
    result1 = radix_sort(data1.copy())
    print(f"Sorted:   {result1}")
    print()
    
    # Example 2: Small numbers
    print("Example 2: Small Numbers")
    print("-" * 70)
    data2 = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    print(f"Original: {data2}")
    result2 = radix_sort(data2.copy())
    print(f"Sorted:   {result2}")
    print()
    
    # Example 3: Large numbers
    print("Example 3: Large Numbers")
    print("-" * 70)
    data3 = [1234, 5678, 9012, 3456, 7890]
    print(f"Original: {data3}")
    result3 = radix_sort(data3.copy())
    print(f"Sorted:   {result3}")
    print()
    
    # Example 4: Duplicates
    print("Example 4: With Duplicates")
    print("-" * 70)
    data4 = [321, 123, 321, 456, 123, 789]
    print(f"Original: {data4}")
    result4 = radix_sort(data4.copy())
    print(f"Sorted:   {result4}")
    print()
    
    # Example 5: Visualization
    print("Example 5: Visualized Radix Sort")
    print("-" * 70)
    data5 = [329, 457, 657, 839, 436, 720, 355]
    result5 = radix_sort_visualized(data5.copy())
    print()
    
    # Example 6: Performance measurement
    print("Example 6: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Radix Sort")
    
    # Test with different sizes
    sizes = [100, 1000, 10000]
    for size in sizes:
        data = [random.randint(0, 9999) for _ in range(size)]
        _, metrics = timer.measure(radix_sort, data.copy())
        print(f"n={size:5d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    print()
    timer.print_summary()
    
    print("\n" + "=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(d * (n + k))")
    print("         d = number of digits, k = radix (usually 10)")
    print("  Space: O(n + k)")
    print("  Stable: Yes")
    print("  Adaptive: No")
    print("\nKey Points:")
    print("  + Linear time when d is constant")
    print("  + Stable sorting")
    print("  + No comparisons needed")
    print("  + Good for integers with fixed length")
    print("  - Only works with integers (or can be adapted)")
    print("  - Not in-place")
    print("  - Slower than comparison sorts for small n")
    print("\nWhen to use:")
    print("  • Sorting integers with limited digits")
    print("  • Need stable sort")
    print("  • n is large, d is small")
    print("  • Need linear time complexity")
    print("\nWhen NOT to use:")
    print("  • Variable-length keys")
    print("  • Small datasets")
    print("  • Need in-place sorting")
    print("=" * 70)


if __name__ == "__main__":
    main()
