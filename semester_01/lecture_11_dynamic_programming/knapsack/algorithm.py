#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knapsack implementation.

This file contains the implementation of the Knapsack algorithm.
"""

from typing import List, Optional, Dict, Set


def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """0/1 Knapsack problem using dynamic programming."""
    n = len(weights)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


def main() -> None:
    """Demonstrate Knapsack."""
    print("=" * 70)
    print("KNAPSACK")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Knapsack")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
