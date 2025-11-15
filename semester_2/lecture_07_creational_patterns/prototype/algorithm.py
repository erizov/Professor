#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prototype Design Pattern.

Specify the kinds of objects to create using a prototypical instance,
and create new objects by copying this prototype.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
import copy

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


# Prototype Interface
class Prototype(ABC):
    """Abstract prototype interface."""
    
    @abstractmethod
    def clone(self) -> 'Prototype':
        """Clone the prototype."""
        pass


# Concrete Prototype
class Document(Prototype):
    """Document prototype."""
    
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author
        self.pages = []
    
    def add_page(self, page: str) -> None:
        """Add page to document."""
        self.pages.append(page)
    
    def clone(self) -> 'Document':
        """Create a deep copy of the document."""
        return copy.deepcopy(self)
    
    def __str__(self) -> str:
        return (f"Document(title='{self.title}', "
                f"author='{self.author}', pages={len(self.pages)})")


# Example 2: Shape Prototype
class Shape(Prototype):
    """Shape prototype."""
    
    def __init__(self, x: int, y: int, color: str):
        self.x = x
        self.y = y
        self.color = color
    
    def clone(self) -> 'Shape':
        """Clone shape."""
        return copy.deepcopy(self)
    
    def __str__(self) -> str:
        return f"Shape(x={self.x}, y={self.y}, color='{self.color}')"


class Circle(Shape):
    """Circle shape."""
    
    def __init__(self, x: int, y: int, color: str, radius: int):
        super().__init__(x, y, color)
        self.radius = radius
    
    def clone(self) -> 'Circle':
        """Clone circle."""
        return copy.deepcopy(self)
    
    def __str__(self) -> str:
        return (f"Circle(x={self.x}, y={self.y}, "
                f"color='{self.color}', radius={self.radius})")


class Rectangle(Shape):
    """Rectangle shape."""
    
    def __init__(self, x: int, y: int, color: str, 
                 width: int, height: int):
        super().__init__(x, y, color)
        self.width = width
        self.height = height
    
    def clone(self) -> 'Rectangle':
        """Clone rectangle."""
        return copy.deepcopy(self)
    
    def __str__(self) -> str:
        return (f"Rectangle(x={self.x}, y={self.y}, "
                f"color='{self.color}', {self.width}x{self.height})")


# Prototype Registry
class PrototypeRegistry:
    """Registry for managing prototypes."""
    
    def __init__(self):
        self.prototypes: dict[str, Prototype] = {}
    
    def register(self, key: str, prototype: Prototype) -> None:
        """Register a prototype."""
        self.prototypes[key] = prototype
    
    def create(self, key: str) -> Prototype:
        """Create object from prototype."""
        if key not in self.prototypes:
            raise ValueError(f"Prototype '{key}' not found")
        return self.prototypes[key].clone()


def main() -> None:
    """Demonstration of Prototype Pattern."""
    print("=" * 70)
    print("PROTOTYPE DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Document Prototype
    print("Example 1: Document Prototype")
    print("-" * 70)
    
    # Create original document
    original_doc = Document(
        title="Design Patterns",
        content="Introduction to design patterns...",
        author="John Doe"
    )
    original_doc.add_page("Page 1: Introduction")
    original_doc.add_page("Page 2: Creational Patterns")
    
    print(f"Original: {original_doc}")
    print()
    
    # Clone document
    cloned_doc = original_doc.clone()
    cloned_doc.title = "Advanced Design Patterns"
    cloned_doc.add_page("Page 3: Advanced Patterns")
    
    print(f"Original (unchanged): {original_doc}")
    print(f"Clone (modified): {cloned_doc}")
    print()
    
    # Example 2: Shape Prototype
    print("Example 2: Shape Prototype")
    print("-" * 70)
    
    # Create prototype shapes
    circle_prototype = Circle(10, 20, "red", 5)
    rectangle_prototype = Rectangle(30, 40, "blue", 10, 15)
    
    # Clone shapes
    circle1 = circle_prototype.clone()
    circle2 = circle_prototype.clone()
    circle2.x = 50
    circle2.color = "green"
    
    rect1 = rectangle_prototype.clone()
    rect2 = rectangle_prototype.clone()
    rect2.y = 60
    
    print(f"Original circle: {circle_prototype}")
    print(f"Clone 1: {circle1}")
    print(f"Clone 2 (modified): {circle2}")
    print()
    print(f"Original rectangle: {rectangle_prototype}")
    print(f"Clone 1: {rect1}")
    print(f"Clone 2 (modified): {rect2}")
    print()
    
    # Example 3: Prototype Registry
    print("Example 3: Prototype Registry")
    print("-" * 70)
    
    registry = PrototypeRegistry()
    
    # Register prototypes
    registry.register("default_circle", Circle(0, 0, "black", 1))
    registry.register("default_rect", Rectangle(0, 0, "black", 1, 1))
    
    # Create from registry
    circle3 = registry.create("default_circle")
    circle3.x = 100
    circle3.y = 200
    circle3.radius = 10
    
    rect3 = registry.create("default_rect")
    rect3.width = 20
    rect3.height = 30
    
    print(f"Created from registry: {circle3}")
    print(f"Created from registry: {rect3}")
    print()
    
    # Example 4: Performance measurement
    print("Example 4: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Prototype")
    
    def clone_document():
        doc = Document("Test", "Content", "Author")
        doc.add_page("Page 1")
        doc.add_page("Page 2")
        return doc.clone()
    
    result, metrics = timer.measure(clone_document)
    print(f"Time to clone document: {metrics['execution_time_ms']:.3f} ms")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Specify the kinds of objects to create using a prototypical")
    print("  instance, and create new objects by copying this prototype.")
    print("\nKey Advantages:")
    print("  - Reduces object creation cost")
    print("  - Hides complexity of creating new instances")
    print("  - Allows adding/removing objects at runtime")
    print("  - Alternative to inheritance for object configuration")
    print("\nKey Disadvantages:")
    print("  - Cloning complex objects can be difficult")
    print("  - Deep vs shallow copy considerations")
    print("  - Circular references can be problematic")
    print("\nWhen to Use:")
    print("  - Object creation is expensive")
    print("  - Want to avoid subclassing")
    print("  - Classes instantiated at runtime")
    print("  - Need to configure objects dynamically")
    print("\nCommon Use Cases:")
    print("  - Document editors (clone templates)")
    print("  - Game development (clone game objects)")
    print("  - Database record copying")
    print("  - Configuration objects")
    print("=" * 70)


if __name__ == "__main__":
    main()
