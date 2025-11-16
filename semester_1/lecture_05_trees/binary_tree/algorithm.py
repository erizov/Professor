#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binary Tree implementation.

Basic tree data structure where each node has at most two children.
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
    """Node in a binary tree."""
    
    def __init__(self, val: int):
        """
        Initialize tree node.
        
        Args:
            val: Value of the node
        """
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None


class BinaryTree:
    """
    Binary Tree implementation.
    
    Supports insertion, traversals, and basic operations.
    """
    
    def __init__(self):
        """Initialize empty binary tree."""
        self.root: Optional[TreeNode] = None
    
    def insert(self, val: int) -> None:
        """
        Insert value into tree (level-order insertion).
        
        Args:
            val: Value to insert
            
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        if not self.root:
            self.root = TreeNode(val)
            return
        
        # Level-order insertion using queue
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            
            if not node.left:
                node.left = TreeNode(val)
                return
            else:
                queue.append(node.left)
            
            if not node.right:
                node.right = TreeNode(val)
                return
            else:
                queue.append(node.right)
    
    def inorder_traversal(self, node: Optional[TreeNode] = None,
                         result: Optional[List[int]] = None) -> List[int]:
        """
        Inorder traversal (Left-Root-Right).
        
        Args:
            node: Starting node (default: root)
            result: List to store results
            
        Returns:
            List of values in inorder
            
        Time Complexity: O(n)
        Space Complexity: O(h) where h is height
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.val)
            self.inorder_traversal(node.right, result)
        
        return result
    
    def preorder_traversal(self, node: Optional[TreeNode] = None,
                          result: Optional[List[int]] = None) -> List[int]:
        """
        Preorder traversal (Root-Left-Right).
        
        Time Complexity: O(n)
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        if node:
            result.append(node.val)
            self.preorder_traversal(node.left, result)
            self.preorder_traversal(node.right, result)
        
        return result
    
    def postorder_traversal(self, node: Optional[TreeNode] = None,
                           result: Optional[List[int]] = None) -> List[int]:
        """
        Postorder traversal (Left-Right-Root).
        
        Time Complexity: O(n)
        """
        if result is None:
            result = []
        if node is None:
            node = self.root
        
        if node:
            self.postorder_traversal(node.left, result)
            self.postorder_traversal(node.right, result)
            result.append(node.val)
        
        return result
    
    def levelorder_traversal(self) -> List[int]:
        """
        Level-order traversal (BFS).
        
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        if not self.root:
            return []
        
        result = []
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return result
    
    def height(self, node: Optional[TreeNode] = None) -> int:
        """
        Calculate height of tree.
        
        Time Complexity: O(n)
        """
        if node is None:
            node = self.root
        
        if not node:
            return 0
        
        left_height = self.height(node.left)
        right_height = self.height(node.right)
        
        return max(left_height, right_height) + 1
    
    def size(self, node: Optional[TreeNode] = None) -> int:
        """
        Count number of nodes.
        
        Time Complexity: O(n)
        """
        if node is None:
            node = self.root
        
        if not node:
            return 0
        
        return 1 + self.size(node.left) + self.size(node.right)
    
    def search(self, val: int, node: Optional[TreeNode] = None) -> bool:
        """
        Search for value in tree.
        
        Time Complexity: O(n)
        """
        if node is None:
            node = self.root
        
        if not node:
            return False
        
        if node.val == val:
            return True
        
        return (self.search(val, node.left) or 
                self.search(val, node.right))


def main() -> None:
    """Demonstration of Binary Tree."""
    logger.info("=" * 70)
    logger.info("BINARY TREE DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic operations
    logger.info("Example 1: Building a Binary Tree")
    logger.info("-" * 70)
    
    tree = BinaryTree()
    values = [1, 2, 3, 4, 5, 6, 7]
    
    logger.info(f"Inserting values: {values}")
    for val in values:
        tree.insert(val)
    
    logger.info(f"Tree size: {tree.size()}")
    logger.info(f"Tree height: {tree.height()}")
    logger.info()
    
    # Example 2: Traversals
    logger.info("Example 2: Tree Traversals")
    logger.info("-" * 70)
    
    logger.info(f"Inorder:     {tree.inorder_traversal()}")
    logger.info(f"Preorder:    {tree.preorder_traversal()}")
    logger.info(f"Postorder:   {tree.postorder_traversal()}")
    logger.info(f"Level-order: {tree.levelorder_traversal()}")
    logger.info()
    
    # Example 3: Search
    logger.info("Example 3: Searching")
    logger.info("-" * 70)
    
    search_values = [5, 10, 1, 8]
    for val in search_values:
        found = tree.search(val)
        logger.info(f"Search {val}: {'Found' if found else 'Not found'}")
    logger.info()
    
    # Example 4: Larger tree
    logger.info("Example 4: Larger Tree")
    logger.info("-" * 70)
    
    tree2 = BinaryTree()
    values2 = list(range(1, 16))
    
    for val in values2:
        tree2.insert(val)
    
    logger.info(f"Inserted {len(values2)} values")
    logger.info(f"Size: {tree2.size()}")
    logger.info(f"Height: {tree2.height()}")
    logger.info(f"Level-order: {tree2.levelorder_traversal()}")
    logger.info()
    
    # Example 5: Performance measurement
    logger.info("Example 5: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Binary Tree")
    
    sizes = [100, 500, 1000]
    for size in sizes:
        tree_perf = BinaryTree()
        values_perf = list(range(size))
        
        def insert_all():
            for val in values_perf:
                tree_perf.insert(val)
        
        _, metrics = timer.measure(insert_all)
        
        logger.info(f"n={size:4d}: Insert {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    logger.info()
    timer.print_summary()
    
    logger.info("\n" + "=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Insertion: O(n) - level-order")
    logger.info("  Search: O(n) - must check all nodes")
    logger.info("  Traversal: O(n)")
    logger.info("  Height: O(n)")
    logger.info("  Space: O(n) - storing nodes")
    logger.info("\nKey Points:")
    logger.info("  + Simple hierarchical structure")
    logger.info("  + Foundation for other trees")
    logger.info("  + Natural recursive operations")
    logger.info("  + Good for hierarchical data")
    logger.info("  - No ordering guarantee")
    logger.info("  - Search is O(n)")
    logger.info("  - Can become unbalanced")
    logger.info("\nWhen to use:")
    logger.info("  • Hierarchical data")
    logger.info("  • Expression trees")
    logger.info("  • Decision trees")
    logger.info("  • File systems")
    logger.info("\nCommon Applications:")
    logger.info("  • Binary heap")
    logger.info("  • Binary search tree")
    logger.info("  • Expression parsing")
    logger.info("  • Huffman coding")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()