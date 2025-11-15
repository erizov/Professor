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

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Iterator Interface
class Iterator(ABC):
    """Iterator interface."""
    
    @abstractmethod
    def has_next(self) -> bool:
        """Check if there are more elements."""
        pass
    
    @abstractmethod
    def next(self) -> Optional[any]:
        """Get next element."""
        pass


# Aggregate Interface
class Aggregate(ABC):
    """Aggregate interface."""
    
    @abstractmethod
    def create_iterator(self) -> Iterator:
        """Create iterator."""
        pass


# Concrete Aggregate
class BookCollection(Aggregate):
    """Book collection."""
    
    def __init__(self):
        self.books: List[str] = []
    
    def add_book(self, book: str) -> None:
        """Add book to collection."""
        self.books.append(book)
    
    def create_iterator(self) -> Iterator:
        """Create iterator for books."""
        return BookIterator(self.books)


# Concrete Iterator
class BookIterator(Iterator):
    """Iterator for book collection."""
    
    def __init__(self, books: List[str]):
        self.books = books
        self.index = 0
    
    def has_next(self) -> bool:
        return self.index < len(self.books)
    
    def next(self) -> Optional[str]:
        if self.has_next():
            book = self.books[self.index]
            self.index += 1
            return book
        return None


# Example 2: Tree Iterator
class TreeNode:
    """Tree node."""
    
    def __init__(self, value: int):
        self.value = value
        self.left: Optional['TreeNode'] = None
        self.right: Optional['TreeNode'] = None


class BinaryTree(Aggregate):
    """Binary tree aggregate."""
    
    def __init__(self, root: TreeNode):
        self.root = root
    
    def create_iterator(self) -> Iterator:
        """Create in-order iterator."""
        return InOrderIterator(self.root)


class InOrderIterator(Iterator):
    """In-order tree iterator."""
    
    def __init__(self, root: TreeNode):
        self.stack: List[TreeNode] = []
        self._push_left(root)
    
    def _push_left(self, node: Optional[TreeNode]) -> None:
        """Push all left nodes to stack."""
        while node:
            self.stack.append(node)
            node = node.left
    
    def has_next(self) -> bool:
        return len(self.stack) > 0
    
    def next(self) -> Optional[int]:
        if not self.has_next():
            return None
        
        node = self.stack.pop()
        self._push_left(node.right)
        return node.value


# Example 3: Python-style Iterator
class NumberRange:
    """Number range with Python iterator protocol."""
    
    def __init__(self, start: int, end: int, step: int = 1):
        self.start = start
        self.end = end
        self.step = step
    
    def __iter__(self):
        """Return iterator."""
        return NumberRangeIterator(self.start, self.end, self.step)


class NumberRangeIterator:
    """Iterator for number range."""
    
    def __init__(self, start: int, end: int, step: int):
        self.current = start
        self.end = end
        self.step = step
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if (self.step > 0 and self.current >= self.end) or \
           (self.step < 0 and self.current <= self.end):
            raise StopIteration
        
        value = self.current
        self.current += self.step
        return value


def main() -> None:
    """Demonstration of Iterator Pattern."""
    print("=" * 70)
    print("ITERATOR DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Book Collection
    print("Example 1: Book Collection Iterator")
    print("-" * 70)
    
    collection = BookCollection()
    collection.add_book("Design Patterns")
    collection.add_book("Clean Code")
    collection.add_book("Refactoring")
    
    iterator = collection.create_iterator()
    print("Books in collection:")
    while iterator.has_next():
        book = iterator.next()
        print(f"  - {book}")
    print()
    
    # Example 2: Tree Iterator
    print("Example 2: Binary Tree Iterator")
    print("-" * 70)
    
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
    
    print("In-order traversal:")
    values = []
    while tree_iterator.has_next():
        values.append(tree_iterator.next())
    print(f"  {values}")
    print()
    
    # Example 3: Python Iterator Protocol
    print("Example 3: Python Iterator Protocol")
    print("-" * 70)
    
    number_range = NumberRange(1, 10, 2)
    print("Numbers from 1 to 10 (step 2):")
    for num in number_range:
        print(f"  {num}", end=" ")
    print("\n")
    
    # Example 4: Using built-in iterators
    print("Example 4: Built-in Python Iterators")
    print("-" * 70)
    
    data = [1, 2, 3, 4, 5]
    iterator = iter(data)
    
    print("Iterating over list:")
    try:
        while True:
            value = next(iterator)
            print(f"  {value}", end=" ")
    except StopIteration:
        pass
    print("\n")
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Provide a way to access elements of an aggregate object")
    print("  sequentially without exposing its underlying representation.")
    print("\nKey Advantages:")
    print("  - Supports multiple traversal methods")
    print("  - Simplifies aggregate interface")
    print("  - Allows multiple iterators on same aggregate")
    print("  - Encapsulates traversal logic")
    print("\nKey Disadvantages:")
    print("  - Can be overkill for simple collections")
    print("  - Adds complexity")
    print("\nWhen to Use:")
    print("  - Need to traverse aggregate in different ways")
    print("  - Want to hide aggregate's internal structure")
    print("  - Need multiple iterators on same aggregate")
    print("  - Lazy evaluation needed")
    print("\nCommon Use Cases:")
    print("  - Collections (lists, trees, graphs)")
    print("  - Database result sets")
    print("  - File system traversal")
    print("  - Stream processing")
    print("=" * 70)


if __name__ == "__main__":
    main()
