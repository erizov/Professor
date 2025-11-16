#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insertion Sort implementation."""

from typing import List, TypeVar
from framework.logging_utils import get_logger
logger = get_logger(__name__)

T = TypeVar('T')


def insertion_sort(arr: List[T]) -> List[T]:
    """
    Sort array using insertion sort.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list
        
    Time: O(n²) worst, O(n) best, Space: O(1)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Move elements greater than key one position ahead
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr


def main():
    """Demonstration."""
    logger.info("=" * 70)
    logger.info("INSERTION SORT")
    logger.info("=" * 70)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    logger.info(f"Original: {data}")
    result = insertion_sort(data.copy())
    logger.info(f"Sorted:   {result}")
    
    logger.info("\nComplexity: O(n²) worst, O(n) best, O(1) space")


if __name__ == "__main__":
    main()