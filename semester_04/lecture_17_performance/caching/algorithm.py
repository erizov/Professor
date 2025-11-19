#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Caching implementation.

This file contains the implementation of the Caching algorithm.
"""

from typing import List, Optional, Dict, Set


class Cache:
    """Simple cache implementation."""

    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.cache: Dict[str, any] = {}
        self.access_order: List[str] = []

    def get(self, key: str) -> Optional[any]:
        """Get value from cache."""
        if key in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None

    def put(self, key: str, value: any) -> None:
        """Put value in cache."""
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            # Remove least recently used
            lru_key = self.access_order.pop(0)
            del self.cache[lru_key]

        self.cache[key] = value
        self.access_order.append(key)

    def clear(self) -> None:
        """Clear cache."""
        self.cache.clear()
        self.access_order.clear()


def main() -> None:
    """Demonstrate Caching."""
    print("=" * 70)
    print("CACHING")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Caching")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
