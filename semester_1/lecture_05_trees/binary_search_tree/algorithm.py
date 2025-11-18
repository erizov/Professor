#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binary Search Tree implementation.

This file contains the implementation of the Binary Search Tree algorithm.
"""

from typing import List, Optional, Dict, Set


class BSTNode:
    """Binary Search Tree node."""
    def __init__(self, val: int):
        self.val = val
        self.left: Optional['BSTNode'] = None
        self.right: Optional['BSTNode'] = None

class BinarySearchTree:
    """Binary Search Tree implementation."""
    def __init__(self):
        self.root: Optional[BSTNode] = None
    
    def insert(self, val: int) -> None:
        """Insert value into BST."""
        self.root = self._insert(self.root, val)
    
    def _insert(self, root: Optional[BSTNode], val: int) -> BSTNode:
        if root is None:
            return BSTNode(val)
        if val < root.val:
            root.left = self._insert(root.left, val)
        elif val > root.val:
            root.right = self._insert(root.right, val)
        return root
    
    def search(self, val: int) -> bool:
        """Search for value in BST."""
        return self._search(self.root, val)
    
    def _search(self, root: Optional[BSTNode], val: int) -> bool:
        if root is None:
            return False
        if root.val == val:
            return True
        elif val < root.val:
            return self._search(root.left, val)
        else:
            return self._search(root.right, val)


def main() -> None:
    """Demonstrate Binary Search Tree."""
    print("=" * 70)
    print("BINARY SEARCH TREE")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Binary Search Tree")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
