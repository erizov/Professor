#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Heap Sort implementation.

This file contains the implementation of the Heap Sort algorithm.
"""

from typing import List, Optional, Dict, Set


def heap_sort(arr: List[int]) -> List[int]:
    """Heap sort algorithm."""
    def heapify(arr: List[int], n: int, i: int) -> None:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr


def main() -> None:
    """Demonstrate Heap Sort."""
    print("=" * 70)
    print("HEAP SORT")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Heap Sort")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
