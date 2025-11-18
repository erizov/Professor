#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strategy implementation.

This file contains the implementation of the Strategy algorithm.
"""

from typing import List, Optional, Dict, Set


class Strategy:
    """Strategy interface."""
    def execute(self, data: List[int]) -> List[int]:
        pass

class BubbleSortStrategy(Strategy):
    """Bubble sort strategy."""
    def execute(self, data: List[int]) -> List[int]:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

class QuickSortStrategy(Strategy):
    """Quick sort strategy."""
    def execute(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return QuickSortStrategy().execute(left) + middle + QuickSortStrategy().execute(right)

class Context:
    """Context that uses strategy."""
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy: Strategy) -> None:
        """Set strategy."""
        self.strategy = strategy
    
    def execute_strategy(self, data: List[int]) -> List[int]:
        """Execute strategy."""
        return self.strategy.execute(data)


def main() -> None:
    """Demonstrate Strategy."""
    print("=" * 70)
    print("STRATEGY")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Strategy")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
