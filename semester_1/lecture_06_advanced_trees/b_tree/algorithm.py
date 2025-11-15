#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B-Tree implementation.

Self-balancing search tree optimized for systems that read/write large blocks
of data (databases, file systems).
"""

import sys
from pathlib import Path
from typing import List, Optional, Any

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class BTreeNode:
    """Node in B-Tree."""
    
    def __init__(self, leaf: bool = False):
        """Initialize B-Tree node."""
        self.keys: List[Any] = []
        self.children: List['BTreeNode'] = []
        self.leaf = leaf
    
    def split(self, parent: 'BTreeNode', index: int) -> None:
        """Split this node and update parent."""
        new_node = BTreeNode(leaf=self.leaf)
        mid_index = len(self.keys) // 2
        
        # Move second half of keys to new node
        new_node.keys = self.keys[mid_index + 1:]
        self.keys = self.keys[:mid_index]
        
        # Move children if not leaf
        if not self.leaf:
            new_node.children = self.children[mid_index + 1:]
            self.children = self.children[:mid_index + 1]
        
        # Move middle key to parent
        parent.keys.insert(index, self.keys[mid_index])
        parent.children.insert(index + 1, new_node)


class BTree:
    """
    B-Tree implementation.
    
    Properties:
    - All leaves at same level
    - Minimum degree t (t >= 2)
    - Every node (except root) has at least t-1 keys
    - Every node has at most 2t-1 keys
    - Number of children = number of keys + 1
    """
    
    def __init__(self, t: int = 3):
        """
        Initialize B-Tree.
        
        Args:
            t: Minimum degree (minimum keys per node = t-1)
        """
        self.root = BTreeNode(leaf=True)
        self.t = t  # Minimum degree
    
    def search(self, key: Any, node: Optional[BTreeNode] = None) -> bool:
        """
        Search for key in B-Tree.
        
        Args:
            key: Key to search for
            node: Node to start search from
            
        Returns:
            True if key found, False otherwise
        """
        if node is None:
            node = self.root
        
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        if i < len(node.keys) and key == node.keys[i]:
            return True
        
        if node.leaf:
            return False
        
        return self.search(key, node.children[i])
    
    def insert(self, key: Any) -> None:
        """Insert key into B-Tree."""
        root = self.root
        
        # If root is full, split it
        if len(root.keys) >= 2 * self.t - 1:
            new_root = BTreeNode()
            new_root.children.append(self.root)
            self.root = new_root
            root.split(new_root, 0)
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)
    
    def _insert_non_full(self, node: BTreeNode, key: Any) -> None:
        """Insert key into non-full node."""
        i = len(node.keys) - 1
        
        if node.leaf:
            # Insert key in sorted position
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            # Find child to insert into
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            
            # Split child if full
            if len(node.children[i].keys) >= 2 * self.t - 1:
                node.children[i].split(node, i)
                if key > node.keys[i]:
                    i += 1
            
            self._insert_non_full(node.children[i], key)
    
    def print_tree(self, node: Optional[BTreeNode] = None,
                   level: int = 0) -> None:
        """Print tree structure."""
        if node is None:
            node = self.root
        
        print(' ' * 4 * level + '→ ' + str(node.keys))
        
        if not node.leaf:
            for child in node.children:
                self.print_tree(child, level + 1)
    
    def inorder(self, node: Optional[BTreeNode] = None) -> List[Any]:
        """Get inorder traversal."""
        if node is None:
            node = self.root
        
        result = []
        
        for i in range(len(node.keys)):
            if not node.leaf:
                result.extend(self.inorder(node.children[i]))
            result.append(node.keys[i])
        
        if not node.leaf:
            result.extend(self.inorder(node.children[-1]))
        
        return result


def main() -> None:
    """Demonstration of B-Tree."""
    print("=" * 70)
    print("B-TREE DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic operations
    print("Example 1: Basic Insert and Search (t=3)")
    print("-" * 70)
    btree = BTree(t=3)
    keys = [10, 20, 5, 6, 12, 30, 7, 17]
    
    print(f"Inserting: {keys}")
    for key in keys:
        btree.insert(key)
    
    print("\nTree structure:")
    btree.print_tree()
    
    print(f"\nInorder traversal: {btree.inorder()}")
    print(f"Search for 12: {btree.search(12)}")
    print(f"Search for 15: {btree.search(15)}")
    print()
    
    # Example 2: More insertions to show splitting
    print("Example 2: Node Splitting (t=2)")
    print("-" * 70)
    btree2 = BTree(t=2)
    keys2 = list(range(1, 11))
    
    print(f"Inserting: {keys2}")
    for key in keys2:
        btree2.insert(key)
        print(f"  After inserting {key}:")
        btree2.print_tree()
        print()
    
    print("Final inorder:", btree2.inorder())
    print()
    
    # Example 3: Larger tree
    print("Example 3: Larger Tree (t=3)")
    print("-" * 70)
    btree3 = BTree(t=3)
    keys3 = [i for i in range(1, 21)]
    
    print(f"Inserting: {keys3}")
    for key in keys3:
        btree3.insert(key)
    
    print("\nTree structure:")
    btree3.print_tree()
    print(f"\nInorder: {btree3.inorder()}")
    print()
    
    # Example 4: Performance
    print("Example 4: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("B-Tree")
    
    def test_insertions(n, t=3):
        tree = BTree(t=t)
        for i in range(n):
            tree.insert(i)
        return tree
    
    _, metrics_100 = timer.measure(test_insertions, 100)
    print(f"100 insertions:")
    print(f"  Time: {metrics_100['execution_time_ms']:.3f} ms")
    
    _, metrics_1000 = timer.measure(test_insertions, 1000)
    print(f"\n1,000 insertions:")
    print(f"  Time: {metrics_1000['execution_time_ms']:.3f} ms")
    
    print()
    print("=" * 70)
    print("\nComplexity Summary (t = minimum degree):")
    print("  Time:  O(log_t n) - search, insert")
    print("  Space: O(n) - storage")
    print("  Height: O(log_t n)")
    print("\nKey Advantages:")
    print("  - Optimized for disk I/O")
    print("  - Fewer disk reads (wide nodes)")
    print("  - Used in databases and filesystems")
    print("  - Guaranteed logarithmic height")
    print("\nKey Disadvantages:")
    print("  - Complex implementation")
    print("  - Higher space overhead")
    print("  - Not cache-friendly for in-memory")
    print("\nCommon Use Cases:")
    print("  - Database indexes (MySQL InnoDB)")
    print("  - File systems (NTFS, ext4)")
    print("  - Block storage systems")
    print("=" * 70)


if __name__ == "__main__":
    main()
