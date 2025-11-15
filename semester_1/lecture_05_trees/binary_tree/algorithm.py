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
    print("=" * 70)
    print("BINARY TREE DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic operations
    print("Example 1: Building a Binary Tree")
    print("-" * 70)
    
    tree = BinaryTree()
    values = [1, 2, 3, 4, 5, 6, 7]
    
    print(f"Inserting values: {values}")
    for val in values:
        tree.insert(val)
    
    print(f"Tree size: {tree.size()}")
    print(f"Tree height: {tree.height()}")
    print()
    
    # Example 2: Traversals
    print("Example 2: Tree Traversals")
    print("-" * 70)
    
    print(f"Inorder:     {tree.inorder_traversal()}")
    print(f"Preorder:    {tree.preorder_traversal()}")
    print(f"Postorder:   {tree.postorder_traversal()}")
    print(f"Level-order: {tree.levelorder_traversal()}")
    print()
    
    # Example 3: Search
    print("Example 3: Searching")
    print("-" * 70)
    
    search_values = [5, 10, 1, 8]
    for val in search_values:
        found = tree.search(val)
        print(f"Search {val}: {'Found' if found else 'Not found'}")
    print()
    
    # Example 4: Larger tree
    print("Example 4: Larger Tree")
    print("-" * 70)
    
    tree2 = BinaryTree()
    values2 = list(range(1, 16))
    
    for val in values2:
        tree2.insert(val)
    
    print(f"Inserted {len(values2)} values")
    print(f"Size: {tree2.size()}")
    print(f"Height: {tree2.height()}")
    print(f"Level-order: {tree2.levelorder_traversal()}")
    print()
    
    # Example 5: Performance measurement
    print("Example 5: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Binary Tree")
    
    sizes = [100, 500, 1000]
    for size in sizes:
        tree_perf = BinaryTree()
        values_perf = list(range(size))
        
        def insert_all():
            for val in values_perf:
                tree_perf.insert(val)
        
        _, metrics = timer.measure(insert_all)
        
        print(f"n={size:4d}: Insert {metrics['execution_time_ms']:8.3f} ms, "
              f"{metrics['memory_peak_kb']:8.2f} KB")
    
    print()
    timer.print_summary()
    
    print("\n" + "=" * 70)
    print("\nComplexity Summary:")
    print("  Insertion: O(n) - level-order")
    print("  Search: O(n) - must check all nodes")
    print("  Traversal: O(n)")
    print("  Height: O(n)")
    print("  Space: O(n) - storing nodes")
    print("\nKey Points:")
    print("  + Simple hierarchical structure")
    print("  + Foundation for other trees")
    print("  + Natural recursive operations")
    print("  + Good for hierarchical data")
    print("  - No ordering guarantee")
    print("  - Search is O(n)")
    print("  - Can become unbalanced")
    print("\nWhen to use:")
    print("  • Hierarchical data")
    print("  • Expression trees")
    print("  • Decision trees")
    print("  • File systems")
    print("\nCommon Applications:")
    print("  • Binary heap")
    print("  • Binary search tree")
    print("  • Expression parsing")
    print("  • Huffman coding")
    print("=" * 70)


if __name__ == "__main__":
    main()
