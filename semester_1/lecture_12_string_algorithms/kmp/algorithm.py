#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knuth-Morris-Pratt (KMP) Algorithm.

Efficient string pattern matching using failure function (LPS array).
Avoids re-checking characters that have already been matched.
"""

import sys
from pathlib import Path
from typing import List

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


def compute_lps(pattern: str) -> List[int]:
    """
    Compute Longest Proper Prefix which is also Suffix (LPS) array.
    
    Args:
        pattern: Pattern string
        
    Returns:
        LPS array
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # Length of previous longest prefix suffix
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Search for pattern in text using KMP algorithm.
    
    Args:
        text: Text to search in
        pattern: Pattern to search for
        
    Returns:
        List of starting indices where pattern is found
    """
    n = len(text)
    m = len(pattern)
    
    if m == 0:
        return []
    if m > n:
        return []
    
    lps = compute_lps(pattern)
    result = []
    
    i = 0  # Index for text
    j = 0  # Index for pattern
    
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            # Pattern found
            result.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            # Mismatch after j matches
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return result


def kmp_count(text: str, pattern: str) -> int:
    """
    Count occurrences of pattern in text.
    
    Args:
        text: Text to search in
        pattern: Pattern to search for
        
    Returns:
        Number of occurrences
    """
    return len(kmp_search(text, pattern))


def main() -> None:
    """Demonstration of KMP Algorithm."""
    print("=" * 70)
    print("KNUTH-MORRIS-PRATT (KMP) ALGORITHM DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic pattern matching
    print("Example 1: Basic Pattern Matching")
    print("-" * 70)
    
    text1 = "ABABDABACDABABCABCABAB"
    pattern1 = "ABABCABAB"
    
    matches = kmp_search(text1, pattern1)
    print(f"Text: {text1}")
    print(f"Pattern: {pattern1}")
    print(f"Matches found at indices: {matches}")
    print(f"Number of occurrences: {len(matches)}")
    print()
    
    # Example 2: Multiple occurrences
    print("Example 2: Multiple Occurrences")
    print("-" * 70)
    
    text2 = "AABAACAADAABAABA"
    pattern2 = "AABA"
    
    matches2 = kmp_search(text2, pattern2)
    print(f"Text: {text2}")
    print(f"Pattern: {pattern2}")
    print(f"Matches found at indices: {matches2}")
    print()
    
    # Example 3: LPS array visualization
    print("Example 3: LPS Array (Failure Function)")
    print("-" * 70)
    
    patterns = ["AAAA", "ABCDE", "AABAACAABAA", "AAACAAAAAC"]
    
    for pattern in patterns:
        lps = compute_lps(pattern)
        print(f"Pattern: {pattern}")
        print(f"LPS:     {lps}")
        print()
    
    # Example 4: No match
    print("Example 4: Pattern Not Found")
    print("-" * 70)
    
    text4 = "ABCDEFGHIJKLMNOP"
    pattern4 = "XYZ"
    
    matches4 = kmp_search(text4, pattern4)
    print(f"Text: {text4}")
    print(f"Pattern: {pattern4}")
    print(f"Matches: {matches4}")
    print("Pattern not found in text")
    print()
    
    # Example 5: Performance comparison
    print("Example 5: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("KMP")
    
    # Generate test data
    text_large = "A" * 1000 + "B" * 1000 + "A" * 1000
    pattern_large = "A" * 10 + "B" * 10
    
    def naive_search(text: str, pattern: str) -> List[int]:
        """Naive string search for comparison."""
        n, m = len(text), len(pattern)
        result = []
        for i in range(n - m + 1):
            if text[i:i + m] == pattern:
                result.append(i)
        return result
    
    # KMP
    _, metrics_kmp = timer.measure(kmp_search, text_large, pattern_large)
    print(f"KMP Algorithm:")
    print(f"  Time: {metrics_kmp['execution_time_ms']:.3f} ms")
    
    # Naive (for comparison)
    _, metrics_naive = timer.measure(naive_search, text_large, pattern_large)
    print(f"\nNaive Algorithm:")
    print(f"  Time: {metrics_naive['execution_time_ms']:.3f} ms")
    print(f"\nKMP is {metrics_naive['execution_time_ms'] / metrics_kmp['execution_time_ms']:.1f}x faster")
    print()
    
    # Example 6: Real-world application
    print("Example 6: Real-world Application - Text Search")
    print("-" * 70)
    
    document = "The quick brown fox jumps over the lazy dog. " * 10
    search_term = "fox"
    
    positions = kmp_search(document, search_term)
    print(f"Searching for '{search_term}' in document:")
    print(f"Found at positions: {positions}")
    print(f"Total occurrences: {len(positions)}")
    print()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Preprocessing (LPS): O(m) - m is pattern length")
    print("  Searching: O(n) - n is text length")
    print("  Total: O(n + m)")
    print("  Space: O(m) - for LPS array")
    print("\nKey Advantages:")
    print("  - Linear time complexity")
    print("  - No backtracking in text")
    print("  - Efficient for repeated patterns")
    print("  - Better than naive O(n*m)")
    print("\nKey Disadvantages:")
    print("  - More complex than naive algorithm")
    print("  - Requires preprocessing")
    print("  - Extra space for LPS array")
    print("\nWhen to Use:")
    print("  - Text search in large documents")
    print("  - Pattern matching in strings")
    print("  - DNA sequence matching")
    print("  - Multiple pattern searches")
    print("  - When pattern has repetitions")
    print("\nWhen NOT to Use:")
    print("  - Very short patterns (naive is simpler)")
    print("  - One-time search (preprocessing overhead)")
    print("  - Random text (naive might be faster)")
    print("\nCommon Use Cases:")
    print("  - Text editors (find/replace)")
    print("  - Search engines")
    print("  - DNA sequence analysis")
    print("  - Compiler string matching")
    print("  - Network packet inspection")
    print("\nComparison with Other Algorithms:")
    print("  - Naive: O(n*m) - simple but slow")
    print("  - KMP: O(n+m) - efficient, no backtracking")
    print("  - Rabin-Karp: O(n+m) average - hash-based")
    print("  - Boyer-Moore: O(n/m) best case - skip characters")
    print("=" * 70)


if __name__ == "__main__":
    main()

