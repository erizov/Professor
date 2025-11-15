#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AVL Tree implementation.

Self-balancing binary search tree with guaranteed O(log n) operations.
"""

import sys
from pathlib import Path
from typing import Optional, List
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class AVLNode:
    """Node in an AVL tree."""
    
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1


class AVLTree:
    """
    AVL Tree - Self-balancing Binary Search Tree.
    
    Maintains balance factor of each node in range [-1, 1].
    Performs rotations to maintain balance after insertions/deletions.
    """
    
    def __init__(self):
        """Initialize empty AVL tree."""
        self.root: Optional[AVLNode] = None
    
    def get_height(self, node: Optional[AVLNode]) -> int:
        """Get height of node."""
        if not node:
            return 0
        return node.height
    
    def get_balance(self, node: Optional[AVLNode]) -> int:
        """Get balance factor of node."""
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def update_height(self, node: AVLNode) -> None:
        """Update height of node."""
        node.height = 1 + max(self.get_height(node.left),
                             self.get_height(node.right))
    
    def rotate_right(self, z: AVLNode) -> AVLNode:
        """
        Right rotation.
        
            z                y
           / \              / \
          y   C    =>      x   z
         / \                  / \
        x   B                B   C
        """
        y = z.left
        B = y.right
        
        # Perform rotation
        y.right = z
        z.left = B
        
        # Update heights
        self.update_height(z)
        self.update_height(y)
        
        return y
    
    def rotate_left(self, z: AVLNode) -> AVLNode:
        """
        Left rotation.
        
          z                  y
         / \                / \
        A   y      =>      z   x
           / \            / \
          B   x          A   B
        """
        y = z.right
        B = y.left
        
        # Perform rotation
        y.left = z
        z.right = B
        
        # Update heights
        self.update_height(z)
        self.update_height(y)
        
        return y
    
    def insert(self, val: int) -> None:
        """
        Insert value into AVL tree.
        
        Time Complexity: O(log n)
        """
        self.root = self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node: Optional[AVLNode],
                         val: int) -> AVLNode:
        """Helper for recursive insertion with balancing."""
        # Standard BST insertion
        if not node:
            return AVLNode(val)
        
        if val < node.val:
            node.left = self._insert_recursive(node.left, val)
        else:
            node.right = self._insert_recursive(node.right, val)
        
        # Update height
        self.update_height(node)
        
        # Get balance factor
        balance = self.get_balance(node)
        
        # Left-Left Case
        if balance > 1 and val < node.left.val:
            return self.rotate_right(node)
        
        # Right-Right Case
        if balance < -1 and val > node.right.val:
            return self.rotate_left(node)
        
        # Left-Right Case
        if balance > 1 and val > node.left.val:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        
        # Right-Left Case
        if balance < -1 and val < node.right.val:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        
        return node
    
    def search(self, val: int) -> bool:
        """
        Search for value.
        
        Time Complexity: O(log n)
        """
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node: Optional[AVLNode],
                         val: int) -> bool:
        """Helper for recursive search."""
        if not node:
            return False
        
        if val == node.val:
            return True
        elif val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)
    
    def inorder(self, node: Optional[AVLNode] = None,
               result: Optional[List[int]] = None) -> List[int]:
        """Inorder traversal."""
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        if node:
            self.inorder(node.left, result)
            result.append(node.val)
            self.inorder(node.right, result)
        
        return result
    
    def height(self) -> int:
        """Get height of tree."""
        return self.get_height(self.root)
    
    def size(self, node: Optional[AVLNode] = None) -> int:
        """Count number of nodes."""
        if node is None:
            node = self.root
        
        if not node:
            return 0
        
        return 1 + self.size(node.left) + self.size(node.right)


def main() -> None:
    """Demonstration of AVL Tree."""
    print("=" * 70)
    print("AVL TREE DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic operations
    print("Example 1: Building an AVL Tree")
    print("-" * 70)
    
    avl = AVLTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    
    print(f"Inserting values: {values}")
    for val in values:
        avl.insert(val)
    
    print(f"Size: {avl.size()}")
    print(f"Height: {avl.height()}")
    print(f"Inorder (sorted): {avl.inorder()}")
    print()
    
    # Example 2: Search
    print("Example 2: Searching")
    print("-" * 70)
    
    search_values = [40, 25, 70, 100]
    for val in search_values:
        found = avl.search(val)
        print(f"Search {val}: {'Found' if found else 'Not found'}")
    print()
    
    # Example 3: Balance demonstration
    print("Example 3: Self-Balancing Demonstration")
    print("-" * 70)
    
    # Sequential insertion (would create skewed tree in BST)
    avl_balanced = AVLTree()
    sequential = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print(f"Inserting sequential values: {sequential}")
    for val in sequential:
        avl_balanced.insert(val)
    
    print(f"Size: {avl_balanced.size()}")
    print(f"Height: {avl_balanced.height()} (balanced!)")
    print(f"Compare to BST height which would be: {len(sequential)}")
    print(f"Inorder: {avl_balanced.inorder()}")
    print()
    
    # Example 4: Performance comparison
    print("Example 4: Performance vs BST")
    print("-" * 70)
    
    print("Sequential insertion (worst case for BST):")
    timer = PerformanceTimer("AVL Tree")
    
    sizes = [100, 500, 1000]
    for size in sizes:
        avl_perf = AVLTree()
        values_perf = list(range(size))
        
        def insert_all():
            for val in values_perf:
                avl_perf.insert(val)
        
        _, metrics = timer.measure(insert_all)
        
        print(f"n={size:4d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"height={avl_perf.height()} (optimal: ~{size.bit_length()})")
    
    print()
    timer.print_summary()
    
    print("\n" + "=" * 70)
    print("\nComplexity Summary:")
    print("  Search:  O(log n) - GUARANTEED")
    print("  Insert:  O(log n) - GUARANTEED")
    print("  Delete:  O(log n) - GUARANTEED")
    print("  Space:   O(n)")
    print("  Height:  O(log n) - self-balancing")
    print("\nKey Points:")
    print("  + Guaranteed O(log n) operations")
    print("  + Self-balancing after each operation")
    print("  + Better than BST for sorted/skewed data")
    print("  + Predictable performance")
    print("  - More complex implementation")
    print("  - Extra space for height storage")
    print("  - More rotations than Red-Black trees")
    print("\nBalance Factor:")
    print("  Range: [-1, 0, 1]")
    print("  Formula: height(left) - height(right)")
    print("  Rebalance if |balance_factor| > 1")
    print("\nRotations:")
    print("  LL Case: Right rotation")
    print("  RR Case: Left rotation")
    print("  LR Case: Left-Right rotation")
    print("  RL Case: Right-Left rotation")
    print("\nWhen to use:")
    print("  • Need guaranteed O(log n)")
    print("  • Frequent searches")
    print("  • Sorted/near-sorted insertions")
    print("  • Predictable performance critical")
    print("\nWhen NOT to use:")
    print("  • Frequent insertions/deletions")
    print("  • Simpler BST sufficient")
    print("  • Memory constrained (extra height storage)")
    print("=" * 70)


if __name__ == "__main__":
    main()

