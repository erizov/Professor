#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jump Search implementation.

This file contains the implementation of the Jump Search algorithm.
"""

from typing import List, Dict, Set


def jump_search(arr: List[int], target: int) -> int:
    """Jump search algorithm."""
    n = len(arr)
    if n == 0:
        return -1

    step = int(n**0.5)
    prev = 0

    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(n**0.5)
        if prev >= n:
            return -1

    for i in range(prev, min(step, n)):
        if arr[i] == target:
            return i
    return -1


def main() -> None:
    """Demonstrate Jump Search."""
    print("=" * 70)
    print("JUMP SEARCH")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Jump Search")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
