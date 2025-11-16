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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("=" * 70)
    logger.info("KNUTH-MORRIS-PRATT (KMP) ALGORITHM DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic pattern matching
    logger.info("Example 1: Basic Pattern Matching")
    logger.info("-" * 70)
    
    text1 = "ABABDABACDABABCABCABAB"
    pattern1 = "ABABCABAB"
    
    matches = kmp_search(text1, pattern1)
    logger.info(f"Text: {text1}")
    logger.info(f"Pattern: {pattern1}")
    logger.info(f"Matches found at indices: {matches}")
    logger.info(f"Number of occurrences: {len(matches)}")
    logger.info()
    
    # Example 2: Multiple occurrences
    logger.info("Example 2: Multiple Occurrences")
    logger.info("-" * 70)
    
    text2 = "AABAACAADAABAABA"
    pattern2 = "AABA"
    
    matches2 = kmp_search(text2, pattern2)
    logger.info(f"Text: {text2}")
    logger.info(f"Pattern: {pattern2}")
    logger.info(f"Matches found at indices: {matches2}")
    logger.info()
    
    # Example 3: LPS array visualization
    logger.info("Example 3: LPS Array (Failure Function)")
    logger.info("-" * 70)
    
    patterns = ["AAAA", "ABCDE", "AABAACAABAA", "AAACAAAAAC"]
    
    for pattern in patterns:
        lps = compute_lps(pattern)
        logger.info(f"Pattern: {pattern}")
        logger.info(f"LPS:     {lps}")
        logger.info()
    
    # Example 4: No match
    logger.info("Example 4: Pattern Not Found")
    logger.info("-" * 70)
    
    text4 = "ABCDEFGHIJKLMNOP"
    pattern4 = "XYZ"
    
    matches4 = kmp_search(text4, pattern4)
    logger.info(f"Text: {text4}")
    logger.info(f"Pattern: {pattern4}")
    logger.info(f"Matches: {matches4}")
    logger.info("Pattern not found in text")
    logger.info()
    
    # Example 5: Performance comparison
    logger.info("Example 5: Performance Measurement")
    logger.info("-" * 70)
    
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
    logger.info(f"KMP Algorithm:")
    logger.info(f"  Time: {metrics_kmp['execution_time_ms']:.3f} ms")
    
    # Naive (for comparison)
    _, metrics_naive = timer.measure(naive_search, text_large, pattern_large)
    logger.info(f"\nNaive Algorithm:")
    logger.info(f"  Time: {metrics_naive['execution_time_ms']:.3f} ms")
    logger.info(f"\nKMP is {metrics_naive['execution_time_ms'] / metrics_kmp['execution_time_ms']:.1f}x faster")
    logger.info()
    
    # Example 6: Real-world application
    logger.info("Example 6: Real-world Application - Text Search")
    logger.info("-" * 70)
    
    document = "The quick brown fox jumps over the lazy dog. " * 10
    search_term = "fox"
    
    positions = kmp_search(document, search_term)
    logger.info(f"Searching for '{search_term}' in document:")
    logger.info(f"Found at positions: {positions}")
    logger.info(f"Total occurrences: {len(positions)}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Preprocessing (LPS): O(m) - m is pattern length")
    logger.info("  Searching: O(n) - n is text length")
    logger.info("  Total: O(n + m)")
    logger.info("  Space: O(m) - for LPS array")
    logger.info("\nKey Advantages:")
    logger.info("  - Linear time complexity")
    logger.info("  - No backtracking in text")
    logger.info("  - Efficient for repeated patterns")
    logger.info("  - Better than naive O(n*m)")
    logger.info("\nKey Disadvantages:")
    logger.info("  - More complex than naive algorithm")
    logger.info("  - Requires preprocessing")
    logger.info("  - Extra space for LPS array")
    logger.info("\nWhen to Use:")
    logger.info("  - Text search in large documents")
    logger.info("  - Pattern matching in strings")
    logger.info("  - DNA sequence matching")
    logger.info("  - Multiple pattern searches")
    logger.info("  - When pattern has repetitions")
    logger.info("\nWhen NOT to Use:")
    logger.info("  - Very short patterns (naive is simpler)")
    logger.info("  - One-time search (preprocessing overhead)")
    logger.info("  - Random text (naive might be faster)")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Text editors (find/replace)")
    logger.info("  - Search engines")
    logger.info("  - DNA sequence analysis")
    logger.info("  - Compiler string matching")
    logger.info("  - Network packet inspection")
    logger.info("\nComparison with Other Algorithms:")
    logger.info("  - Naive: O(n*m) - simple but slow")
    logger.info("  - KMP: O(n+m) - efficient, no backtracking")
    logger.info("  - Rabin-Karp: O(n+m) average - hash-based")
    logger.info("  - Boyer-Moore: O(n/m) best case - skip characters")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()