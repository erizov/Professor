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
from framework.logging_utils import get_logger
logger = get_logger(__name__)

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
    logger.info(f"Initial array: {arr}")
    logger.info()
    
    # Build max heap
    logger.info("Building max heap:")
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
        logger.info(f"  After heapifying at index {i}: {arr}")
    logger.info(f"Max heap built: {arr}")
    logger.info()
    
    # Extract elements
    logger.info("Extracting elements:")
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        logger.info(f"  Moved {arr[i]} to position {i}: {arr[:i]} | [{arr[i:]}]")
        heapify(arr, i, 0)
        logger.info(f"  After heapify: {arr[:i]} | [{arr[i:]}]")
    
    logger.info(f"\nFinal sorted array: {arr}")
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
    logger.info("=" * 70)
    logger.info("HEAP SORT DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic sorting
    logger.info("Example 1: Basic Integer Sorting")
    logger.info("-" * 70)
    data1 = [64, 34, 25, 12, 22, 11, 90]
    logger.info(f"Original: {data1}")
    result1 = heap_sort(data1.copy())
    logger.info(f"Sorted:   {result1}")
    logger.info()
    
    # Example 2: Already sorted
    logger.info("Example 2: Already Sorted Array")
    logger.info("-" * 70)
    data2 = [1, 2, 3, 4, 5, 6, 7]
    logger.info(f"Original: {data2}")
    result2 = heap_sort(data2.copy())
    logger.info(f"Sorted:   {result2}")
    logger.info("Note: Still O(n log n) - not adaptive")
    logger.info()
    
    # Example 3: Reverse sorted
    logger.info("Example 3: Reverse Sorted Array")
    logger.info("-" * 70)
    data3 = [7, 6, 5, 4, 3, 2, 1]
    logger.info(f"Original: {data3}")
    result3 = heap_sort(data3.copy())
    logger.info(f"Sorted:   {result3}")
    logger.info()
    
    # Example 4: Descending order
    logger.info("Example 4: Descending Order")
    logger.info("-" * 70)
    data4 = [64, 34, 25, 12, 22, 11, 90]
    logger.info(f"Original: {data4}")
    result4 = heap_sort_descending(data4.copy())
    logger.info(f"Sorted (desc): {result4}")
    logger.info()
    
    # Example 5: Visualization
    logger.info("Example 5: Visualized Heap Sort Process")
    logger.info("-" * 70)
    data5 = [12, 11, 13, 5, 6, 7]
    heap_sort_visualized(data5)
    logger.info()
    
    # Example 6: Performance measurement
    logger.info("Example 6: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Heap Sort")
    
    # Small dataset
    data_small = [random.randint(1, 100) for _ in range(100)]
    _, metrics_small = timer.measure(heap_sort, data_small.copy())
    logger.info(f"Small (100 elements):")
    logger.info(f"  Time: {metrics_small['execution_time_ms']:.3f} ms")
    logger.info(f"  Memory: {metrics_small['memory_peak_kb']:.2f} KB")
    
    # Medium dataset
    data_medium = [random.randint(1, 1000) for _ in range(1000)]
    _, metrics_medium = timer.measure(heap_sort, data_medium.copy())
    logger.info(f"\nMedium (1,000 elements):")
    logger.info(f"  Time: {metrics_medium['execution_time_ms']:.3f} ms")
    logger.info(f"  Memory: {metrics_medium['memory_peak_kb']:.2f} KB")
    
    # Large dataset
    data_large = [random.randint(1, 10000) for _ in range(10000)]
    _, metrics_large = timer.measure(heap_sort, data_large.copy())
    logger.info(f"\nLarge (10,000 elements):")
    logger.info(f"  Time: {metrics_large['execution_time_ms']:.3f} ms")
    logger.info(f"  Memory: {metrics_large['memory_peak_kb']:.2f} KB")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(n log n) - all cases")
    logger.info("  Space: O(1) - in-place (O(log n) recursion stack)")
    logger.info("  Stable: No - relative order not preserved")
    logger.info("  Adaptive: No - always O(n log n)")
    logger.info("\nKey Advantages:")
    logger.info("  - Guaranteed O(n log n) performance")
    logger.info("  - In-place sorting (O(1) auxiliary space)")
    logger.info("  - No worst-case quadratic time")
    logger.info("  - Good for memory-constrained systems")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Not stable")
    logger.info("  - Not cache-friendly")
    logger.info("  - Slower than quick sort in practice")
    logger.info("  - Not adaptive")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()