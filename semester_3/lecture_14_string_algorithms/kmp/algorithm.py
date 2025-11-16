#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knuth-Morris-Pratt (KMP) String Matching Algorithm.

Efficient string searching algorithm that uses information from previous
matches to avoid unnecessary comparisons. Preprocesses the pattern to
create a failure function (LPS array).
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
        List of indices where pattern is found
        
    Time Complexity: O(n + m)
    Space Complexity: O(m)
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return []
    if n < m:
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


def kmp_search_all(text: str, pattern: str) -> List[int]:
    """Find all occurrences of pattern in text."""
    return kmp_search(text, pattern)


def count_occurrences(text: str, pattern: str) -> int:
    """Count occurrences of pattern in text."""
    return len(kmp_search(text, pattern))


def main() -> None:
    """Demonstration of KMP Algorithm."""
    logger.info("=" * 70)
    logger.info("KNUTH-MORRIS-PRATT (KMP) STRING MATCHING DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic search
    logger.info("Example 1: Basic String Search")
    logger.info("-" * 70)
    
    test_cases = [
        ("ABABDABACDABABCABCABAB", "ABABCABAB"),
        ("AABAACAADAABAABA", "AABA"),
        ("THIS IS A TEST TEXT", "TEST"),
        ("AAAAABAAABA", "AAAA"),
    ]
    
    for text, pattern in test_cases:
        indices = kmp_search(text, pattern)
        logger.info(f"Text: '{text}'")
        logger.info(f"Pattern: '{pattern}'")
        logger.info(f"Found at indices: {indices}")
        logger.info(f"Count: {len(indices)}")
        logger.info()
    
    # Example 2: Multiple occurrences
    logger.info("Example 2: Multiple Occurrences")
    logger.info("-" * 70)
    
    text = "ABABDABACDABABCABCABAB"
    pattern = "AB"
    
    indices = kmp_search_all(text, pattern)
    logger.info(f"Text: '{text}'")
    logger.info(f"Pattern: '{pattern}'")
    logger.info(f"All occurrences at: {indices}")
    logger.info(f"Total count: {count_occurrences(text, pattern)}")
    logger.info()
    
    # Example 3: LPS array demonstration
    logger.info("Example 3: LPS Array (Longest Proper Prefix which is also Suffix)")
    logger.info("-" * 70)
    
    patterns = ["ABABCABAB", "AAAA", "ABCDE", "AABAACAABAA"]
    
    for pattern in patterns:
        lps = compute_lps(pattern)
        logger.info(f"Pattern: '{pattern}'")
        logger.info(f"LPS:     {lps}")
        logger.info()
    
    # Example 4: Performance comparison
    logger.info("Example 4: Performance Measurement")
    logger.info("-" * 70)
    
    text = "A" * 10000 + "B" + "A" * 10000
    pattern = "A" * 100 + "B"
    
    timer = PerformanceTimer("KMP")
    
    def kmp_operation():
        return kmp_search(text, pattern)
    
    result, metrics = timer.measure(kmp_operation)
    logger.info(f"Text length: {len(text)}")
    logger.info(f"Pattern length: {len(pattern)}")
    logger.info(f"Time: {metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Found: {len(result)} occurrence(s)")
    logger.info()
    
    # Example 5: Real-world use case - text search
    logger.info("Example 5: Text Search Use Case")
    logger.info("-" * 70)
    
    document = """
    The quick brown fox jumps over the lazy dog.
    The dog was lazy and the fox was quick.
    Quick brown foxes are common in the forest.
    """
    
    search_terms = ["quick", "fox", "lazy"]
    
    for term in search_terms:
        indices = kmp_search(document.lower(), term.lower())
        logger.info(f"Searching for '{term}':")
        logger.info(f"  Found {len(indices)} occurrence(s) at positions: {indices}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(n + m) - n is text length, m is pattern length")
    logger.info("  Space: O(m) - for LPS array")
    logger.info("\nKey Advantages:")
    logger.info("  - Linear time complexity")
    logger.info("  - No backtracking in text")
    logger.info("  - Efficient for repeated patterns")
    logger.info("  - Better than naive O(n*m) approach")
    logger.info("\nKey Disadvantages:")
    logger.info("  - More complex than naive algorithm")
    logger.info("  - Requires preprocessing")
    logger.info("  - Extra space for LPS array")
    logger.info("\nWhen to Use:")
    logger.info("  - Text search in large documents")
    logger.info("  - Pattern matching")
    logger.info("  - String search libraries")
    logger.info("  - DNA sequence matching")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Text editors (find/replace)")
    logger.info("  - Search engines")
    logger.info("  - Bioinformatics")
    logger.info("  - String matching libraries")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()