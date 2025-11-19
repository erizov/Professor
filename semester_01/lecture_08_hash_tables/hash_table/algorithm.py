#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hash Table implementation.

This file contains the implementation of the Hash Table algorithm.
"""

from typing import List, Optional, Dict, Set


class HashTable:
    """Hash table implementation with chaining."""

    def __init__(self, size: int = 10):
        self.size = size
        self.table: List[List[tuple]] = [[] for _ in range(size)]

    def _hash(self, key: int) -> int:
        """Hash function."""
        return key % self.size

    def insert(self, key: int, value: any) -> None:
        """Insert key-value pair."""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def get(self, key: int) -> Optional[any]:
        """Get value by key."""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key: int) -> bool:
        """Delete key-value pair."""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False


def main() -> None:
    """Demonstrate Hash Table."""
    print("=" * 70)
    print("HASH TABLE")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Hash Table")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
