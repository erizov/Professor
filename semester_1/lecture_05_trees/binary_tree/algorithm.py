#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binary Tree implementation.

This file contains the implementation of the Binary Tree algorithm.
"""

from typing import List, Optional, Dict, Set


class TreeNode:
    """Binary tree node."""
    def __init__(self, val: int = 0):
        self.val = val
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None

def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Inorder traversal of binary tree."""
    result = []
    if root:
        result.extend(inorder_traversal(root.left))
        result.append(root.val)
        result.extend(inorder_traversal(root.right))
    return result

def preorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Preorder traversal of binary tree."""
    result = []
    if root:
        result.append(root.val)
        result.extend(preorder_traversal(root.left))
        result.extend(preorder_traversal(root.right))
    return result

def postorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """Postorder traversal of binary tree."""
    result = []
    if root:
        result.extend(postorder_traversal(root.left))
        result.extend(postorder_traversal(root.right))
        result.append(root.val)
    return result


def main() -> None:
    """Demonstrate Binary Tree."""
    print("=" * 70)
    print("BINARY TREE")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Binary Tree")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
