#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dynamic Programming - Demonstration.

This lecture covers dynamic programming algorithms including
Fibonacci, knapsack, and longest common subsequence.
"""


def fibonacci(n: int) -> int:
    """Fibonacci using dynamic programming."""
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


def main() -> None:
    """Demonstrate dynamic programming."""
    print("=" * 70)
    print("DYNAMIC PROGRAMMING")
    print("=" * 70)
    
    n = 10
    result = fibonacci(n)
    print(f"Fibonacci({n}) = {result}")
    print("=" * 70)


if __name__ == "__main__":
    main()
