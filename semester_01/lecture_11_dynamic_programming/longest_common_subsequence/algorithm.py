#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Longest Common Subsequence implementation.

This file contains the implementation of the Longest Common Subsequence algorithm.
"""

from typing import List, Optional, Dict, Set


def longest_common_subsequence(s1: str, s2: str) -> int:
    """Longest Common Subsequence using dynamic programming."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def main() -> None:
    """Demonstrate Longest Common Subsequence."""
    print("=" * 70)
    print("LONGEST COMMON SUBSEQUENCE")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Longest Common Subsequence")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
