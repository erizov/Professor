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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("=" * 70)
    logger.info("AVL TREE DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic operations
    logger.info("Example 1: Building an AVL Tree")
    logger.info("-" * 70)
    
    avl = AVLTree()
    values = [50, 30, 70, 20, 40, 60, 80]
    
    logger.info(f"Inserting values: {values}")
    for val in values:
        avl.insert(val)
    
    logger.info(f"Size: {avl.size()}")
    logger.info(f"Height: {avl.height()}")
    logger.info(f"Inorder (sorted): {avl.inorder()}")
    logger.info()
    
    # Example 2: Search
    logger.info("Example 2: Searching")
    logger.info("-" * 70)
    
    search_values = [40, 25, 70, 100]
    for val in search_values:
        found = avl.search(val)
        logger.info(f"Search {val}: {'Found' if found else 'Not found'}")
    logger.info()
    
    # Example 3: Balance demonstration
    logger.info("Example 3: Self-Balancing Demonstration")
    logger.info("-" * 70)
    
    # Sequential insertion (would create skewed tree in BST)
    avl_balanced = AVLTree()
    sequential = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    logger.info(f"Inserting sequential values: {sequential}")
    for val in sequential:
        avl_balanced.insert(val)
    
    logger.info(f"Size: {avl_balanced.size()}")
    logger.info(f"Height: {avl_balanced.height()} (balanced!)")
    logger.info(f"Compare to BST height which would be: {len(sequential)}")
    logger.info(f"Inorder: {avl_balanced.inorder()}")
    logger.info()
    
    # Example 4: Performance comparison
    logger.info("Example 4: Performance vs BST")
    logger.info("-" * 70)
    
    logger.info("Sequential insertion (worst case for BST):")
    timer = PerformanceTimer("AVL Tree")
    
    sizes = [100, 500, 1000]
    for size in sizes:
        avl_perf = AVLTree()
        values_perf = list(range(size))
        
        def insert_all():
            for val in values_perf:
                avl_perf.insert(val)
        
        _, metrics = timer.measure(insert_all)
        
        logger.info(f"n={size:4d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"height={avl_perf.height()} (optimal: ~{size.bit_length()})")
    
    logger.info()
    timer.print_summary()
    
    logger.info("\n" + "=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Search:  O(log n) - GUARANTEED")
    logger.info("  Insert:  O(log n) - GUARANTEED")
    logger.info("  Delete:  O(log n) - GUARANTEED")
    logger.info("  Space:   O(n)")
    logger.info("  Height:  O(log n) - self-balancing")
    logger.info("\nKey Points:")
    logger.info("  + Guaranteed O(log n) operations")
    logger.info("  + Self-balancing after each operation")
    logger.info("  + Better than BST for sorted/skewed data")
    logger.info("  + Predictable performance")
    logger.info("  - More complex implementation")
    logger.info("  - Extra space for height storage")
    logger.info("  - More rotations than Red-Black trees")
    logger.info("\nBalance Factor:")
    logger.info("  Range: [-1, 0, 1]")
    logger.info("  Formula: height(left) - height(right)")
    logger.info("  Rebalance if |balance_factor| > 1")
    logger.info("\nRotations:")
    logger.info("  LL Case: Right rotation")
    logger.info("  RR Case: Left rotation")
    logger.info("  LR Case: Left-Right rotation")
    logger.info("  RL Case: Right-Left rotation")
    logger.info("\nWhen to use:")
    logger.info("  • Need guaranteed O(log n)")
    logger.info("  • Frequent searches")
    logger.info("  • Sorted/near-sorted insertions")
    logger.info("  • Predictable performance critical")
    logger.info("\nWhen NOT to use:")
    logger.info("  • Frequent insertions/deletions")
    logger.info("  • Simpler BST sufficient")
    logger.info("  • Memory constrained (extra height storage)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()