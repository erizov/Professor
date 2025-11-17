#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Iterator Design Pattern.

Provides a way to access elements of an aggregate object sequentially
without exposing its underlying representation.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Optional
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Iterator Interface
class Iterator(ABC):
    """Iterator interface."""
    
    @abstractmethod
    def has_next(self) -> bool:
        """Check if there are more elements."""
        
    """
    Iterator implementation.
    
    Args:
        *args: Variable arguments
        **kwargs: Keyword arguments
        
    Returns:
        Algorithm result
    """
    # Implementation for iterator
    logger.info(f"Executing iterator")
    return None


def main() -> None:
    """Demonstration of Iterator Pattern."""
    logger.info("=" * 70)
    logger.info("ITERATOR DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Book Collection
    logger.info("Example 1: Book Collection Iterator")
    logger.info("-" * 70)
    
    collection = BookCollection()
    collection.add_book("Design Patterns")
    collection.add_book("Clean Code")
    collection.add_book("Refactoring")
    
    iterator = collection.create_iterator()
    logger.info("Books in collection:")
    while iterator.has_next():
        book = iterator.next()
        logger.info(f"  - {book}")
    logger.info()
    
    # Example 2: Tree Iterator
    logger.info("Example 2: Binary Tree Iterator")
    logger.info("-" * 70)
    
    # Create tree:     4
    #                 / \
    #                2   6
    #               / \ / \
    #              1  3 5  7
    root = TreeNode(4)
    root.left = TreeNode(2)
    root.right = TreeNode(6)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(7)
    
    tree = BinaryTree(root)
    tree_iterator = tree.create_iterator()
    
    logger.info("In-order traversal:")
    values = []
    while tree_iterator.has_next():
        values.append(tree_iterator.next())
    logger.info(f"  {values}")
    logger.info()
    
    # Example 3: Python Iterator Protocol
    logger.info("Example 3: Python Iterator Protocol")
    logger.info("-" * 70)
    
    number_range = NumberRange(1, 10, 2)
    logger.debug("Numbers from 1 to 10 (step 2):")
    for num in number_range:
        logger.info(f"  {num}", end=" ")
    logger.info("\n")
    
    # Example 4: Using built-in iterators
    logger.info("Example 4: Built-in Python Iterators")
    logger.info("-" * 70)
    
    data = [1, 2, 3, 4, 5]
    iterator = iter(data)
    
    logger.info("Iterating over list:")
    try:
        while True:
            value = next(iterator)
            logger.info(f"  {value}", end=" ")
    except StopIteration:
        pass
    logger.info("\n")
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Provide a way to access elements of an aggregate object")
    logger.info("  sequentially without exposing its underlying representation.")
    logger.info("\nKey Advantages:")
    logger.info("  - Supports multiple traversal methods")
    logger.info("  - Simplifies aggregate interface")
    logger.info("  - Allows multiple iterators on same aggregate")
    logger.info("  - Encapsulates traversal logic")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Can be overkill for simple collections")
    logger.info("  - Adds complexity")
    logger.info("\nWhen to Use:")
    logger.info("  - Need to traverse aggregate in different ways")
    logger.info("  - Want to hide aggregate's internal structure")
    logger.info("  - Need multiple iterators on same aggregate")
    logger.info("  - Lazy evaluation needed")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Collections (lists, trees, graphs)")
    logger.info("  - Database result sets")
    logger.info("  - File system traversal")
    logger.info("  - Stream processing")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()