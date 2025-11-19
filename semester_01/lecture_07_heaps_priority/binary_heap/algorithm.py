#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binary Heap implementation.

This file contains the implementation of the Binary Heap algorithm.
"""

from typing import List, Optional, Dict, Set


class BinaryHeap:
    """Binary heap (min heap) implementation."""

    def __init__(self):
        self.heap: List[int] = []

    def parent(self, i: int) -> int:
        """Get parent index."""
        return (i - 1) // 2

    def left_child(self, i: int) -> int:
        """Get left child index."""
        return 2 * i + 1

    def right_child(self, i: int) -> int:
        """Get right child index."""
        return 2 * i + 2

    def insert(self, val: int) -> None:
        """Insert value into heap."""
        self.heap.append(val)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self) -> Optional[int]:
        """Extract minimum value."""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, i: int) -> None:
        """Maintain heap property upward."""
        while i > 0 and self.heap[self.parent(i)] > self.heap[i]:
            self.heap[i], self.heap[self.parent(i)] = (
                self.heap[self.parent(i)],
                self.heap[i],
            )
            i = self.parent(i)

    def _heapify_down(self, i: int) -> None:
        """Maintain heap property downward."""
        smallest = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_down(smallest)


def main() -> None:
    """Demonstrate Binary Heap."""
    print("=" * 70)
    print("BINARY HEAP")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Binary Heap")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
