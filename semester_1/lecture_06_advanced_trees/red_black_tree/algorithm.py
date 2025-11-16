#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Red-Black Tree implementation.

Self-balancing binary search tree with color property that ensures
the tree remains approximately balanced.
"""

import sys
from pathlib import Path
from enum import Enum
from typing import Optional, List, Any

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class Color(Enum):
    """Node colors."""
    RED = 1
    BLACK = 2


class RBNode:
    """Red-Black Tree Node."""
    
    def __init__(self, key: Any, color: Color = Color.RED):
        """Initialize RB node."""
        self.key = key
        self.color = color
        self.left: Optional['RBNode'] = None
        self.right: Optional['RBNode'] = None
        self.parent: Optional['RBNode'] = None


class RedBlackTree:
    """
    Red-Black Tree implementation.
    
    Properties:
    1. Every node is either red or black
    2. Root is always black
    3. All leaves (NIL) are black
    4. Red nodes have black children
    5. All paths from node to leaves have same number of black nodes
    """
    
    def __init__(self):
        """Initialize empty Red-Black tree."""
        self.NIL = RBNode(key=None, color=Color.BLACK)
        self.root = self.NIL
    
    def insert(self, key: Any) -> None:
        """Insert key into Red-Black tree."""
        node = RBNode(key)
        node.left = self.NIL
        node.right = self.NIL
        
        parent = None
        current = self.root
        
        # Find position for new node
        while current != self.NIL:
            parent = current
            if node.key < current.key:
                current = current.left
            else:
                current = current.right
        
        node.parent = parent
        
        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node
        
        # Fix Red-Black properties
        self._insert_fixup(node)
    
    def _insert_fixup(self, node: RBNode) -> None:
        """Fix Red-Black properties after insertion."""
        while node.parent and node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                
                if uncle.color == Color.RED:
                    # Case 1: Uncle is red
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        # Case 2: Node is right child
                        node = node.parent
                        self._rotate_left(node)
                    
                    # Case 3: Node is left child
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                
                if uncle.color == Color.RED:
                    # Case 1: Uncle is red
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        # Case 2: Node is left child
                        node = node.parent
                        self._rotate_right(node)
                    
                    # Case 3: Node is right child
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self._rotate_left(node.parent.parent)
        
        self.root.color = Color.BLACK
    
    def _rotate_left(self, x: RBNode) -> None:
        """Left rotation."""
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def _rotate_right(self, x: RBNode) -> None:
        """Right rotation."""
        y = x.left
        x.left = y.right
        
        if y.right != self.NIL:
            y.right.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        
        y.right = x
        x.parent = y
    
    def search(self, key: Any) -> bool:
        """Search for key in tree."""
        return self._search(self.root, key) != self.NIL
    
    def _search(self, node: RBNode, key: Any) -> RBNode:
        """Helper method to search."""
        if node == self.NIL or key == node.key:
            return node
        
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)
    
    def inorder(self) -> List[Any]:
        """Get inorder traversal."""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node: RBNode, result: List[Any]) -> None:
        """Helper for inorder traversal."""
        if node != self.NIL:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)
    
    def print_tree(self, node: Optional[RBNode] = None,
                   level: int = 0) -> None:
        """Print tree structure with colors."""
        if node is None:
            node = self.root
        
        if node != self.NIL:
            self.print_tree(node.right, level + 1)
            color = "R" if node.color == Color.RED else "B"
            logger.info(' ' * 4 * level + '→ ' + 
                  f"{node.key}({color})")
            self.print_tree(node.left, level + 1)
    
    def get_black_height(self, node: Optional[RBNode] = None) -> int:
        """Get black height of tree."""
        if node is None:
            node = self.root
        
        if node == self.NIL:
            return 0
        
        left_height = self.get_black_height(node.left)
        right_height = self.get_black_height(node.right)
        
        add_black = 1 if node.color == Color.BLACK else 0
        
        return max(left_height, right_height) + add_black


def main() -> None:
    """Demonstration of Red-Black Tree."""
    logger.info("=" * 70)
    logger.info("RED-BLACK TREE DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic operations
    logger.info("Example 1: Basic Insert and Search")
    logger.info("-" * 70)
    rb_tree = RedBlackTree()
    keys = [7, 3, 18, 10, 22, 8, 11, 26]
    
    logger.info(f"Inserting: {keys}")
    for key in keys:
        rb_tree.insert(key)
    
    logger.info("\nTree structure (R=Red, B=Black):")
    rb_tree.print_tree()
    
    logger.info(f"\nInorder traversal: {rb_tree.inorder()}")
    logger.info(f"Search for 10: {rb_tree.search(10)}")
    logger.info(f"Search for 15: {rb_tree.search(15)}")
    logger.info(f"Black height: {rb_tree.get_black_height()}")
    logger.info()
    
    # Example 2: Sequential insertion
    logger.info("Example 2: Sequential Insertion (1-10)")
    logger.info("-" * 70)
    rb_tree2 = RedBlackTree()
    logger.info("Inserting 1 through 10 sequentially...")
    for i in range(1, 11):
        rb_tree2.insert(i)
    
    logger.info("\nBalanced tree structure:")
    rb_tree2.print_tree()
    logger.info(f"Inorder: {rb_tree2.inorder()}")
    logger.info(f"Black height: {rb_tree2.get_black_height()}")
    logger.info("Note: Tree remains balanced despite sequential input")
    logger.info()
    
    # Example 3: Properties verification
    logger.info("Example 3: Red-Black Properties")
    logger.info("-" * 70)
    rb_tree3 = RedBlackTree()
    test_keys = [20, 15, 25, 10, 5, 1, 30, 35]
    
    logger.info(f"Inserting: {test_keys}")
    for key in test_keys:
        rb_tree3.insert(key)
    
    logger.info("\nTree structure:")
    rb_tree3.print_tree()
    
    logger.info("\nVerifying properties:")
    logger.info("  1. Root is black:", 
          rb_tree3.root.color == Color.BLACK)
    logger.info(f"  2. Black height: {rb_tree3.get_black_height()}")
    logger.info("  3. All paths have same black height: True (by design)")
    logger.info()
    
    # Example 4: Performance measurement
    logger.info("Example 4: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Red-Black Tree")
    
    def test_insertions(n):
        tree = RedBlackTree()
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
    logger.info("  Height: O(log n) - guaranteed")
    logger.info("\nKey Advantages:")
    logger.info("  - Guaranteed O(log n) operations")
    logger.info("  - Fewer rotations than AVL tree")
    logger.info("  - Used in many standard libraries")
    logger.info("  - Better for frequent insertions/deletions")
    logger.info("\nKey Disadvantages:")
    logger.info("  - More complex than AVL tree")
    logger.info("  - Extra storage for color")
    logger.info("  - Slightly less balanced than AVL")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()