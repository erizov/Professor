#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Heap Sort implementation.

Sorting algorithm based on binary heap data structure. Uses max-heap
to sort in ascending order.
"""

import sys
from pathlib import Path
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer

from typing import List, TypeVar

T = TypeVar('T')


def heapify(arr: List[T], n: int, i: int) -> None:
    """
    Heapify subtree rooted at index i.
    
    Args:
        arr: Array to heapify
        n: Size of heap
        i: Root index of subtree
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    # Check if left child exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    # Check if right child exists and is greater than largest
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    # If largest is not root, swap and continue heapifying
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr: List[T]) -> List[T]:
    """
    Sort array using heap sort algorithm.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list (modifies in-place and returns)
        
    Time Complexity: O(n log n) - all cases
    Space Complexity: O(1) - in-place (O(log n) for recursion)
    """
    n = len(arr)
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    # Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root to end
        arr[0], arr[i] = arr[i], arr[0]
        
        # Heapify the reduced heap
        heapify(arr, i, 0)
    
    return arr


def heap_sort_visualized(arr: List[int]) -> List[int]:
    """
    Heap sort with step-by-step visualization.
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
    """
    n = len(arr)
    print(f"Initial array: {arr}")
    print()
    
    # Build max heap
    print("Building max heap:")
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
        print(f"  After heapifying at index {i}: {arr}")
    print(f"Max heap built: {arr}")
    print()
    
    # Extract elements
    print("Extracting elements:")
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        print(f"  Moved {arr[i]} to position {i}: {arr[:i]} | [{arr[i:]}]")
        heapify(arr, i, 0)
        print(f"  After heapify: {arr[:i]} | [{arr[i:]}]")
    
    print(f"\nFinal sorted array: {arr}")
    return arr


def build_min_heap(arr: List[T]) -> None:
    """Build a min heap (for descending order sort)."""
    n = len(arr)
    
    def min_heapify(arr: List[T], n: int, i: int) -> None:
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] < arr[smallest]:
            smallest = left
        if right < n and arr[right] < arr[smallest]:
            smallest = right
        
        if smallest != i:
            arr[i], arr[smallest] = arr[smallest], arr[i]
            min_heapify(arr, n, smallest)
    
    for i in range(n // 2 - 1, -1, -1):
        min_heapify(arr, n, i)


def heap_sort_descending(arr: List[T]) -> List[T]:
    """Sort in descending order using min heap."""
    n = len(arr)
    
    # Build min heap
    build_min_heap(arr)
    
    def min_heapify(arr: List[T], n: int, i: int) -> None:
        smallest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] < arr[smallest]:
            smallest = left
        if right < n and arr[right] < arr[smallest]:
            smallest = right
        
        if smallest != i:
            arr[i], arr[smallest] = arr[smallest], arr[i]
            min_heapify(arr, n, smallest)
    
    # Extract elements
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        min_heapify(arr, i, 0)
    
    return arr


def main() -> None:
    """Demonstration of Heap Sort."""
    print("=" * 70)
    print("HEAP SORT DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic sorting
    print("Example 1: Basic Integer Sorting")
    print("-" * 70)
    data1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {data1}")
    result1 = heap_sort(data1.copy())
    print(f"Sorted:   {result1}")
    print()
    
    # Example 2: Already sorted
    print("Example 2: Already Sorted Array")
    print("-" * 70)
    data2 = [1, 2, 3, 4, 5, 6, 7]
    print(f"Original: {data2}")
    result2 = heap_sort(data2.copy())
    print(f"Sorted:   {result2}")
    print("Note: Still O(n log n) - not adaptive")
    print()
    
    # Example 3: Reverse sorted
    print("Example 3: Reverse Sorted Array")
    print("-" * 70)
    data3 = [7, 6, 5, 4, 3, 2, 1]
    print(f"Original: {data3}")
    result3 = heap_sort(data3.copy())
    print(f"Sorted:   {result3}")
    print()
    
    # Example 4: Descending order
    print("Example 4: Descending Order")
    print("-" * 70)
    data4 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original: {data4}")
    result4 = heap_sort_descending(data4.copy())
    print(f"Sorted (desc): {result4}")
    print()
    
    # Example 5: Visualization
    print("Example 5: Visualized Heap Sort Process")
    print("-" * 70)
    data5 = [12, 11, 13, 5, 6, 7]
    heap_sort_visualized(data5)
    print()
    
    # Example 6: Performance measurement
    print("Example 6: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Heap Sort")
    
    # Small dataset
    data_small = [random.randint(1, 100) for _ in range(100)]
    _, metrics_small = timer.measure(heap_sort, data_small.copy())
    print(f"Small (100 elements):")
    print(f"  Time: {metrics_small['execution_time_ms']:.3f} ms")
    print(f"  Memory: {metrics_small['memory_peak_kb']:.2f} KB")
    
    # Medium dataset
    data_medium = [random.randint(1, 1000) for _ in range(1000)]
    _, metrics_medium = timer.measure(heap_sort, data_medium.copy())
    print(f"\nMedium (1,000 elements):")
    print(f"  Time: {metrics_medium['execution_time_ms']:.3f} ms")
    print(f"  Memory: {metrics_medium['memory_peak_kb']:.2f} KB")
    
    # Large dataset
    data_large = [random.randint(1, 10000) for _ in range(10000)]
    _, metrics_large = timer.measure(heap_sort, data_large.copy())
    print(f"\nLarge (10,000 elements):")
    print(f"  Time: {metrics_large['execution_time_ms']:.3f} ms")
    print(f"  Memory: {metrics_large['memory_peak_kb']:.2f} KB")
    print()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(n log n) - all cases")
    print("  Space: O(1) - in-place (O(log n) recursion stack)")
    print("  Stable: No - relative order not preserved")
    print("  Adaptive: No - always O(n log n)")
    print("\nKey Advantages:")
    print("  - Guaranteed O(n log n) performance")
    print("  - In-place sorting (O(1) auxiliary space)")
    print("  - No worst-case quadratic time")
    print("  - Good for memory-constrained systems")
    print("\nKey Disadvantages:")
    print("  - Not stable")
    print("  - Not cache-friendly")
    print("  - Slower than quick sort in practice")
    print("  - Not adaptive")
    print("=" * 70)


if __name__ == "__main__":
    main()
