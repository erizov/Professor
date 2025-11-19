#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rabin Karp implementation.

This file contains the implementation of the Rabin Karp algorithm.
"""

from typing import List, Optional, Dict, Set


def rabin_karp_search(
    text: str, pattern: str, base: int = 256, mod: int = 101
) -> List[int]:
    """Rabin-Karp string search algorithm."""
    m, n = len(pattern), len(text)
    if m == 0 or m > n:
        return []

    # Calculate hash of pattern and first window of text
    pattern_hash = 0
    text_hash = 0
    h = 1

    for i in range(m - 1):
        h = (h * base) % mod

    for i in range(m):
        pattern_hash = (base * pattern_hash + ord(pattern[i])) % mod
        text_hash = (base * text_hash + ord(text[i])) % mod

    result = []

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i : i + m] == pattern:
                result.append(i)

        if i < n - m:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            if text_hash < 0:
                text_hash += mod

    return result


def main() -> None:
    """Demonstrate Rabin Karp."""
    print("=" * 70)
    print("RABIN KARP")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Rabin Karp")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
