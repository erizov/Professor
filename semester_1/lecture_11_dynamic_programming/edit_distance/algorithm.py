#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edit Distance (Levenshtein Distance) - Dynamic Programming.

Minimum number of single-character edits (insertions, deletions,
substitutions) required to change one word into another.
"""

import sys
from pathlib import Path
from typing import List, Tuple

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


def edit_distance(s1: str, s2: str) -> int:
    """
    Calculate edit distance (Levenshtein distance).
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Edit distance (minimum operations needed)
        
    Time Complexity: O(m * n)
    Space Complexity: O(m * n)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters from s1
    
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters from s2
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters match, no operation needed
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Take minimum of three operations
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )
    
    return dp[m][n]


def edit_distance_optimized(s1: str, s2: str) -> int:
    """
    Space-optimized edit distance.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Edit distance
        
    Space Complexity: O(min(m, n))
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    
    m, n = len(s1), len(s2)
    prev = list(range(n + 1))
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev, curr = curr, prev
    
    return prev[n]


def edit_operations(s1: str, s2: str) -> List[str]:
    """
    Get sequence of edit operations.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        List of operations
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Build DP table
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], 
                                  dp[i - 1][j - 1])
    
    # Reconstruct operations
    operations = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            operations.append(f"Replace '{s1[i - 1]}' with '{s2[j - 1]}'")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            operations.append(f"Delete '{s1[i - 1]}'")
            i -= 1
        else:
            operations.append(f"Insert '{s2[j - 1]}'")
            j -= 1
    
    return list(reversed(operations))


def similarity(s1: str, s2: str) -> float:
    """
    Calculate similarity percentage.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Similarity (0.0 to 1.0)
    """
    if not s1 and not s2:
        return 1.0
    
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    
    distance = edit_distance(s1, s2)
    return 1.0 - (distance / max_len)


def main() -> None:
    """Demonstration of Edit Distance Algorithm."""
    logger.info("=" * 70)
    logger.info("EDIT DISTANCE (LEVENSHTEIN DISTANCE) DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic edit distance
    logger.info("Example 1: Basic Edit Distance")
    logger.info("-" * 70)
    
    test_cases = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("horse", "ros"),
        ("intention", "execution"),
    ]
    
    for s1, s2 in test_cases:
        distance = edit_distance(s1, s2)
        logger.info(f"'{s1}' -> '{s2}': {distance} operations")
    logger.info()
    
    # Example 2: Edit operations
    logger.info("Example 2: Edit Operations")
    logger.info("-" * 70)
    
    s1, s2 = "kitten", "sitting"
    distance = edit_distance(s1, s2)
    operations = edit_operations(s1, s2)
    
    logger.info(f"'{s1}' -> '{s2}' (distance: {distance}):")
    for i, op in enumerate(operations, 1):
        logger.info(f"  {i}. {op}")
    logger.info()
    
    # Example 3: Similarity
    logger.info("Example 3: String Similarity")
    logger.info("-" * 70)
    
    pairs = [
        ("hello", "hello"),
        ("hello", "hallo"),
        ("hello", "world"),
        ("algorithm", "alogrithm"),
    ]
    
    for s1, s2 in pairs:
        sim = similarity(s1, s2)
        dist = edit_distance(s1, s2)
        logger.info(f"'{s1}' vs '{s2}':")
        logger.info(f"  Distance: {dist}, Similarity: {sim:.2%}")
    logger.info()
    
    # Example 4: Spell checking simulation
    logger.info("Example 4: Spell Checking Simulation")
    logger.info("-" * 70)
    
    dictionary = ["hello", "world", "python", "algorithm", "computer"]
    word = "algoritm"
    
    logger.info(f"Checking word: '{word}'")
    logger.info("Suggestions (sorted by edit distance):")
    
    suggestions = []
    for dict_word in dictionary:
        dist = edit_distance(word, dict_word)
        suggestions.append((dict_word, dist))
    
    suggestions.sort(key=lambda x: x[1])
    for word_suggest, dist in suggestions[:3]:
        logger.info(f"  '{word_suggest}' (distance: {dist})")
    logger.info()
    
    # Example 5: Performance measurement
    logger.info("Example 5: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Edit Distance")
    
    test_strings = [
        ("abcdefghij", "abcdefghij"),
        ("abcdefghijklmnop", "abcdefghijklmnop"),
        ("abcdefghijklmnopqrstuvwxyz", "abcdefghijklmnopqrstuvwxyz"),
    ]
    
    for s1, s2 in test_strings:
        _, metrics = timer.measure(edit_distance, s1, s2)
        logger.info(f"Strings of length {len(s1)}:")
        logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        logger.info(f"  Distance: {edit_distance(s1, s2)}")
    
    logger.info()
    
    # Example 6: Space-optimized version
    logger.info("Example 6: Space-Optimized Version")
    logger.info("-" * 70)
    
    s1, s2 = "saturday", "sunday"
    dist_standard = edit_distance(s1, s2)
    dist_optimized = edit_distance_optimized(s1, s2)
    
    logger.info(f"'{s1}' -> '{s2}':")
    logger.info(f"  Standard: {dist_standard}")
    logger.info(f"  Optimized: {dist_optimized}")
    logger.info("Note: Optimized uses O(min(m,n)) space instead of O(m*n)")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(m * n) - m and n are string lengths")
    logger.info("  Space: O(m * n) - standard")
    logger.info("        O(min(m, n)) - optimized")
    logger.info("\nKey Advantages:")
    logger.info("  - Optimal solution")
    logger.info("  - Can be space-optimized")
    logger.info("  - Can reconstruct operations")
    logger.info("  - Useful for many applications")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Quadratic time complexity")
    logger.info("  - Not suitable for very long strings")
    logger.info("  - Standard version uses O(m*n) space")
    logger.info("\nWhen to Use:")
    logger.info("  - Spell checking")
    logger.info("  - DNA sequence alignment")
    logger.info("  - Fuzzy string matching")
    logger.info("  - Autocorrect systems")
    logger.info("  - Plagiarism detection")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Spell checkers")
    logger.info("  - Autocorrect")
    logger.info("  - DNA sequence comparison")
    logger.info("  - Fuzzy search")
    logger.info("  - String similarity")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()