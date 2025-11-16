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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("=" * 70)
    logger.info("FIBONACCI SEQUENCE - DYNAMIC PROGRAMMING DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Compare different approaches
    logger.debug("Example 1: Comparing Different Approaches")
    logger.info("-" * 70)
    
    n = 10
    logger.info(f"Computing Fibonacci({n}):")
    
    logger.info(f"  Naive recursive: {fibonacci_naive(n)}")
    logger.info(f"  Memoized: {fibonacci_memoized(n)}")
    logger.info(f"  LRU Cache: {fibonacci_lru_cache(n)}")
    logger.info(f"  Bottom-up DP: {fibonacci_bottom_up(n)}")
    logger.info(f"  Optimized (O(1) space): {fibonacci_optimized(n)}")
    logger.info(f"  Matrix exponentiation: {fibonacci_matrix(n)}")
    logger.info()
    
    # Example 2: Performance comparison
    logger.info("Example 2: Performance Comparison")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Fibonacci")
    
    test_values = [20, 30, 35]
    
    for n_val in test_values:
        logger.info(f"\nComputing Fibonacci({n_val}):")
        
        # Naive (only for small n)
        if n_val <= 30:
            _, metrics_naive = timer.measure(fibonacci_naive, n_val)
            logger.info(f"  Naive: {metrics_naive['execution_time_ms']:.3f} ms")
        
        # Memoized
        fibonacci_memoized.cache_clear() if hasattr(fibonacci_memoized, 'cache_clear') else None
        _, metrics_memo = timer.measure(fibonacci_memoized, n_val)
        logger.info(f"  Memoized: {metrics_memo['execution_time_ms']:.3f} ms")
        
        # Bottom-up
        _, metrics_bottom = timer.measure(fibonacci_bottom_up, n_val)
        logger.info(f"  Bottom-up: {metrics_bottom['execution_time_ms']:.3f} ms")
        
        # Optimized
        _, metrics_opt = timer.measure(fibonacci_optimized, n_val)
        logger.info(f"  Optimized: {metrics_opt['execution_time_ms']:.3f} ms")
        
        # Matrix (for larger n)
        if n_val >= 30:
            _, metrics_matrix = timer.measure(fibonacci_matrix, n_val)
            logger.info(f"  Matrix: {metrics_matrix['execution_time_ms']:.3f} ms")
    logger.info()
    
    # Example 3: Generate sequence
    logger.info("Example 3: Generating Fibonacci Sequence")
    logger.info("-" * 70)
    
    sequence = fibonacci_sequence(15)
    logger.info(f"First 15 Fibonacci numbers:")
    logger.info(f"  {sequence}")
    logger.info()
    
    # Example 4: Large values
    logger.info("Example 4: Large Fibonacci Numbers")
    logger.info("-" * 70)
    
    large_n = [50, 100, 200]
    for n_val in large_n:
        result = fibonacci_optimized(n_val)
        logger.info(f"Fibonacci({n_val}) = {result}")
        logger.info(f"  (digits: {len(str(result))})")
    logger.info()
    
    # Example 5: Space complexity comparison
    logger.info("Example 5: Space Complexity Analysis")
    logger.info("-" * 70)
    
    logger.info("Space Complexity:")
    logger.info("  Naive recursive: O(n) - recursion stack")
    logger.info("  Memoized: O(n) - memoization table + stack")
    logger.info("  Bottom-up DP: O(n) - DP array")
    logger.info("  Optimized: O(1) - only two variables")
    logger.info("  Matrix: O(log n) - recursion depth")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Naive Recursive:")
    logger.info("    Time:  O(2^n) - exponential!")
    logger.info("    Space: O(n)")
    logger.info("  Memoized (Top-down DP):")
    logger.info("    Time:  O(n)")
    logger.info("    Space: O(n)")
    logger.info("  Bottom-up DP:")
    logger.info("    Time:  O(n)")
    logger.info("    Space: O(n)")
    logger.info("  Optimized:")
    logger.info("    Time:  O(n)")
    logger.info("    Space: O(1) - best space complexity")
    logger.info("  Matrix Exponentiation:")
    logger.info("    Time:  O(log n) - best time complexity")
    logger.info("    Space: O(log n)")
    logger.info("\nKey Advantages:")
    logger.info("  - Demonstrates DP concepts clearly")
    logger.info("  - Multiple optimization strategies")
    logger.info("  - Shows space-time trade-offs")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Naive approach is extremely slow")
    logger.info("  - Integer overflow for large n")
    logger.info("\nWhen to Use:")
    logger.info("  - Learning dynamic programming")
    logger.info("  - When Fibonacci numbers are needed")
    logger.info("  - Pattern matching problems")
    logger.info("  - Golden ratio applications")
    logger.info("\nOptimization Tips:")
    logger.info("  1. Always use memoization or bottom-up for production")
    logger.info("  2. Use optimized version for space-constrained systems")
    logger.info("  3. Use matrix exponentiation for very large n")
    logger.info("  4. Consider modulo arithmetic for huge numbers")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()