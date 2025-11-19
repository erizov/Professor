#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Priority Queue implementation.

This file contains the implementation of the Priority Queue algorithm.
"""

from typing import List, Optional, Dict, Set


class PriorityQueue:
    """Priority queue implementation using heap."""

    def __init__(self):
        self.heap: List[tuple] = []

    def push(self, item: any, priority: int) -> None:
        """Add item with priority."""
        from heapq import heappush

        heappush(self.heap, (priority, item))

    def pop(self) -> Optional[any]:
        """Remove and return highest priority item."""
        from heapq import heappop

        if self.heap:
            return heappop(self.heap)[1]
        return None

    def peek(self) -> Optional[any]:
        """Return highest priority item without removing."""
        if self.heap:
            return self.heap[0][1]
        return None

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.heap) == 0


def main() -> None:
    """Demonstrate Priority Queue."""
    print("=" * 70)
    print("PRIORITY QUEUE")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Priority Queue")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
