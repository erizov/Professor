#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edit Distance implementation.

This file contains the implementation of the Edit Distance algorithm.
"""

from typing import List, Optional, Dict, Set


def edit_distance(s1: str, s2: str) -> int:
    """Edit distance (Levenshtein distance) using dynamic programming."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # deletion
                    dp[i][j - 1],  # insertion
                    dp[i - 1][j - 1],  # substitution
                )

    return dp[m][n]


def main() -> None:
    """Demonstrate Edit Distance."""
    print("=" * 70)
    print("EDIT DISTANCE")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Edit Distance")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
