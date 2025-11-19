#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Readers Writers implementation.

This file contains the implementation of the Readers Writers algorithm.
"""

from typing import List, Optional, Dict, Set


import threading


class ReadersWriters:
    """Readers-Writers problem solution."""

    def __init__(self):
        self.readers_count = 0
        self.mutex = threading.Lock()
        self.write_lock = threading.Lock()
        self.data = 0

    def read(self) -> int:
        """Read data."""
        with self.mutex:
            self.readers_count += 1
            if self.readers_count == 1:
                self.write_lock.acquire()

        # Read data
        value = self.data

        with self.mutex:
            self.readers_count -= 1
            if self.readers_count == 0:
                self.write_lock.release()

        return value

    def write(self, value: int) -> None:
        """Write data."""
        with self.write_lock:
            self.data = value


def main() -> None:
    """Demonstrate Readers Writers."""
    print("=" * 70)
    print("READERS WRITERS")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Readers Writers")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
