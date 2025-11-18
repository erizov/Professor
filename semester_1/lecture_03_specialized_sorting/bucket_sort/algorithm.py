#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bucket Sort implementation.

This file contains the implementation of the Bucket Sort algorithm.
"""

from typing import List, Optional, Dict, Set


def bucket_sort(arr: List[float]) -> List[float]:
    """Bucket sort algorithm."""
    if not arr:
        return arr
    
    n = len(arr)
    buckets = [[] for _ in range(n)]
    
    for num in arr:
        bucket_idx = int(n * num)
        if bucket_idx == n:
            bucket_idx = n - 1
        buckets[bucket_idx].append(num)
    
    for bucket in buckets:
        bucket.sort()
    
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result


def main() -> None:
    """Demonstrate Bucket Sort."""
    print("=" * 70)
    print("BUCKET SORT")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Bucket Sort")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
