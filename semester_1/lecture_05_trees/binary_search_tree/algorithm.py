#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binary Search Tree (BST) implementation.

Ordered binary tree where left subtree < node < right subtree.
"""

import sys
from pathlib import Path
from typing import Optional, List
import random

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class TreeNode:
    """Node in a BST."""
    
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None


class BST:
    """
    Binary Search Tree implementation.
    
    Maintains BST property: left < node < right
    """
    
    def __init__(self):
        """Initialize empty BST."""
        self.root: Optional[TreeNode] = None
    
    def insert(self, val: int) -> None:
        """
        Insert value into BST.
        
        Time Complexity: O(h) where h is height
        Best: O(log n), Worst: O(n) for skewed tree
        """
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert_recursive(self.root, val)
    
    def _insert_recursive(self, node: TreeNode, val: int) -> TreeNode:
        """Helper for recursive insertion."""
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self._insert_recursive(node.left, val)
        else:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self._insert_recursive(node.right, val)
        return node
    
    def search(self, val: int) -> bool:
        """
        Search for value in BST.
        
        Time Complexity: O(h)
        """
        return self._search_recursive(self.root, val)
    
    def _search_recursive(self, node: Optional[TreeNode], 
                         val: int) -> bool:
        """Helper for recursive search."""
        if node is None:
            return False
        
        if val == node.val:
            return True
        elif val < node.val:
            return self._search_recursive(node.left, val)
        else:
            return self._search_recursive(node.right, val)
    
    def delete(self, val: int) -> None:
        """
        Delete value from BST.
        
        Time Complexity: O(h)
        """
        self.root = self._delete_recursive(self.root, val)
    
    def _delete_recursive(self, node: Optional[TreeNode], 
                         val: int) -> Optional[TreeNode]:
        """Helper for recursive deletion."""
        if node is None:
            return None
        
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            # Node to delete found
            # Case 1: No children
            if node.left is None and node.right is None:
                return None
            
            # Case 2: One child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            
            # Case 3: Two children
            # Find inorder successor (min in right subtree)
            min_node = self._find_min(node.right)
            node.val = min_node.val
            node.right = self._delete_recursive(node.right, min_node.val)
        
        return node
    
    def _find_min(self, node: TreeNode) -> TreeNode:
        """Find minimum value node in subtree."""
        while node.left:
            node = node.left
        return node
    
    def _find_max(self, node: TreeNode) -> TreeNode:
        """Find maximum value node in subtree."""
        while node.right:
            node = node.right
        return node
    
    def inorder(self, node: Optional[TreeNode] = None,
               result: Optional[List[int]] = None) -> List[int]:
        """
        Inorder traversal (gives sorted order).
        
        Time Complexity: O(n)
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        if node:
            self.inorder(node.left, result)
            result.append(node.val)
            self.inorder(node.right, result)
        
        return result
    
    def height(self, node: Optional[TreeNode] = None) -> int:
        """Calculate height of tree."""
        if node is None:
            node = self.root
        
        if not node:
            return 0
        
        return max(self.height(node.left), self.height(node.right)) + 1
    
    def size(self, node: Optional[TreeNode] = None) -> int:
        """Count number of nodes."""
        if node is None:
            node = self.root
        
        if not node:
            return 0
        
        return 1 + self.size(node.left) + self.size(node.right)
    
    def find_min(self) -> Optional[int]:
        """Find minimum value in tree."""
        if not self.root:
            return None
        node = self._find_min(self.root)
        return node.val
    
    def find_max(self) -> Optional[int]:
        """Find maximum value in tree."""
        if not self.root:
            return None
        node = self._find_max(self.root)
        return node.val


def main() -> None:
    """Demonstration of Binary Search Tree."""
    logger.info("=" * 70)
    logger.info("BINARY SEARCH TREE DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic operations
    logger.info("Example 1: Building a BST")
    logger.info("-" * 70)
    
    bst = BST()
    values = [50, 30, 70, 20, 40, 60, 80]
    
    logger.info(f"Inserting values: {values}")
    for val in values:
        bst.insert(val)
    
    logger.info(f"Size: {bst.size()}")
    logger.info(f"Height: {bst.height()}")
    logger.info(f"Inorder (sorted): {bst.inorder()}")
    logger.info(f"Min value: {bst.find_min()}")
    logger.info(f"Max value: {bst.find_max()}")
    logger.info()
    
    # Example 2: Search
    logger.info("Example 2: Searching")
    logger.info("-" * 70)
    
    search_values = [40, 25, 70, 100]
    for val in search_values:
        found = bst.search(val)
        logger.info(f"Search {val}: {'Found' if found else 'Not found'}")
    logger.info()
    
    # Example 3: Deletion
    logger.info("Example 3: Deletion")
    logger.info("-" * 70)
    
    logger.info(f"Before deletion: {bst.inorder()}")
    
    # Delete leaf node
    bst.delete(20)
    logger.info(f"After deleting 20 (leaf): {bst.inorder()}")
    
    # Delete node with one child
    bst.delete(30)
    logger.info(f"After deleting 30 (one child): {bst.inorder()}")
    
    # Delete node with two children
    bst.delete(50)
    logger.info(f"After deleting 50 (two children): {bst.inorder()}")
    logger.info()
    
    # Example 4: Balanced vs Unbalanced
    logger.info("Example 4: Balanced vs Unbalanced Trees")
    logger.info("-" * 70)
    
    # Balanced insertion
    balanced = BST()
    balanced_vals = [50, 25, 75, 12, 37, 62, 87]
    for val in balanced_vals:
        balanced.insert(val)
    
    logger.info(f"Balanced BST: {balanced_vals}")
    logger.info(f"  Height: {balanced.height()}")
    logger.info(f"  Sorted: {balanced.inorder()}")
    
    # Unbalanced insertion (sorted order)
    unbalanced = BST()
    unbalanced_vals = [1, 2, 3, 4, 5, 6, 7]
    for val in unbalanced_vals:
        unbalanced.insert(val)
    
    logger.info(f"\nUnbalanced BST: {unbalanced_vals}")
    logger.info(f"  Height: {unbalanced.height()} (becomes a linked list!)")
    logger.info(f"  Sorted: {unbalanced.inorder()}")
    logger.info()
    
    # Example 5: Performance measurement
    logger.info("Example 5: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("BST")
    
    logger.info("Random insertion (balanced):")
    sizes = [100, 500, 1000]
    for size in sizes:
        bst_perf = BST()
        values_perf = list(range(size))
        random.shuffle(values_perf)
        
        def insert_all():
            for val in values_perf:
                bst_perf.insert(val)
        
        _, metrics = timer.measure(insert_all)
        
        logger.info(f"n={size:4d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"height={bst_perf.height()}")
    
    logger.info()
    timer.print_summary()
    
    logger.info("\n" + "=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Search:    O(h) - h is height")
    logger.info("  Insert:    O(h)")
    logger.info("  Delete:    O(h)")
    logger.info("  Min/Max:   O(h)")
    logger.info("  Traversal: O(n)")
    logger.info("\nBalanced tree: h = O(log n)")
    logger.info("Unbalanced tree: h = O(n) (worst case)")
    logger.info("\nKey Points:")
    logger.info("  + Fast search, insert, delete (if balanced)")
    logger.info("  + Inorder traversal gives sorted order")
    logger.info("  + Simple to implement")
    logger.info("  + Dynamic size")
    logger.info("  - Can become unbalanced")
    logger.info("  - No balancing guarantee")
    logger.info("  - Worst case O(n) operations")
    logger.info("\nWhen to use:")
    logger.info("  • Need sorted data")
    logger.info("  • Dynamic insertions/deletions")
    logger.info("  • Range queries")
    logger.info("  • Don't need guaranteed balance")
    logger.info("\nWhen NOT to use:")
    logger.info("  • Need guaranteed O(log n) (use AVL/Red-Black)")
    logger.info("  • Sorted input (becomes unbalanced)")
    logger.info("  • Need frequent rotations")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()