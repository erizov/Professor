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
    print("=" * 70)
    print("LONGEST COMMON SUBSEQUENCE (LCS) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic LCS
    print("Example 1: Basic LCS")
    print("-" * 70)
    
    s1 = "ABCDGH"
    s2 = "AEDFHR"
    
    length = lcs_length(s1, s2)
    sequence = lcs_sequence(s1, s2)
    
    print(f"String 1: {s1}")
    print(f"String 2: {s2}")
    print(f"LCS Length: {length}")
    print(f"LCS Sequence: {sequence}")
    print()
    
    # Example 2: Another example
    print("Example 2: Another Example")
    print("-" * 70)
    
    s3 = "AGGTAB"
    s4 = "GXTXAYB"
    
    length2 = lcs_length(s3, s4)
    sequence2 = lcs_sequence(s3, s4)
    
    print(f"String 1: {s3}")
    print(f"String 2: {s4}")
    print(f"LCS Length: {length2}")
    print(f"LCS Sequence: {sequence2}")
    print()
    
    # Example 3: DNA sequence comparison
    print("Example 3: DNA Sequence Comparison")
    print("-" * 70)
    
    dna1 = "ACGTACGT"
    dna2 = "ACCTACGT"
    
    lcs_dna = lcs_sequence(dna1, dna2)
    print(f"DNA Sequence 1: {dna1}")
    print(f"DNA Sequence 2: {dna2}")
    print(f"LCS: {lcs_dna}")
    print(f"Similarity: {len(lcs_dna) / max(len(dna1), len(dna2)) * 100:.1f}%")
    print()
    
    # Example 4: Space-optimized version
    print("Example 4: Space-Optimized Version")
    print("-" * 70)
    
    s5 = "ABCDEFGHIJKLMNOP"
    s6 = "ACEGIKMOQ"
    
    length_standard = lcs_length(s5, s6)
    length_optimized = lcs_optimized(s5, s6)
    
    print(f"String 1: {s5}")
    print(f"String 2: {s6}")
    print(f"LCS Length (standard): {length_standard}")
    print(f"LCS Length (optimized): {length_optimized}")
    print("Note: Optimized version uses O(min(m,n)) space instead of O(m*n)")
    print()
    
    # Example 5: All LCS sequences
    print("Example 5: All LCS Sequences")
    print("-" * 70)
    
    s7 = "ABCBDAB"
    s8 = "BDCABA"
    
    all_lcs = lcs_all_sequences(s7, s8)
    print(f"String 1: {s7}")
    print(f"String 2: {s8}")
    print(f"LCS Length: {lcs_length(s7, s8)}")
    print(f"All LCS sequences: {all_lcs}")
    print()
    
    # Example 6: Performance measurement
    print("Example 6: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("LCS")
    
    test_cases = [
        ("ABCDEFGHIJ", "ACEGIKMOQ"),
        ("ABCDEFGHIJKLMNOP", "ACEGIKMOQSUWY"),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ACEGIKMOQSUWYACE"),
    ]
    
    for s1, s2 in test_cases:
        _, metrics = timer.measure(lcs_length, s1, s2)
        print(f"Strings of length {len(s1)} and {len(s2)}:")
        print(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        print(f"  LCS Length: {lcs_length(s1, s2)}")
    
    print()
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(m * n) - m and n are string lengths")
    print("  Space: O(m * n) - standard")
    print("        O(min(m, n)) - optimized")
    print("\nKey Advantages:")
    print("  - Efficient dynamic programming solution")
    print("  - Can be space-optimized")
    print("  - Handles sequences of any type")
    print("  - Can find all LCS sequences")
    print("\nKey Disadvantages:")
    print("  - Quadratic time complexity")
    print("  - Not suitable for very long sequences")
    print("  - Standard version uses O(m*n) space")
    print("\nWhen to Use:")
    print("  - String similarity comparison")
    print("  - DNA sequence alignment")
    print("  - Version control (diff algorithms)")
    print("  - Plagiarism detection")
    print("  - Text comparison")
    print("\nCommon Use Cases:")
    print("  - Git diff algorithm")
    print("  - DNA sequence alignment")
    print("  - Spell checkers")
    print("  - File comparison tools")
    print("  - Bioinformatics")
    print("\nVariations:")
    print("  - Longest Common Substring (contiguous)")
    print("  - Edit Distance (Levenshtein)")
    print("  - Longest Increasing Subsequence")
    print("=" * 70)


if __name__ == "__main__":
    main()

