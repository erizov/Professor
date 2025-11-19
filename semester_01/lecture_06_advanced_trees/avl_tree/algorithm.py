#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Avl Tree implementation.

This file contains the implementation of the Avl Tree algorithm.
"""

from typing import List, Optional, Dict, Set


class AVLNode:
    """Node in AVL tree."""

    def __init__(self, val: int):
        self.val = val
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height = 1


class AVLTree:
    """AVL tree (self-balancing BST) implementation."""

    def __init__(self):
        self.root: Optional[AVLNode] = None

    def _height(self, node: Optional[AVLNode]) -> int:
        """Get height of node."""
        return node.height if node else 0

    def _balance_factor(self, node: AVLNode) -> int:
        """Get balance factor."""
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node: AVLNode) -> None:
        """Update height of node."""
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """Right rotation."""
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self._update_height(y)
        self._update_height(x)

        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """Left rotation."""
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self._update_height(x)
        self._update_height(y)

        return y

    def insert(self, val: int) -> None:
        """Insert value."""
        self.root = self._insert(self.root, val)

    def _insert(self, node: Optional[AVLNode], val: int) -> AVLNode:
        """Insert helper."""
        if not node:
            return AVLNode(val)

        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        else:
            return node

        self._update_height(node)
        balance = self._balance_factor(node)

        # Left Left
        if balance > 1 and val < node.left.val:
            return self._rotate_right(node)

        # Right Right
        if balance < -1 and val > node.right.val:
            return self._rotate_left(node)

        # Left Right
        if balance > 1 and val > node.left.val:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        # Right Left
        if balance < -1 and val < node.right.val:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def search(self, val: int) -> bool:
        """Search for value."""
        return self._search(self.root, val)

    def _search(self, node: Optional[AVLNode], val: int) -> bool:
        """Search helper."""
        if not node:
            return False
        if val == node.val:
            return True
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)


def main() -> None:
    """Demonstrate Avl Tree."""
    print("=" * 70)
    print("AVL TREE")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Avl Tree")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
