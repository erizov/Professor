#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kmp implementation.

This file contains the implementation of the Kmp algorithm.
"""

from typing import List, Optional, Dict, Set


def kmp_search(text: str, pattern: str) -> List[int]:
    """KMP string search algorithm."""

    def build_lps(pattern: str) -> List[int]:
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
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

    lps = build_lps(pattern)
    i = j = 0
    result = []

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            result.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return result


def main() -> None:
    """Demonstrate Kmp."""
    print("=" * 70)
    print("KMP")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Kmp")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
