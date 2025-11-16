#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binary Heap implementation.

Complete binary tree that satisfies the heap property:
- Max Heap: parent >= children
- Min Heap: parent <= children
"""

import sys
from pathlib import Path
from typing import List, Optional, Callable

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class BinaryHeap:
    """
    Binary Heap data structure.
    
    Supports both min-heap and max-heap via comparator function.
    """
    
    def __init__(self, heap_type: str = 'min'):
        """
        Initialize binary heap.
        
        Args:
            heap_type: 'min' for min-heap, 'max' for max-heap
        """
        self.heap: List[int] = []
        self.heap_type = heap_type
        
        if heap_type == 'min':
            self._compare = lambda a, b: a < b
        else:
            self._compare = lambda a, b: a > b
    
    def _parent(self, index: int) -> int:
        """Get parent index."""
        return (index - 1) // 2
    
    def _left_child(self, index: int) -> int:
        """Get left child index."""
        return 2 * index + 1
    
    def _right_child(self, index: int) -> int:
        """Get right child index."""
        return 2 * index + 2
    
    def _swap(self, i: int, j: int) -> None:
        """Swap elements at indices i and j."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def _heapify_up(self, index: int) -> None:
        """Move element up to maintain heap property."""
        while index > 0:
            parent = self._parent(index)
            if self._compare(self.heap[index], self.heap[parent]):
                self._swap(index, parent)
                index = parent
            else:
                break
    
    def _heapify_down(self, index: int) -> None:
        """Move element down to maintain heap property."""
        while True:
            left = self._left_child(index)
            right = self._right_child(index)
            target = index
            
            if left < len(self.heap) and \
               self._compare(self.heap[left], self.heap[target]):
                target = left
            
            if right < len(self.heap) and \
               self._compare(self.heap[right], self.heap[target]):
                target = right
            
            if target != index:
                self._swap(index, target)
                index = target
            else:
                break
    
    def insert(self, value: int) -> None:
        """Insert value into heap."""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)
    
    def extract(self) -> Optional[int]:
        """Extract root element."""
        if not self.heap:
            return None
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        
        return root
    
    def peek(self) -> Optional[int]:
        """Get root without removing."""
        return self.heap[0] if self.heap else None
    
    def size(self) -> int:
        """Get heap size."""
        return len(self.heap)
    
    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return len(self.heap) == 0
    
    def build_heap(self, arr: List[int]) -> None:
        """Build heap from array."""
        self.heap = arr[:]
        # Start from last non-leaf node
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._heapify_down(i)


def main() -> None:
    """Demonstration of Binary Heap."""
    logger.info("=" * 70)
    logger.info("BINARY HEAP DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Min Heap
    logger.info("Example 1: Min Heap Operations")
    logger.info("-" * 70)
    
    min_heap = BinaryHeap('min')
    values = [10, 20, 15, 30, 40, 5, 25]
    
    logger.info(f"Inserting: {values}")
    for val in values:
        min_heap.insert(val)
        logger.info(f"  After inserting {val}: root = {min_heap.peek()}")
    
    logger.info(f"\nExtracting all elements:")
    while not min_heap.is_empty():
        logger.info(f"  Extracted: {min_heap.extract()}")
    logger.info()
    
    # Example 2: Max Heap
    logger.info("Example 2: Max Heap Operations")
    logger.info("-" * 70)
    
    max_heap = BinaryHeap('max')
    for val in values:
        max_heap.insert(val)
    
    logger.info(f"Extracting from max heap:")
    while not max_heap.is_empty():
        logger.info(f"  Extracted: {max_heap.extract()}")
    logger.info()
    
    # Example 3: Build heap from array
    logger.info("Example 3: Build Heap from Array")
    logger.info("-" * 70)
    
    arr = [4, 10, 3, 5, 1]
    heap = BinaryHeap('min')
    heap.build_heap(arr)
    
    logger.info(f"Array: {arr}")
    logger.info(f"Heap structure: {heap.heap}")
    logger.info(f"Extracting: {[heap.extract() for _ in range(heap.size())]}")
    logger.info()
    
    # Example 4: Performance
    logger.info("Example 4: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Binary Heap")
    
    def test_operations(n):
        heap = BinaryHeap('min')
        for i in range(n):
            heap.insert(i)
        for _ in range(n):
            heap.extract()
        return heap
    
    _, metrics = timer.measure(test_operations, 1000)
    logger.info(f"1000 insertions + 1000 extractions:")
    logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")
    
    logger.info()
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Insert: O(log n)")
    logger.info("  Extract: O(log n)")
    logger.info("  Peek: O(1)")
    logger.info("  Build Heap: O(n)")
    logger.info("  Space: O(n)")
    logger.info("\nKey Advantages:")
    logger.info("  - Efficient priority queue")
    logger.info("  - O(log n) insert/extract")
    logger.info("  - O(1) peek")
    logger.info("  - Used in heap sort, Dijkstra's algorithm")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()