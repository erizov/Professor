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
    print("=" * 70)
    print("EDIT DISTANCE (LEVENSHTEIN DISTANCE) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic edit distance
    print("Example 1: Basic Edit Distance")
    print("-" * 70)
    
    test_cases = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("horse", "ros"),
        ("intention", "execution"),
    ]
    
    for s1, s2 in test_cases:
        distance = edit_distance(s1, s2)
        print(f"'{s1}' -> '{s2}': {distance} operations")
    print()
    
    # Example 2: Edit operations
    print("Example 2: Edit Operations")
    print("-" * 70)
    
    s1, s2 = "kitten", "sitting"
    distance = edit_distance(s1, s2)
    operations = edit_operations(s1, s2)
    
    print(f"'{s1}' -> '{s2}' (distance: {distance}):")
    for i, op in enumerate(operations, 1):
        print(f"  {i}. {op}")
    print()
    
    # Example 3: Similarity
    print("Example 3: String Similarity")
    print("-" * 70)
    
    pairs = [
        ("hello", "hello"),
        ("hello", "hallo"),
        ("hello", "world"),
        ("algorithm", "alogrithm"),
    ]
    
    for s1, s2 in pairs:
        sim = similarity(s1, s2)
        dist = edit_distance(s1, s2)
        print(f"'{s1}' vs '{s2}':")
        print(f"  Distance: {dist}, Similarity: {sim:.2%}")
    print()
    
    # Example 4: Spell checking simulation
    print("Example 4: Spell Checking Simulation")
    print("-" * 70)
    
    dictionary = ["hello", "world", "python", "algorithm", "computer"]
    word = "algoritm"
    
    print(f"Checking word: '{word}'")
    print("Suggestions (sorted by edit distance):")
    
    suggestions = []
    for dict_word in dictionary:
        dist = edit_distance(word, dict_word)
        suggestions.append((dict_word, dist))
    
    suggestions.sort(key=lambda x: x[1])
    for word_suggest, dist in suggestions[:3]:
        print(f"  '{word_suggest}' (distance: {dist})")
    print()
    
    # Example 5: Performance measurement
    print("Example 5: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Edit Distance")
    
    test_strings = [
        ("abcdefghij", "abcdefghij"),
        ("abcdefghijklmnop", "abcdefghijklmnop"),
        ("abcdefghijklmnopqrstuvwxyz", "abcdefghijklmnopqrstuvwxyz"),
    ]
    
    for s1, s2 in test_strings:
        _, metrics = timer.measure(edit_distance, s1, s2)
        print(f"Strings of length {len(s1)}:")
        print(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        print(f"  Distance: {edit_distance(s1, s2)}")
    
    print()
    
    # Example 6: Space-optimized version
    print("Example 6: Space-Optimized Version")
    print("-" * 70)
    
    s1, s2 = "saturday", "sunday"
    dist_standard = edit_distance(s1, s2)
    dist_optimized = edit_distance_optimized(s1, s2)
    
    print(f"'{s1}' -> '{s2}':")
    print(f"  Standard: {dist_standard}")
    print(f"  Optimized: {dist_optimized}")
    print("Note: Optimized uses O(min(m,n)) space instead of O(m*n)")
    print()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(m * n) - m and n are string lengths")
    print("  Space: O(m * n) - standard")
    print("        O(min(m, n)) - optimized")
    print("\nKey Advantages:")
    print("  - Optimal solution")
    print("  - Can be space-optimized")
    print("  - Can reconstruct operations")
    print("  - Useful for many applications")
    print("\nKey Disadvantages:")
    print("  - Quadratic time complexity")
    print("  - Not suitable for very long strings")
    print("  - Standard version uses O(m*n) space")
    print("\nWhen to Use:")
    print("  - Spell checking")
    print("  - DNA sequence alignment")
    print("  - Fuzzy string matching")
    print("  - Autocorrect systems")
    print("  - Plagiarism detection")
    print("\nCommon Use Cases:")
    print("  - Spell checkers")
    print("  - Autocorrect")
    print("  - DNA sequence comparison")
    print("  - Fuzzy search")
    print("  - String similarity")
    print("=" * 70)


if __name__ == "__main__":
    main()

