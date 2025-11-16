#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Liskov Substitution Principle (LSP).

Objects of a superclass should be replaceable with objects of its
subclasses without breaking the application. Subtypes must be
substitutable for their base types.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# ❌ BAD: Violates LSP - Rectangle and Square are not substitutable
class BadRectangle:
    """Rectangle that violates LSP."""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def set_width(self, width: float) -> None:
        self.width = width
    
    def set_height(self, height: float) -> None:
        self.height = height
    
    def get_area(self) -> float:
        return self.width * self.height


class BadSquare(BadRectangle):
    """Square that violates LSP."""
    
    def __init__(self, side: float):
        super().__init__(side, side)
    
    def set_width(self, width: float) -> None:
        self.width = width
        self.height = width  # Breaks rectangle behavior!
    
    def set_height(self, height: float) -> None:
        self.width = height
        self.height = height  # Breaks rectangle behavior!


# ✅ GOOD: Follows LSP - both are substitutable
class Shape(ABC):
    """Abstract shape."""
    
    @abstractmethod
    def get_area(self) -> float:
        """Get area."""
        pass


class Rectangle(Shape):
    """Rectangle - follows LSP."""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def get_area(self) -> float:
        return self.width * self.height


class Square(Shape):
    """Square - follows LSP."""
    
    def __init__(self, side: float):
        self.side = side
    
    def get_area(self) -> float:
        return self.side ** 2


# Example 2: Bird Example (Classic LSP Violation)
# ❌ BAD: Violates LSP
class BadBird:
    """Bird that violates LSP."""
    
    def fly(self) -> None:
        logger.info("Flying...")


class BadPenguin(BadBird):
    """Penguin - cannot fly, violates LSP."""
    
    def fly(self) -> None:
        raise NotImplementedError("Penguins cannot fly!")  # Breaks LSP!


# ✅ GOOD: Follows LSP
class Bird(ABC):
    """Abstract bird."""
    
    @abstractmethod
    def move(self) -> None:
        """Move - all birds can move."""
        pass


class FlyingBird(Bird):
    """Bird that can fly."""
    
    def move(self) -> None:
        self.fly()
    
    def fly(self) -> None:
        logger.info("Flying...")


class NonFlyingBird(Bird):
    """Bird that cannot fly."""
    
    def move(self) -> None:
        self.swim()
    
    def swim(self) -> None:
        logger.info("Swimming...")


class Sparrow(FlyingBird):
    """Sparrow - can fly."""
    pass


class Penguin(NonFlyingBird):
    """Penguin - cannot fly, but can swim."""
    pass


# Example 3: Collection Example
class ReadOnlyCollection(ABC):
    """Read-only collection interface."""
    
    @abstractmethod
    def get(self, index: int) -> any:
        """Get item at index."""
        pass
    
    @abstractmethod
    def size(self) -> int:
        """Get size."""
        pass


class MutableCollection(ReadOnlyCollection):
    """Mutable collection - extends read-only."""
    
    @abstractmethod
    def add(self, item: any) -> None:
        """Add item."""
        pass
    
    @abstractmethod
    def remove(self, index: int) -> None:
        """Remove item."""
        pass


class ListCollection(MutableCollection):
    """List collection - follows LSP."""
    
    def __init__(self):
        self.items = []
    
    def get(self, index: int) -> any:
        return self.items[index]
    
    def size(self) -> int:
        return len(self.items)
    
    def add(self, item: any) -> None:
        self.items.append(item)
    
    def remove(self, index: int) -> None:
        self.items.pop(index)


class ImmutableList(ReadOnlyCollection):
    """Immutable list - follows LSP."""
    
    def __init__(self, items: list):
        self.items = tuple(items)
    
    def get(self, index: int) -> any:
        return self.items[index]
    
    def size(self) -> int:
        return len(self.items)


def process_collection(collection: ReadOnlyCollection) -> None:
    """Process any read-only collection - LSP allows substitution."""
    logger.info(f"Collection size: {collection.size()}")
    if collection.size() > 0:
        logger.info(f"First item: {collection.get(0)}")


def main() -> None:
    """Demonstration of Liskov Substitution Principle."""
    logger.info("=" * 70)
    logger.info("LISKOV SUBSTITUTION PRINCIPLE (LSP) DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Rectangle/Square
    logger.info("Example 1: Rectangle and Square")
    logger.info("-" * 70)
    
    logger.info("❌ BAD: Square breaks Rectangle behavior")
    rect = BadRectangle(5, 4)
    logger.info(f"Rectangle area: {rect.get_area()}")
    
    # This should work but breaks expectations
    square = BadSquare(5)
    logger.info(f"Square area: {square.get_area()}")
    square.set_width(10)  # This changes height too - unexpected!
    logger.info(f"After set_width(10): {square.get_area()}")
    logger.info()
    
    logger.info("✅ GOOD: Both are substitutable as Shapes")
    shapes = [
        Rectangle(5, 4),
        Square(5),
    ]
    
    for shape in shapes:
        logger.info(f"{shape.__class__.__name__} area: {shape.get_area()}")
    logger.info()
    
    # Example 2: Birds
    logger.info("Example 2: Bird Hierarchy")
    logger.info("-" * 70)
    
    logger.info("❌ BAD: Penguin cannot substitute Bird")
    try:
        penguin = BadPenguin()
        penguin.fly()  # This will raise exception!
    except NotImplementedError as e:
        logger.info(f"Error: {e}")
    logger.info()
    
    logger.info("✅ GOOD: All birds can move (substitutable)")
    birds = [
        Sparrow(),
        Penguin(),
    ]
    
    for bird in birds:
        logger.info(f"{bird.__class__.__name__}: ")
        bird.move()
    logger.info()
    
    # Example 3: Collections
    logger.info("Example 3: Collection Substitution")
    logger.info("-" * 70)
    
    mutable = ListCollection()
    mutable.add("Item 1")
    mutable.add("Item 2")
    
    immutable = ImmutableList(["Item A", "Item B"])
    
    # Both can be used as ReadOnlyCollection
    logger.info("Processing mutable collection:")
    process_collection(mutable)
    
    logger.info("\nProcessing immutable collection:")
    process_collection(immutable)
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPrinciple Summary:")
    logger.info("\nDefinition:")
    logger.info("  Objects of a superclass should be replaceable with")
    logger.info("  objects of its subclasses without breaking the application.")
    logger.info("  Subtypes must be substitutable for their base types.")
    logger.info("\nKey Rules:")
    logger.info("  - Preconditions cannot be strengthened in subtypes")
    logger.info("  - Postconditions cannot be weakened in subtypes")
    logger.info("  - Invariants of supertype must be preserved")
    logger.info("  - Subtypes should not throw new exceptions")
    logger.info("\nKey Benefits:")
    logger.info("  - Polymorphism works correctly")
    logger.info("  - Code reuse without breaking behavior")
    logger.info("  - Easier to maintain and extend")
    logger.info("  - Fewer bugs from unexpected behavior")
    logger.info("\nCommon Violations:")
    logger.info("  - Throwing exceptions in overridden methods")
    logger.info("  - Changing method behavior unexpectedly")
    logger.info("  - Strengthening preconditions")
    logger.info("  - Weakening postconditions")
    logger.info("\nHow to Apply:")
    logger.info("  1. Design contracts carefully")
    logger.info("  2. Use abstract base classes")
    logger.info("  3. Test substitutability")
    logger.info("  4. Avoid inheritance when composition is better")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()