#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Consistent Hashing implementation.

This file contains the implementation of the Consistent Hashing algorithm.
"""

from typing import List, Optional, Dict, Set


class ConsistentHash:
    """Consistent hashing implementation."""

    def __init__(self, nodes: List[str], replicas: int = 3):
        self.replicas = replicas
        self.ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []

        for node in nodes:
            for i in range(replicas):
                key = self._hash(f"{node}:{i}")
                self.ring[key] = node
                self.sorted_keys.append(key)

        self.sorted_keys.sort()

    def _hash(self, key: str) -> int:
        """Hash function."""
        return hash(key) % (2**32)

    def get_node(self, key: str) -> Optional[str]:
        """Get node for given key."""
        if not self.ring:
            return None

        hash_key = self._hash(key)

        # Find first node with hash >= hash_key
        for ring_key in self.sorted_keys:
            if ring_key >= hash_key:
                return self.ring[ring_key]

        # Wrap around
        return self.ring[self.sorted_keys[0]]


def main() -> None:
    """Demonstrate Consistent Hashing."""
    print("=" * 70)
    print("CONSISTENT HASHING")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Consistent Hashing")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
