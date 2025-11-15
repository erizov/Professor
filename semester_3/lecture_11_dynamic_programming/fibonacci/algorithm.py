#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fibonacci Sequence - Dynamic Programming.

Multiple approaches: naive recursive, memoized, bottom-up DP, and optimized.
"""

import sys
from pathlib import Path
from functools import lru_cache
from typing import Dict

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


def fibonacci_naive(n: int) -> int:
    """
    Naive recursive Fibonacci (exponential time).
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        nth Fibonacci number
        
    Time Complexity: O(2^n)
    Space Complexity: O(n) - recursion stack
    """
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


def fibonacci_memoized(n: int, memo: Dict[int, int] = None) -> int:
    """
    Memoized recursive Fibonacci (top-down DP).
    
    Args:
        n: Position in Fibonacci sequence
        memo: Memoization dictionary
        
    Returns:
        nth Fibonacci number
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fibonacci_memoized(n - 1, memo) + \
              fibonacci_memoized(n - 2, memo)
    return memo[n]


@lru_cache(maxsize=None)
def fibonacci_lru_cache(n: int) -> int:
    """
    Fibonacci using Python's LRU cache decorator.
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        nth Fibonacci number
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if n <= 1:
        return n
    return fibonacci_lru_cache(n - 1) + fibonacci_lru_cache(n - 2)


def fibonacci_bottom_up(n: int) -> int:
    """
    Bottom-up dynamic programming Fibonacci.
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        nth Fibonacci number
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]


def fibonacci_optimized(n: int) -> int:
    """
    Space-optimized Fibonacci (only store last two values).
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        nth Fibonacci number
        
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if n <= 1:
        return n
    
    prev2 = 0  # F(0)
    prev1 = 1  # F(1)
    
    for i in range(2, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1


def fibonacci_matrix(n: int) -> int:
    """
    Fibonacci using matrix exponentiation (advanced).
    
    Uses the fact that [F(n+1), F(n)]^T = [[1,1],[1,0]]^n * [1,0]^T
    
    Args:
        n: Position in Fibonacci sequence
        
    Returns:
        nth Fibonacci number
        
    Time Complexity: O(log n)
    Space Complexity: O(log n) - recursion
    """
    def matrix_multiply(A: list, B: list) -> list:
        """Multiply two 2x2 matrices."""
        return [
            [A[0][0] * B[0][0] + A[0][1] * B[1][0],
             A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0],
             A[1][0] * B[0][1] + A[1][1] * B[1][1]]
        ]
    
    def matrix_power(matrix: list, power: int) -> list:
        """Compute matrix^power using exponentiation by squaring."""
        if power == 1:
            return matrix
        
        if power % 2 == 0:
            half = matrix_power(matrix, power // 2)
            return matrix_multiply(half, half)
        else:
            return matrix_multiply(matrix, 
                                  matrix_power(matrix, power - 1))
    
    if n <= 1:
        return n
    
    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(base_matrix, n)
    
    return result_matrix[0][1]


def fibonacci_sequence(n: int, method: str = 'optimized') -> list:
    """
    Generate first n Fibonacci numbers.
    
    Args:
        n: Number of Fibonacci numbers to generate
        method: Method to use ('optimized', 'bottom_up', etc.)
        
    Returns:
        List of first n Fibonacci numbers
    """
    if method == 'optimized':
        func = fibonacci_optimized
    elif method == 'bottom_up':
        func = fibonacci_bottom_up
    elif method == 'memoized':
        func = fibonacci_memoized
    else:
        func = fibonacci_optimized
    
    return [func(i) for i in range(n)]


def main() -> None:
    """Demonstration of Fibonacci implementations."""
    print("=" * 70)
    print("FIBONACCI SEQUENCE - DYNAMIC PROGRAMMING DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Compare different approaches
    print("Example 1: Comparing Different Approaches")
    print("-" * 70)
    
    n = 10
    print(f"Computing Fibonacci({n}):")
    
    print(f"  Naive recursive: {fibonacci_naive(n)}")
    print(f"  Memoized: {fibonacci_memoized(n)}")
    print(f"  LRU Cache: {fibonacci_lru_cache(n)}")
    print(f"  Bottom-up DP: {fibonacci_bottom_up(n)}")
    print(f"  Optimized (O(1) space): {fibonacci_optimized(n)}")
    print(f"  Matrix exponentiation: {fibonacci_matrix(n)}")
    print()
    
    # Example 2: Performance comparison
    print("Example 2: Performance Comparison")
    print("-" * 70)
    
    timer = PerformanceTimer("Fibonacci")
    
    test_values = [20, 30, 35]
    
    for n_val in test_values:
        print(f"\nComputing Fibonacci({n_val}):")
        
        # Naive (only for small n)
        if n_val <= 30:
            _, metrics_naive = timer.measure(fibonacci_naive, n_val)
            print(f"  Naive: {metrics_naive['execution_time_ms']:.3f} ms")
        
        # Memoized
        fibonacci_memoized.cache_clear() if hasattr(fibonacci_memoized, 'cache_clear') else None
        _, metrics_memo = timer.measure(fibonacci_memoized, n_val)
        print(f"  Memoized: {metrics_memo['execution_time_ms']:.3f} ms")
        
        # Bottom-up
        _, metrics_bottom = timer.measure(fibonacci_bottom_up, n_val)
        print(f"  Bottom-up: {metrics_bottom['execution_time_ms']:.3f} ms")
        
        # Optimized
        _, metrics_opt = timer.measure(fibonacci_optimized, n_val)
        print(f"  Optimized: {metrics_opt['execution_time_ms']:.3f} ms")
        
        # Matrix (for larger n)
        if n_val >= 30:
            _, metrics_matrix = timer.measure(fibonacci_matrix, n_val)
            print(f"  Matrix: {metrics_matrix['execution_time_ms']:.3f} ms")
    print()
    
    # Example 3: Generate sequence
    print("Example 3: Generating Fibonacci Sequence")
    print("-" * 70)
    
    sequence = fibonacci_sequence(15)
    print(f"First 15 Fibonacci numbers:")
    print(f"  {sequence}")
    print()
    
    # Example 4: Large values
    print("Example 4: Large Fibonacci Numbers")
    print("-" * 70)
    
    large_n = [50, 100, 200]
    for n_val in large_n:
        result = fibonacci_optimized(n_val)
        print(f"Fibonacci({n_val}) = {result}")
        print(f"  (digits: {len(str(result))})")
    print()
    
    # Example 5: Space complexity comparison
    print("Example 5: Space Complexity Analysis")
    print("-" * 70)
    
    print("Space Complexity:")
    print("  Naive recursive: O(n) - recursion stack")
    print("  Memoized: O(n) - memoization table + stack")
    print("  Bottom-up DP: O(n) - DP array")
    print("  Optimized: O(1) - only two variables")
    print("  Matrix: O(log n) - recursion depth")
    print()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Naive Recursive:")
    print("    Time:  O(2^n) - exponential!")
    print("    Space: O(n)")
    print("  Memoized (Top-down DP):")
    print("    Time:  O(n)")
    print("    Space: O(n)")
    print("  Bottom-up DP:")
    print("    Time:  O(n)")
    print("    Space: O(n)")
    print("  Optimized:")
    print("    Time:  O(n)")
    print("    Space: O(1) - best space complexity")
    print("  Matrix Exponentiation:")
    print("    Time:  O(log n) - best time complexity")
    print("    Space: O(log n)")
    print("\nKey Advantages:")
    print("  - Demonstrates DP concepts clearly")
    print("  - Multiple optimization strategies")
    print("  - Shows space-time trade-offs")
    print("\nKey Disadvantages:")
    print("  - Naive approach is extremely slow")
    print("  - Integer overflow for large n")
    print("\nWhen to Use:")
    print("  - Learning dynamic programming")
    print("  - When Fibonacci numbers are needed")
    print("  - Pattern matching problems")
    print("  - Golden ratio applications")
    print("\nOptimization Tips:")
    print("  1. Always use memoization or bottom-up for production")
    print("  2. Use optimized version for space-constrained systems")
    print("  3. Use matrix exponentiation for very large n")
    print("  4. Consider modulo arithmetic for huge numbers")
    print("=" * 70)


if __name__ == "__main__":
    main()

