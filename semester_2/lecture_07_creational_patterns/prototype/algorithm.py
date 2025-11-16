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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("=" * 70)
    logger.info("PROTOTYPE DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Document Prototype
    logger.info("Example 1: Document Prototype")
    logger.info("-" * 70)
    
    # Create original document
    original_doc = Document(
        title="Design Patterns",
        content="Introduction to design patterns...",
        author="John Doe"
    )
    original_doc.add_page("Page 1: Introduction")
    original_doc.add_page("Page 2: Creational Patterns")
    
    logger.info(f"Original: {original_doc}")
    logger.info()
    
    # Clone document
    cloned_doc = original_doc.clone()
    cloned_doc.title = "Advanced Design Patterns"
    cloned_doc.add_page("Page 3: Advanced Patterns")
    
    logger.info(f"Original (unchanged): {original_doc}")
    logger.info(f"Clone (modified): {cloned_doc}")
    logger.info()
    
    # Example 2: Shape Prototype
    logger.info("Example 2: Shape Prototype")
    logger.info("-" * 70)
    
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
    
    logger.info(f"Original circle: {circle_prototype}")
    logger.info(f"Clone 1: {circle1}")
    logger.info(f"Clone 2 (modified): {circle2}")
    logger.info()
    logger.info(f"Original rectangle: {rectangle_prototype}")
    logger.info(f"Clone 1: {rect1}")
    logger.info(f"Clone 2 (modified): {rect2}")
    logger.info()
    
    # Example 3: Prototype Registry
    logger.info("Example 3: Prototype Registry")
    logger.info("-" * 70)
    
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
    
    logger.info(f"Created from registry: {circle3}")
    logger.info(f"Created from registry: {rect3}")
    logger.info()
    
    # Example 4: Performance measurement
    logger.info("Example 4: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Prototype")
    
    def clone_document():
        doc = Document("Test", "Content", "Author")
        doc.add_page("Page 1")
        doc.add_page("Page 2")
        return doc.clone()
    
    result, metrics = timer.measure(clone_document)
    logger.info(f"Time to clone document: {metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Specify the kinds of objects to create using a prototypical")
    logger.info("  instance, and create new objects by copying this prototype.")
    logger.info("\nKey Advantages:")
    logger.info("  - Reduces object creation cost")
    logger.info("  - Hides complexity of creating new instances")
    logger.info("  - Allows adding/removing objects at runtime")
    logger.info("  - Alternative to inheritance for object configuration")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Cloning complex objects can be difficult")
    logger.info("  - Deep vs shallow copy considerations")
    logger.info("  - Circular references can be problematic")
    logger.info("\nWhen to Use:")
    logger.info("  - Object creation is expensive")
    logger.info("  - Want to avoid subclassing")
    logger.info("  - Classes instantiated at runtime")
    logger.info("  - Need to configure objects dynamically")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Document editors (clone templates)")
    logger.info("  - Game development (clone game objects)")
    logger.info("  - Database record copying")
    logger.info("  - Configuration objects")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()