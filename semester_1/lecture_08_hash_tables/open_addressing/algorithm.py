#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open Addressing implementation.

This file contains the implementation of the Open Addressing algorithm.
"""

from typing import List, Optional, Dict, Set


class HashTableOpenAddressing:
    """Hash table with open addressing (linear probing)."""
    def __init__(self, size: int = 10):
        self.size = size
        self.table: List[Optional[tuple]] = [None] * size
        self.deleted = object()  # Marker for deleted entries
    
    def _hash(self, key: int) -> int:
        """Hash function."""
        return key % self.size
    
    def _probe(self, key: int, start_index: int) -> int:
        """Linear probing."""
        index = start_index
        while self.table[index] is not None and self.table[index] is not self.deleted:
            if self.table[index][0] == key:
                return index
            index = (index + 1) % self.size
            if index == start_index:
                raise Exception("Hash table is full")
        return index
    
    def insert(self, key: int, value: any) -> None:
        """Insert key-value pair."""
        index = self._hash(key)
        index = self._probe(key, index)
        self.table[index] = (key, value)
    
    def get(self, key: int) -> Optional[any]:
        """Get value by key."""
        index = self._hash(key)
        start = index
        while self.table[index] is not None:
            if self.table[index] is not self.deleted and self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.size
            if index == start:
                break
        return None
    
    def delete(self, key: int) -> bool:
        """Delete key-value pair."""
        index = self._hash(key)
        start = index
        while self.table[index] is not None:
            if self.table[index] is not self.deleted and self.table[index][0] == key:
                self.table[index] = self.deleted
                return True
            index = (index + 1) % self.size
            if index == start:
                break
        return False


def main() -> None:
    """Demonstrate Open Addressing."""
    print("=" * 70)
    print("OPEN ADDRESSING")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Open Addressing")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
