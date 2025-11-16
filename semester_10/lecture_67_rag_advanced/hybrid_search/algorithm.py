#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hybrid Search implementation.
"""

from typing import List, Optional, Any
from framework.logging_utils import get_logger
import logging

logger = get_logger(__name__)

def hybrid_search(arr: List[Any], target: Any) -> Optional[int]:
    """
    Hybrid Search.
    
    Args:
        arr: List to search
        target: Target value
        
    Returns:
        Index if found, None otherwise
        
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    for i, item in enumerate(arr):
        if item == target:
            return i
    return None

def main():
    """Demonstration."""
    print("=" * 70)
    print(f"Hybrid Search")
    print("=" * 70)
    
    # Example usage
    example_data = [1, 2, 3, 4, 5]
    result = hybrid_search(example_data)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
