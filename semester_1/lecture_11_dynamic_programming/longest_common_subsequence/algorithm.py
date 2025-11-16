#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Longest Common Subsequence (LCS) - Dynamic Programming.

Finds the longest subsequence common to two sequences.
A subsequence is a sequence that appears in the same relative order,
but not necessarily contiguous.
"""

import sys
from pathlib import Path
from typing import List, Tuple

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


def lcs_length(s1: str, s2: str) -> int:
    """
    Find length of longest common subsequence.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Length of LCS
        
    Time Complexity: O(m * n)
    Space Complexity: O(m * n)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


def lcs_sequence(s1: str, s2: str) -> str:
    """
    Find longest common subsequence string.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        LCS string
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Build DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Reconstruct LCS
    lcs = []
    i, j = m, n
    
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return ''.join(reversed(lcs))


def lcs_optimized(s1: str, s2: str) -> int:
    """
    Space-optimized LCS (only length).
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Length of LCS
        
    Space Complexity: O(min(m, n))
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    
    m, n = len(s1), len(s2)
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, prev
    
    return prev[n]


def lcs_all_sequences(s1: str, s2: str) -> List[str]:
    """
    Find all longest common subsequences.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        List of all LCS strings
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Build DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Find all LCS using backtracking
    def backtrack(i: int, j: int) -> List[str]:
        if i == 0 or j == 0:
            return ['']
        
        if s1[i - 1] == s2[j - 1]:
            result = []
            for seq in backtrack(i - 1, j - 1):
                result.append(seq + s1[i - 1])
            return result
        else:
            result = []
            if dp[i - 1][j] >= dp[i][j - 1]:
                result.extend(backtrack(i - 1, j))
            if dp[i][j - 1] >= dp[i - 1][j]:
                result.extend(backtrack(i, j - 1))
            return list(set(result))  # Remove duplicates
    
    return backtrack(m, n)


def main() -> None:
    """Demonstration of LCS algorithm."""
    logger.info("=" * 70)
    logger.info("LONGEST COMMON SUBSEQUENCE (LCS) DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic LCS
    logger.info("Example 1: Basic LCS")
    logger.info("-" * 70)
    
    s1 = "ABCDGH"
    s2 = "AEDFHR"
    
    length = lcs_length(s1, s2)
    sequence = lcs_sequence(s1, s2)
    
    logger.info(f"String 1: {s1}")
    logger.info(f"String 2: {s2}")
    logger.info(f"LCS Length: {length}")
    logger.info(f"LCS Sequence: {sequence}")
    logger.info()
    
    # Example 2: Another example
    logger.info("Example 2: Another Example")
    logger.info("-" * 70)
    
    s3 = "AGGTAB"
    s4 = "GXTXAYB"
    
    length2 = lcs_length(s3, s4)
    sequence2 = lcs_sequence(s3, s4)
    
    logger.info(f"String 1: {s3}")
    logger.info(f"String 2: {s4}")
    logger.info(f"LCS Length: {length2}")
    logger.info(f"LCS Sequence: {sequence2}")
    logger.info()
    
    # Example 3: DNA sequence comparison
    logger.info("Example 3: DNA Sequence Comparison")
    logger.info("-" * 70)
    
    dna1 = "ACGTACGT"
    dna2 = "ACCTACGT"
    
    lcs_dna = lcs_sequence(dna1, dna2)
    logger.info(f"DNA Sequence 1: {dna1}")
    logger.info(f"DNA Sequence 2: {dna2}")
    logger.info(f"LCS: {lcs_dna}")
    logger.info(f"Similarity: {len(lcs_dna) / max(len(dna1), len(dna2)) * 100:.1f}%")
    logger.info()
    
    # Example 4: Space-optimized version
    logger.info("Example 4: Space-Optimized Version")
    logger.info("-" * 70)
    
    s5 = "ABCDEFGHIJKLMNOP"
    s6 = "ACEGIKMOQ"
    
    length_standard = lcs_length(s5, s6)
    length_optimized = lcs_optimized(s5, s6)
    
    logger.info(f"String 1: {s5}")
    logger.info(f"String 2: {s6}")
    logger.info(f"LCS Length (standard): {length_standard}")
    logger.info(f"LCS Length (optimized): {length_optimized}")
    logger.info("Note: Optimized version uses O(min(m,n)) space instead of O(m*n)")
    logger.info()
    
    # Example 5: All LCS sequences
    logger.info("Example 5: All LCS Sequences")
    logger.info("-" * 70)
    
    s7 = "ABCBDAB"
    s8 = "BDCABA"
    
    all_lcs = lcs_all_sequences(s7, s8)
    logger.info(f"String 1: {s7}")
    logger.info(f"String 2: {s8}")
    logger.info(f"LCS Length: {lcs_length(s7, s8)}")
    logger.info(f"All LCS sequences: {all_lcs}")
    logger.info()
    
    # Example 6: Performance measurement
    logger.info("Example 6: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("LCS")
    
    test_cases = [
        ("ABCDEFGHIJ", "ACEGIKMOQ"),
        ("ABCDEFGHIJKLMNOP", "ACEGIKMOQSUWY"),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ACEGIKMOQSUWYACE"),
    ]
    
    for s1, s2 in test_cases:
        _, metrics = timer.measure(lcs_length, s1, s2)
        logger.info(f"Strings of length {len(s1)} and {len(s2)}:")
        logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        logger.info(f"  LCS Length: {lcs_length(s1, s2)}")
    
    logger.info()
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(m * n) - m and n are string lengths")
    logger.info("  Space: O(m * n) - standard")
    logger.info("        O(min(m, n)) - optimized")
    logger.info("\nKey Advantages:")
    logger.info("  - Efficient dynamic programming solution")
    logger.info("  - Can be space-optimized")
    logger.info("  - Handles sequences of any type")
    logger.info("  - Can find all LCS sequences")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Quadratic time complexity")
    logger.info("  - Not suitable for very long sequences")
    logger.info("  - Standard version uses O(m*n) space")
    logger.info("\nWhen to Use:")
    logger.info("  - String similarity comparison")
    logger.info("  - DNA sequence alignment")
    logger.info("  - Version control (diff algorithms)")
    logger.info("  - Plagiarism detection")
    logger.info("  - Text comparison")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Git diff algorithm")
    logger.info("  - DNA sequence alignment")
    logger.info("  - Spell checkers")
    logger.info("  - File comparison tools")
    logger.info("  - Bioinformatics")
    logger.info("\nVariations:")
    logger.info("  - Longest Common Substring (contiguous)")
    logger.info("  - Edit Distance (Levenshtein)")
    logger.info("  - Longest Increasing Subsequence")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()