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
    print("=" * 70)
    print("BINARY SEARCH TREE DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic operations
    print("Example 1: Building a BST")
    print("-" * 70)
    
    bst = BST()
    values = [50, 30, 70, 20, 40, 60, 80]
    
    print(f"Inserting values: {values}")
    for val in values:
        bst.insert(val)
    
    print(f"Size: {bst.size()}")
    print(f"Height: {bst.height()}")
    print(f"Inorder (sorted): {bst.inorder()}")
    print(f"Min value: {bst.find_min()}")
    print(f"Max value: {bst.find_max()}")
    print()
    
    # Example 2: Search
    print("Example 2: Searching")
    print("-" * 70)
    
    search_values = [40, 25, 70, 100]
    for val in search_values:
        found = bst.search(val)
        print(f"Search {val}: {'Found' if found else 'Not found'}")
    print()
    
    # Example 3: Deletion
    print("Example 3: Deletion")
    print("-" * 70)
    
    print(f"Before deletion: {bst.inorder()}")
    
    # Delete leaf node
    bst.delete(20)
    print(f"After deleting 20 (leaf): {bst.inorder()}")
    
    # Delete node with one child
    bst.delete(30)
    print(f"After deleting 30 (one child): {bst.inorder()}")
    
    # Delete node with two children
    bst.delete(50)
    print(f"After deleting 50 (two children): {bst.inorder()}")
    print()
    
    # Example 4: Balanced vs Unbalanced
    print("Example 4: Balanced vs Unbalanced Trees")
    print("-" * 70)
    
    # Balanced insertion
    balanced = BST()
    balanced_vals = [50, 25, 75, 12, 37, 62, 87]
    for val in balanced_vals:
        balanced.insert(val)
    
    print(f"Balanced BST: {balanced_vals}")
    print(f"  Height: {balanced.height()}")
    print(f"  Sorted: {balanced.inorder()}")
    
    # Unbalanced insertion (sorted order)
    unbalanced = BST()
    unbalanced_vals = [1, 2, 3, 4, 5, 6, 7]
    for val in unbalanced_vals:
        unbalanced.insert(val)
    
    print(f"\nUnbalanced BST: {unbalanced_vals}")
    print(f"  Height: {unbalanced.height()} (becomes a linked list!)")
    print(f"  Sorted: {unbalanced.inorder()}")
    print()
    
    # Example 5: Performance measurement
    print("Example 5: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("BST")
    
    print("Random insertion (balanced):")
    sizes = [100, 500, 1000]
    for size in sizes:
        bst_perf = BST()
        values_perf = list(range(size))
        random.shuffle(values_perf)
        
        def insert_all():
            for val in values_perf:
                bst_perf.insert(val)
        
        _, metrics = timer.measure(insert_all)
        
        print(f"n={size:4d}: {metrics['execution_time_ms']:8.3f} ms, "
              f"height={bst_perf.height()}")
    
    print()
    timer.print_summary()
    
    print("\n" + "=" * 70)
    print("\nComplexity Summary:")
    print("  Search:    O(h) - h is height")
    print("  Insert:    O(h)")
    print("  Delete:    O(h)")
    print("  Min/Max:   O(h)")
    print("  Traversal: O(n)")
    print("\nBalanced tree: h = O(log n)")
    print("Unbalanced tree: h = O(n) (worst case)")
    print("\nKey Points:")
    print("  + Fast search, insert, delete (if balanced)")
    print("  + Inorder traversal gives sorted order")
    print("  + Simple to implement")
    print("  + Dynamic size")
    print("  - Can become unbalanced")
    print("  - No balancing guarantee")
    print("  - Worst case O(n) operations")
    print("\nWhen to use:")
    print("  • Need sorted data")
    print("  • Dynamic insertions/deletions")
    print("  • Range queries")
    print("  • Don't need guaranteed balance")
    print("\nWhen NOT to use:")
    print("  • Need guaranteed O(log n) (use AVL/Red-Black)")
    print("  • Sorted input (becomes unbalanced)")
    print("  • Need frequent rotations")
    print("=" * 70)


if __name__ == "__main__":
    main()
