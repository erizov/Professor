#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trie implementation.

This file contains the implementation of the Trie algorithm.
"""

from typing import List, Optional, Dict, Set


class TrieNode:
    """Trie node."""

    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end = False


class Trie:
    """Trie data structure."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert word into trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Search for word in trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Check if any word starts with prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


def main() -> None:
    """Demonstrate Trie."""
    print("=" * 70)
    print("TRIE")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Trie")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
