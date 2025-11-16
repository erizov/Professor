#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AVL Tree implementation.

Self-balancing binary search tree where the heights of left and right
subtrees differ by at most 1.
"""

import sys

# Setup logging
logger = logging.getLogger(__name__)
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer

from typing import Optional, List, Any
from framework.logging_utils import get_logger
import logging

logger = get_logger(__name__)


class AVLNode:
    """Node in AVL tree."""
    
    def __init__(self, key: Any):
        """Initialize AVL node."""
        self.key = key
        self.left: Optional['AVLNode'] = None
        self.right: Optional['AVLNode'] = None
        self.height: int = 1


class AVLTree:
    """
    AVL Tree - self-balancing binary search tree.
    
    Maintains balance factor of -1, 0, or 1 for all nodes.
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
            y   C    -->     x   z
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
        
            z                    y
           / \                  / \
          A   y       -->      z   x
             / \              / \
            B   x            A   B
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
    
    def insert(self, key: Any) -> None:
        """Insert key into AVL tree."""
        self.root = self._insert(self.root, key)
    
    def _insert(self, node: Optional[AVLNode], 
                key: Any) -> AVLNode:
        """Helper method to insert key."""
        # Standard BST insertion
        if not node:
            return AVLNode(key)
        
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            # Duplicate keys not allowed
            return node
        
        # Update height
        self.update_height(node)
        
        # Get balance factor
        balance = self.get_balance(node)
        
        # Left-Left case
        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)
        
        # Right-Right case
        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)
        
        # Left-Right case
        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        
        # Right-Left case
        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        
        return node
    
    def delete(self, key: Any) -> None:
        """Delete key from AVL tree."""
        self.root = self._delete(self.root, key)
    
    def _delete(self, node: Optional[AVLNode], 
                key: Any) -> Optional[AVLNode]:
        """Helper method to delete key."""
        if not node:
            return node
        
        # Standard BST deletion
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node with one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            # Node with two children
            # Get inorder successor (smallest in right subtree)
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)
        
        # Update height
        self.update_height(node)
        
        # Get balance factor
        balance = self.get_balance(node)
        
        # Left-Left case
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)
        
        # Left-Right case
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        
        # Right-Right case
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)
        
        # Right-Left case
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        
        return node
    
    def _get_min_value_node(self, node: AVLNode) -> AVLNode:
        """Get node with minimum value."""
        current = node
        while current.left:
            current = current.left
        return current
    
    def search(self, key: Any) -> bool:
        """Search for key in tree."""
        return self._search(self.root, key)
    
    def _search(self, node: Optional[AVLNode], key: Any) -> bool:
        """Helper method to search."""
        if not node:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
    
    def inorder(self) -> List[Any]:
        """Get inorder traversal."""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node: Optional[AVLNode], 
                 result: List[Any]) -> None:
        """Helper for inorder traversal."""
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)
    
    def print_tree(self, node: Optional[AVLNode] = None, 
                   level: int = 0) -> None:
        """Print tree structure."""
        if node is None:
            node = self.root
        
        if node is not None:
            self.print_tree(node.right, level + 1)
            logger.info(' ' * 4 * level + '→ ' + 
                  f"{node.key} (h={node.height})")
            self.print_tree(node.left, level + 1)


def main() -> None:
    """Demonstration of AVL Tree."""
    logger.info("=" * 70)
    logger.info("AVL TREE DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic operations
    logger.info("Example 1: Basic Insert and Search")
    logger.info("-" * 70)
    avl = AVLTree()
    keys = [10, 20, 30, 40, 50, 25]
    
    logger.info(f"Inserting: {keys}")
    for key in keys:
        avl.insert(key)
    
    logger.info("\nTree structure:")
    avl.print_tree()
    
    logger.info(f"\nInorder traversal: {avl.inorder()}")
    logger.info(f"Search for 30: {avl.search(30)}")
    logger.info(f"Search for 35: {avl.search(35)}")
    logger.info()
    
    # Example 2: Deletion
    logger.info("Example 2: Deletion")
    logger.info("-" * 70)
    logger.info("Deleting 10, 30...")
    avl.delete(10)
    avl.delete(30)
    
    logger.info("\nTree structure after deletion:")
    avl.print_tree()
    logger.info(f"Inorder traversal: {avl.inorder()}")
    logger.info()
    
    # Example 3: Left-Left rotation
    logger.info("Example 3: Left-Left Rotation")
    logger.info("-" * 70)
    avl2 = AVLTree()
    logger.info("Inserting 30, 20, 10 (triggers LL rotation)")
    avl2.insert(30)
    avl2.insert(20)
    avl2.insert(10)  # Triggers rotation
    
    logger.info("\nBalanced tree:")
    avl2.print_tree()
    logger.info()
    
    # Example 4: Performance
    logger.info("Example 4: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("AVL Tree")
    
    # Insertions
    def test_insertions(n):
        tree = AVLTree()
        for i in range(n):
            tree.insert(i)
        return tree
    
    _, metrics_100 = timer.measure(test_insertions, 100)
    logger.info(f"100 insertions:")
    logger.info(f"  Time: {metrics_100['execution_time_ms']:.3f} ms")
    
    _, metrics_1000 = timer.measure(test_insertions, 1000)
    logger.info(f"\n1,000 insertions:")
    logger.info(f"  Time: {metrics_1000['execution_time_ms']:.3f} ms")
    
    logger.info()
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Time:  O(log n) - insert, delete, search")
    logger.info("  Space: O(n) - storage")
    logger.info("  Height: O(log n) - guaranteed balanced")
    logger.info("\nKey Advantages:")
    logger.info("  - Guaranteed O(log n) operations")
    logger.info("  - Self-balancing")
    logger.info("  - Better worst-case than BST")
    logger.info("\nKey Disadvantages:")
    logger.info("  - More complex than BST")
    logger.info("  - Extra storage for height")
    logger.info("  - More rotations than Red-Black trees")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()