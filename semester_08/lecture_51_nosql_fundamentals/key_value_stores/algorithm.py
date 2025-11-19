#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Key Value Stores implementation.

This file contains the implementation of the Key Value Stores algorithm.
"""

from typing import List, Optional, Dict, Set


class KeyValueStore:
    """Key-value store."""

    def __init__(self):
        self.store: Dict[str, any] = {}
        self.ttl: Dict[str, float] = {}

    def put(self, key: str, value: any, ttl: int = None) -> None:
        """Put key-value pair."""
        import time

        self.store[key] = value
        if ttl:
            self.ttl[key] = time.time() + ttl

    def get(self, key: str) -> Optional[any]:
        """Get value by key."""
        import time

        if key in self.ttl and time.time() > self.ttl[key]:
            del self.store[key]
            del self.ttl[key]
            return None
        return self.store.get(key)

    def delete(self, key: str) -> bool:
        """Delete key."""
        if key in self.store:
            del self.store[key]
            if key in self.ttl:
                del self.ttl[key]
            return True
        return False

    def exists(self, key: str) -> bool:
        """Check if key exists."""
        return key in self.store


def main() -> None:
    """Demonstrate Key Value Stores."""
    print("=" * 70)
    print("KEY VALUE STORES")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Key Value Stores")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
