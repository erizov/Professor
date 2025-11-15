#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Priority Queue implementation using binary heap.

Elements are dequeued based on priority (highest/lowest first).
"""

import sys
from pathlib import Path
from typing import List, Optional, TypeVar, Generic, Tuple
import heapq

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer

T = TypeVar('T')


class PriorityQueue(Generic[T]):
    """
    Priority Queue using binary heap (min-heap by default).
    
    Lower values have higher priority (min-heap).
    """
    
    def __init__(self, max_priority: bool = False):
        """
        Initialize priority queue.
        
        Args:
            max_priority: If True, higher values have higher priority (max-heap)
        """
        self.heap: List[Tuple[int, int, T]] = []  # (priority, insertion_order, item)
        self.max_priority = max_priority
        self.counter = 0  # For tie-breaking
    
    def push(self, item: T, priority: int) -> None:
        """
        Add item with priority.
        
        Args:
            item: Item to add
            priority: Priority value
        """
        if self.max_priority:
            priority = -priority  # Negate for max-heap
        
        heapq.heappush(self.heap, (priority, self.counter, item))
        self.counter += 1
    
    def pop(self) -> Optional[T]:
        """
        Remove and return highest priority item.
        
        Returns:
            Highest priority item, or None if empty
        """
        if self.is_empty():
            return None
        
        priority, _, item = heapq.heappop(self.heap)
        return item
    
    def peek(self) -> Optional[T]:
        """
        Get highest priority item without removing.
        
        Returns:
            Highest priority item, or None if empty
        """
        if self.is_empty():
            return None
        
        return self.heap[0][2]
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.heap) == 0
    
    def size(self) -> int:
        """Get number of items."""
        return len(self.heap)
    
    def __len__(self) -> int:
        """Get number of items."""
        return len(self.heap)


class Task:
    """Task with priority for demonstration."""
    
    def __init__(self, name: str, priority: int):
        self.name = name
        self.priority = priority
    
    def __str__(self) -> str:
        return f"Task({self.name}, priority={self.priority})"
    
    def __repr__(self) -> str:
        return str(self)


def main() -> None:
    """Demonstration of Priority Queue."""
    print("=" * 70)
    print("PRIORITY QUEUE DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Min priority queue
    print("Example 1: Min Priority Queue (Lower = Higher Priority)")
    print("-" * 70)
    
    pq = PriorityQueue(max_priority=False)
    
    pq.push("Task A", 5)
    pq.push("Task B", 1)  # Highest priority
    pq.push("Task C", 3)
    pq.push("Task D", 2)
    pq.push("Task E", 4)
    
    print("Processing tasks in priority order:")
    while not pq.is_empty():
        task = pq.pop()
        print(f"  Processing: {task}")
    print()
    
    # Example 2: Max priority queue
    print("Example 2: Max Priority Queue (Higher = Higher Priority)")
    print("-" * 70)
    
    pq2 = PriorityQueue(max_priority=True)
    
    pq2.push("Low Priority", 1)
    pq2.push("High Priority", 5)
    pq2.push("Medium Priority", 3)
    pq2.push("Very High Priority", 10)
    
    print("Processing tasks in priority order:")
    while not pq2.is_empty():
        task = pq2.pop()
        print(f"  Processing: {task}")
    print()
    
    # Example 3: Task scheduling
    print("Example 3: Task Scheduling")
    print("-" * 70)
    
    tasks = [
        Task("Email", 3),
        Task("Urgent Bug Fix", 1),  # Highest priority
        Task("Code Review", 4),
        Task("Critical Production Issue", 0),  # Highest priority
        Task("Documentation", 5),
    ]
    
    pq3 = PriorityQueue(max_priority=False)
    for task in tasks:
        pq3.push(task, task.priority)
    
    print("Task execution order:")
    order = 1
    while not pq3.is_empty():
        task = pq3.pop()
        print(f"  {order}. {task}")
        order += 1
    print()
    
    # Example 4: Dijkstra's algorithm usage
    print("Example 4: Usage in Dijkstra's Algorithm")
    print("-" * 70)
    
    print("Priority queues are essential for:")
    print("  - Dijkstra's shortest path algorithm")
    print("  - A* pathfinding")
    print("  - Huffman coding")
    print("  - Task scheduling")
    print("  - Event simulation")
    print()
    
    # Example 5: Performance measurement
    print("Example 5: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Priority Queue")
    
    def test_operations(n):
        pq = PriorityQueue()
        # Push n items
        for i in range(n):
            pq.push(f"item_{i}", i)
        # Pop all items
        while not pq.is_empty():
            _ = pq.pop()
        return pq
    
    for n in [100, 1000, 10000]:
        _, metrics = timer.measure(test_operations, n)
        print(f"Operations on {n} elements:")
        print(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        print(f"  Memory: {metrics['memory_peak_kb']:.2f} KB")
    
    print()
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Push: O(log n)")
    print("  Pop: O(log n)")
    print("  Peek: O(1)")
    print("  Space: O(n)")
    print("\nKey Advantages:")
    print("  - Efficient priority-based access")
    print("  - O(log n) insertions and deletions")
    print("  - O(1) peek operation")
    print("  - Used in many algorithms")
    print("\nKey Disadvantages:")
    print("  - Not efficient for random access")
    print("  - No efficient search operation")
    print("  - Slower than regular queue for FIFO")
    print("\nWhen to Use:")
    print("  - Task scheduling")
    print("  - Dijkstra's algorithm")
    print("  - A* pathfinding")
    print("  - Huffman coding")
    print("  - Event-driven simulation")
    print("\nWhen NOT to Use:")
    print("  - Simple FIFO queue (use regular queue)")
    print("  - Need random access")
    print("  - Need to search for specific items")
    print("\nCommon Use Cases:")
    print("  - Operating system task scheduling")
    print("  - Network packet routing")
    print("  - Graph algorithms (Dijkstra, Prim)")
    print("  - Data compression (Huffman)")
    print("  - Discrete event simulation")
    print("=" * 70)


if __name__ == "__main__":
    main()
