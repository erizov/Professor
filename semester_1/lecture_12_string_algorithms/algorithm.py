#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
String Algorithms - Demonstration.

This lecture covers string algorithms including
KMP, Boyer-Moore, and Rabin-Karp.
"""


def kmp_search(text: str, pattern: str) -> int:
    """KMP string search algorithm."""
    def build_lps(pattern: str) -> list:
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
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def main() -> None:
    """Demonstrate string algorithms."""
    print("=" * 70)
    print("STRING ALGORITHMS")
    print("=" * 70)
    
    text = "ABABDABACDABABCABCAB"
    pattern = "ABABCABAB"
    result = kmp_search(text, pattern)
    print(f"Text: {text}")
    print(f"Pattern: {pattern}")
    if result != -1:
        print(f"Found at index: {result}")
    else:
        print("Pattern not found")
    print("=" * 70)


if __name__ == "__main__":
    main()
