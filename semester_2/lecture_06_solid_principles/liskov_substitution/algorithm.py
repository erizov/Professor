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
        print("Flying...")


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
        print("Flying...")


class NonFlyingBird(Bird):
    """Bird that cannot fly."""
    
    def move(self) -> None:
        self.swim()
    
    def swim(self) -> None:
        print("Swimming...")


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
    print(f"Collection size: {collection.size()}")
    if collection.size() > 0:
        print(f"First item: {collection.get(0)}")


def main() -> None:
    """Demonstration of Liskov Substitution Principle."""
    print("=" * 70)
    print("LISKOV SUBSTITUTION PRINCIPLE (LSP) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Rectangle/Square
    print("Example 1: Rectangle and Square")
    print("-" * 70)
    
    print("❌ BAD: Square breaks Rectangle behavior")
    rect = BadRectangle(5, 4)
    print(f"Rectangle area: {rect.get_area()}")
    
    # This should work but breaks expectations
    square = BadSquare(5)
    print(f"Square area: {square.get_area()}")
    square.set_width(10)  # This changes height too - unexpected!
    print(f"After set_width(10): {square.get_area()}")
    print()
    
    print("✅ GOOD: Both are substitutable as Shapes")
    shapes = [
        Rectangle(5, 4),
        Square(5),
    ]
    
    for shape in shapes:
        print(f"{shape.__class__.__name__} area: {shape.get_area()}")
    print()
    
    # Example 2: Birds
    print("Example 2: Bird Hierarchy")
    print("-" * 70)
    
    print("❌ BAD: Penguin cannot substitute Bird")
    try:
        penguin = BadPenguin()
        penguin.fly()  # This will raise exception!
    except NotImplementedError as e:
        print(f"Error: {e}")
    print()
    
    print("✅ GOOD: All birds can move (substitutable)")
    birds = [
        Sparrow(),
        Penguin(),
    ]
    
    for bird in birds:
        print(f"{bird.__class__.__name__}: ", end="")
        bird.move()
    print()
    
    # Example 3: Collections
    print("Example 3: Collection Substitution")
    print("-" * 70)
    
    mutable = ListCollection()
    mutable.add("Item 1")
    mutable.add("Item 2")
    
    immutable = ImmutableList(["Item A", "Item B"])
    
    # Both can be used as ReadOnlyCollection
    print("Processing mutable collection:")
    process_collection(mutable)
    
    print("\nProcessing immutable collection:")
    process_collection(immutable)
    print()
    
    print("=" * 70)
    print("\nPrinciple Summary:")
    print("\nDefinition:")
    print("  Objects of a superclass should be replaceable with")
    print("  objects of its subclasses without breaking the application.")
    print("  Subtypes must be substitutable for their base types.")
    print("\nKey Rules:")
    print("  - Preconditions cannot be strengthened in subtypes")
    print("  - Postconditions cannot be weakened in subtypes")
    print("  - Invariants of supertype must be preserved")
    print("  - Subtypes should not throw new exceptions")
    print("\nKey Benefits:")
    print("  - Polymorphism works correctly")
    print("  - Code reuse without breaking behavior")
    print("  - Easier to maintain and extend")
    print("  - Fewer bugs from unexpected behavior")
    print("\nCommon Violations:")
    print("  - Throwing exceptions in overridden methods")
    print("  - Changing method behavior unexpectedly")
    print("  - Strengthening preconditions")
    print("  - Weakening postconditions")
    print("\nHow to Apply:")
    print("  1. Design contracts carefully")
    print("  2. Use abstract base classes")
    print("  3. Test substitutability")
    print("  4. Avoid inheritance when composition is better")
    print("=" * 70)


if __name__ == "__main__":
    main()
