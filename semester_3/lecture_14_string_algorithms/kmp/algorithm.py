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
    print("=" * 70)
    print("KNUTH-MORRIS-PRATT (KMP) STRING MATCHING DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic search
    print("Example 1: Basic String Search")
    print("-" * 70)
    
    test_cases = [
        ("ABABDABACDABABCABCABAB", "ABABCABAB"),
        ("AABAACAADAABAABA", "AABA"),
        ("THIS IS A TEST TEXT", "TEST"),
        ("AAAAABAAABA", "AAAA"),
    ]
    
    for text, pattern in test_cases:
        indices = kmp_search(text, pattern)
        print(f"Text: '{text}'")
        print(f"Pattern: '{pattern}'")
        print(f"Found at indices: {indices}")
        print(f"Count: {len(indices)}")
        print()
    
    # Example 2: Multiple occurrences
    print("Example 2: Multiple Occurrences")
    print("-" * 70)
    
    text = "ABABDABACDABABCABCABAB"
    pattern = "AB"
    
    indices = kmp_search_all(text, pattern)
    print(f"Text: '{text}'")
    print(f"Pattern: '{pattern}'")
    print(f"All occurrences at: {indices}")
    print(f"Total count: {count_occurrences(text, pattern)}")
    print()
    
    # Example 3: LPS array demonstration
    print("Example 3: LPS Array (Longest Proper Prefix which is also Suffix)")
    print("-" * 70)
    
    patterns = ["ABABCABAB", "AAAA", "ABCDE", "AABAACAABAA"]
    
    for pattern in patterns:
        lps = compute_lps(pattern)
        print(f"Pattern: '{pattern}'")
        print(f"LPS:     {lps}")
        print()
    
    # Example 4: Performance comparison
    print("Example 4: Performance Measurement")
    print("-" * 70)
    
    text = "A" * 10000 + "B" + "A" * 10000
    pattern = "A" * 100 + "B"
    
    timer = PerformanceTimer("KMP")
    
    def kmp_operation():
        return kmp_search(text, pattern)
    
    result, metrics = timer.measure(kmp_operation)
    print(f"Text length: {len(text)}")
    print(f"Pattern length: {len(pattern)}")
    print(f"Time: {metrics['execution_time_ms']:.3f} ms")
    print(f"Found: {len(result)} occurrence(s)")
    print()
    
    # Example 5: Real-world use case - text search
    print("Example 5: Text Search Use Case")
    print("-" * 70)
    
    document = """
    The quick brown fox jumps over the lazy dog.
    The dog was lazy and the fox was quick.
    Quick brown foxes are common in the forest.
    """
    
    search_terms = ["quick", "fox", "lazy"]
    
    for term in search_terms:
        indices = kmp_search(document.lower(), term.lower())
        print(f"Searching for '{term}':")
        print(f"  Found {len(indices)} occurrence(s) at positions: {indices}")
    print()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(n + m) - n is text length, m is pattern length")
    print("  Space: O(m) - for LPS array")
    print("\nKey Advantages:")
    print("  - Linear time complexity")
    print("  - No backtracking in text")
    print("  - Efficient for repeated patterns")
    print("  - Better than naive O(n*m) approach")
    print("\nKey Disadvantages:")
    print("  - More complex than naive algorithm")
    print("  - Requires preprocessing")
    print("  - Extra space for LPS array")
    print("\nWhen to Use:")
    print("  - Text search in large documents")
    print("  - Pattern matching")
    print("  - String search libraries")
    print("  - DNA sequence matching")
    print("\nCommon Use Cases:")
    print("  - Text editors (find/replace)")
    print("  - Search engines")
    print("  - Bioinformatics")
    print("  - String matching libraries")
    print("=" * 70)


if __name__ == "__main__":
    main()
