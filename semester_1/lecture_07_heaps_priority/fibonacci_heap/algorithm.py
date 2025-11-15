#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fibonacci Heap Implementation.

A data structure for priority queue operations with better amortized
time bounds than binary heaps. Supports O(1) insert and decrease-key,
O(log n) delete-min operations.
"""

import sys
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


@dataclass
class FibonacciNode:
    """Node in Fibonacci heap."""
    key: int
    value: any = None
    parent: Optional['FibonacciNode'] = None
    child: Optional['FibonacciNode'] = None
    left: Optional['FibonacciNode'] = None
    right: Optional['FibonacciNode'] = None
    degree: int = 0
    marked: bool = False
    
    def __init__(self, key: int, value: any = None):
        self.key = key
        self.value = value
        self.parent = None
        self.child = None
        self.left = self
        self.right = self
        self.degree = 0
        self.marked = False


class FibonacciHeap:
    """
    Fibonacci Heap implementation.
    
    Amortized time complexities:
    - insert: O(1)
    - find_min: O(1)
    - extract_min: O(log n)
    - decrease_key: O(1)
    - delete: O(log n)
    """
    
    def __init__(self):
        """Initialize Fibonacci heap."""
        self.min_node: Optional[FibonacciNode] = None
        self.num_nodes = 0
    
    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return self.min_node is None
    
    def insert(self, key: int, value: any = None) -> FibonacciNode:
        """
        Insert node into heap.
        
        Time Complexity: O(1) amortized
        
        Args:
            key: Priority key
            value: Optional value
            
        Returns:
            Created node
        """
        node = FibonacciNode(key, value)
        
        if self.min_node is None:
            self.min_node = node
        else:
            # Add to root list
            node.left = self.min_node
            node.right = self.min_node.right
            self.min_node.right = node
            node.right.left = node
            
            # Update min if necessary
            if node.key < self.min_node.key:
                self.min_node = node
        
        self.num_nodes += 1
        return node
    
    def find_min(self) -> Optional[int]:
        """
        Find minimum key.
        
        Time Complexity: O(1)
        
        Returns:
            Minimum key or None if empty
        """
        return self.min_node.key if self.min_node else None
    
    def extract_min(self) -> Optional[FibonacciNode]:
        """
        Extract and remove minimum node.
        
        Time Complexity: O(log n) amortized
        
        Returns:
            Minimum node or None if empty
        """
        if self.min_node is None:
            return None
        
        min_node = self.min_node
        
        # Move children to root list
        if min_node.child is not None:
            child = min_node.child
            while True:
                next_child = child.right
                child.parent = None
                child.left = self.min_node
                child.right = self.min_node.right
                self.min_node.right = child
                child.right.left = child
                
                if next_child == min_node.child:
                    break
                child = next_child
        
        # Remove min_node from root list
        min_node.left.right = min_node.right
        min_node.right.left = min_node.left
        
        if min_node == min_node.right:
            self.min_node = None
        else:
            self.min_node = min_node.right
            self._consolidate()
        
        self.num_nodes -= 1
        return min_node
    
    def _consolidate(self) -> None:
        """Consolidate trees of same degree."""
        # Array to track trees by degree
        degree_array: List[Optional[FibonacciNode]] = [None] * (self.num_nodes + 1)
        
        # Process all nodes in root list
        nodes_to_process = []
        current = self.min_node
        if current:
            nodes_to_process.append(current)
            temp = current.right
            while temp != current:
                nodes_to_process.append(temp)
                temp = temp.right
        
        for node in nodes_to_process:
            degree = node.degree
            
            # Merge trees of same degree
            while degree_array[degree] is not None:
                other = degree_array[degree]
                
                # Ensure node.key <= other.key
                if node.key > other.key:
                    node, other = other, node
                
                # Make other a child of node
                self._link(other, node)
                
                degree_array[degree] = None
                degree += 1
            
            degree_array[degree] = node
        
        # Rebuild root list and find new min
        self.min_node = None
        for node in degree_array:
            if node is not None:
                if self.min_node is None:
                    self.min_node = node
                    node.left = node
                    node.right = node
                else:
                    node.left = self.min_node
                    node.right = self.min_node.right
                    self.min_node.right = node
                    node.right.left = node
                    
                    if node.key < self.min_node.key:
                        self.min_node = node
    
    def _link(self, child: FibonacciNode, parent: FibonacciNode) -> None:
        """Link child to parent."""
        # Remove child from root list
        child.left.right = child.right
        child.right.left = child.left
        
        # Make child a child of parent
        child.parent = parent
        if parent.child is None:
            parent.child = child
            child.left = child
            child.right = child
        else:
            child.left = parent.child
            child.right = parent.child.right
            parent.child.right = child
            child.right.left = child
        
        parent.degree += 1
        child.marked = False
    
    def decrease_key(self, node: FibonacciNode, new_key: int) -> None:
        """
        Decrease key of node.
        
        Time Complexity: O(1) amortized
        
        Args:
            node: Node to decrease key
            new_key: New key value (must be <= current key)
        """
        if new_key > node.key:
            raise ValueError("New key must be <= current key")
        
        node.key = new_key
        parent = node.parent
        
        if parent is not None and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)
        
        if node.key < self.min_node.key:
            self.min_node = node
    
    def _cut(self, node: FibonacciNode, parent: FibonacciNode) -> None:
        """Cut node from parent."""
        # Remove from parent's child list
        if node.right == node:
            parent.child = None
        else:
            node.left.right = node.right
            node.right.left = node.left
            if parent.child == node:
                parent.child = node.right
        
        parent.degree -= 1
        
        # Add to root list
        node.parent = None
        node.marked = False
        node.left = self.min_node
        node.right = self.min_node.right
        self.min_node.right = node
        node.right.left = node
    
    def _cascading_cut(self, node: FibonacciNode) -> None:
        """Cascading cut operation."""
        parent = node.parent
        if parent is not None:
            if not node.marked:
                node.marked = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)
    
    def delete(self, node: FibonacciNode) -> None:
        """
        Delete node from heap.
        
        Time Complexity: O(log n) amortized
        
        Args:
            node: Node to delete
        """
        self.decrease_key(node, float('-inf'))
        self.extract_min()
    
    def size(self) -> int:
        """Get number of nodes."""
        return self.num_nodes


def main() -> None:
    """Demonstration of Fibonacci Heap."""
    print("=" * 70)
    print("FIBONACCI HEAP DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic operations
    print("Example 1: Basic Operations")
    print("-" * 70)
    
    heap = FibonacciHeap()
    
    # Insert elements
    print("Inserting elements:")
    nodes = []
    for key in [5, 3, 7, 1, 9, 2, 6]:
        node = heap.insert(key, f"Value{key}")
        nodes.append(node)
        print(f"  Inserted: {key}, Min: {heap.find_min()}")
    print()
    
    # Extract min
    print("Extracting minimum elements:")
    while not heap.is_empty():
        min_node = heap.extract_min()
        print(f"  Extracted: {min_node.key}, Remaining: {heap.size()}")
    print()
    
    # Example 2: Decrease key
    print("Example 2: Decrease Key Operation")
    print("-" * 70)
    
    heap = FibonacciHeap()
    node5 = heap.insert(5, "Five")
    node10 = heap.insert(10, "Ten")
    node15 = heap.insert(15, "Fifteen")
    
    print(f"Initial min: {heap.find_min()}")
    print(f"Decreasing key 10 to 2...")
    heap.decrease_key(node10, 2)
    print(f"New min: {heap.find_min()}")
    print()
    
    # Example 3: Priority queue simulation
    print("Example 3: Priority Queue Simulation")
    print("-" * 70)
    
    heap = FibonacciHeap()
    
    # Insert tasks with priorities
    tasks = [
        (3, "Low priority task"),
        (1, "High priority task"),
        (2, "Medium priority task"),
        (1, "Another high priority task"),
    ]
    
    print("Inserting tasks:")
    task_nodes = []
    for priority, description in tasks:
        node = heap.insert(priority, description)
        task_nodes.append(node)
        print(f"  Priority {priority}: {description}")
    print()
    
    print("Processing tasks in priority order:")
    while not heap.is_empty():
        task = heap.extract_min()
        print(f"  Processing: {task.value} (priority: {task.key})")
    print()
    
    # Example 4: Performance measurement
    print("Example 4: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Fibonacci Heap")
    
    def heap_operations():
        heap = FibonacciHeap()
        nodes = []
        
        # Insert
        for i in range(100):
            node = heap.insert(i, f"Item{i}")
            nodes.append(node)
        
        # Extract all
        while not heap.is_empty():
            heap.extract_min()
        
        return heap.size()
    
    result, metrics = timer.measure(heap_operations)
    print(f"Time to insert and extract 100 elements: "
          f"{metrics['execution_time_ms']:.3f} ms")
    print()
    
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Insert:       O(1) amortized")
    print("  Find Min:     O(1)")
    print("  Extract Min:  O(log n) amortized")
    print("  Decrease Key: O(1) amortized")
    print("  Delete:       O(log n) amortized")
    print("\nKey Advantages:")
    print("  - O(1) insert and decrease-key")
    print("  - Better than binary heap for some operations")
    print("  - Useful for Dijkstra's algorithm")
    print("  - Lazy consolidation")
    print("\nKey Disadvantages:")
    print("  - Complex implementation")
    print("  - Higher constant factors")
    print("  - Not cache-friendly")
    print("  - More memory overhead")
    print("\nWhen to Use:")
    print("  - Many decrease-key operations")
    print("  - Dijkstra's algorithm")
    print("  - Prim's algorithm")
    print("  - Priority queue with frequent updates")
    print("\nCommon Use Cases:")
    print("  - Graph algorithms (Dijkstra, Prim)")
    print("  - Network routing")
    print("  - Task scheduling")
    print("  - Event simulation")
    print("=" * 70)


if __name__ == "__main__":
    main()
