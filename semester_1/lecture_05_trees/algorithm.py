#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trees - Demonstration.

This lecture covers tree data structures including
binary trees, binary search trees, and AVL trees.
"""

from typing import Optional


class TreeNode:
    """Binary tree node."""
    
    def __init__(self, val: int = 0):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None


def inorder_traversal(root: Optional[TreeNode]) -> list:
    """Inorder traversal of binary tree."""
    result = []
    if root:
        result.extend(inorder_traversal(root.left))
        result.append(root.val)
        result.extend(inorder_traversal(root.right))
    return result


def main() -> None:
    """Demonstrate tree algorithms."""
    print("=" * 70)
    print("TREES")
    print("=" * 70)
    
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    result = inorder_traversal(root)
    print(f"Inorder traversal: {result}")
    print("=" * 70)


if __name__ == "__main__":
    main()
