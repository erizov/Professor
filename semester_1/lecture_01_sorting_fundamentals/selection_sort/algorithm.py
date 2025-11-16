#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Selection Sort implementation."""

from typing import List, TypeVar
from framework.logging_utils import get_logger
import logging

logger = get_logger(__name__)

T = TypeVar('T')


def selection_sort(arr: List[T]) -> List[T]:
    """
    Sort array using selection sort.
    
    Args:
        arr: List to be sorted
        
    Returns:
        Sorted list (modifies in-place)
        
    Time: O(n²), Space: O(1)
    """
    n = len(arr)
    
    for i in range(n):
        # Find minimum element in remaining array
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap minimum element with first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr


def main():
    """Demonstration."""
    logger.info("=" * 70)
    logger.info("SELECTION SORT")
    logger.info("=" * 70)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    logger.info(f"Original: {data}")
    result = selection_sort(data.copy())
    logger.info(f"Sorted:   {result}")
    
    logger.info("\nComplexity: O(n²) time, O(1) space")
    try:
            """Demonstration."""
            logger.info("=" * 70)
            logger.info("SELECTION SORT")
            logger.info("=" * 70)
            
            data = [64, 34, 25, 12, 22, 11, 90]
            logger.info(f"Original: {data}")
            result = selection_sort(data.copy())
            logger.info(f"Sorted:   {result}")
            
            logger.info("\nComplexity: O(n²) time, O(1) space")
        
        
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()