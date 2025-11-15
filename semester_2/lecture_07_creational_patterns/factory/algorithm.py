#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Factory Design Pattern.

Defines an interface for creating objects, but lets subclasses decide
which class to instantiate.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, Type

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Product Interface
class Shape(ABC):
    """Abstract base class for shapes."""
    
    @abstractmethod
    def draw(self) -> str:
        """Draw the shape."""
        pass
    
    @abstractmethod
    def area(self) -> float:
        """Calculate area."""
        pass


# Concrete Products
class Circle(Shape):
    """Circle implementation."""
    
    def __init__(self, radius: float):
        self.radius = radius
    
    def draw(self) -> str:
        return f"Drawing Circle with radius {self.radius}"
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2


class Rectangle(Shape):
    """Rectangle implementation."""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def draw(self) -> str:
        return f"Drawing Rectangle {self.width}x{self.height}"
    
    def area(self) -> float:
        return self.width * self.height


class Triangle(Shape):
    """Triangle implementation."""
    
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height
    
    def draw(self) -> str:
        return f"Drawing Triangle with base {self.base}, height {self.height}"
    
    def area(self) -> float:
        return 0.5 * self.base * self.height


# Simple Factory (not true Factory Pattern)
class ShapeFactory:
    """Simple factory for creating shapes."""
    
    @staticmethod
    def create_shape(shape_type: str, *args) -> Shape:
        """Create shape based on type."""
        shape_types = {
            'circle': Circle,
            'rectangle': Rectangle,
            'triangle': Triangle
        }
        
        shape_class = shape_types.get(shape_type.lower())
        if shape_class is None:
            raise ValueError(f"Unknown shape type: {shape_type}")
        
        return shape_class(*args)


# Factory Method Pattern
class Document(ABC):
    """Abstract Document."""
    
    @abstractmethod
    def create_page(self) -> 'Page':
        """Factory method to create pages."""
        pass
    
    def print_document(self) -> None:
        """Print document with multiple pages."""
        print(f"Creating {self.__class__.__name__}")
        for i in range(3):
            page = self.create_page()
            print(f"  Page {i+1}: {page.render()}")


class Page(ABC):
    """Abstract Page."""
    
    @abstractmethod
    def render(self) -> str:
        """Render page content."""
        pass


class PDFDocument(Document):
    """PDF Document."""
    
    def create_page(self) -> 'Page':
        return PDFPage()


class PDFPage(Page):
    """PDF Page."""
    
    def render(self) -> str:
        return "Rendering PDF page with vector graphics"


class WordDocument(Document):
    """Word Document."""
    
    def create_page(self) -> 'Page':
        return WordPage()


class WordPage(Page):
    """Word Page."""
    
    def render(self) -> str:
        return "Rendering Word page with formatted text"


# Registry-based Factory
class VehicleFactory:
    """Registry-based factory for vehicles."""
    
    _registry: Dict[str, Type] = {}
    
    @classmethod
    def register(cls, vehicle_type: str, vehicle_class: Type) -> None:
        """Register a vehicle type."""
        cls._registry[vehicle_type.lower()] = vehicle_class
    
    @classmethod
    def create(cls, vehicle_type: str, *args, **kwargs):
        """Create vehicle from registry."""
        vehicle_class = cls._registry.get(vehicle_type.lower())
        if vehicle_class is None:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        return vehicle_class(*args, **kwargs)


class Vehicle(ABC):
    """Abstract Vehicle."""
    
    @abstractmethod
    def start(self) -> str:
        pass


class Car(Vehicle):
    def __init__(self, brand: str):
        self.brand = brand
    
    def start(self) -> str:
        return f"{self.brand} car engine starting: Vroom!"


class Motorcycle(Vehicle):
    def __init__(self, brand: str):
        self.brand = brand
    
    def start(self) -> str:
        return f"{self.brand} motorcycle engine starting: Brrr!"


class Truck(Vehicle):
    def __init__(self, brand: str):
        self.brand = brand
    
    def start(self) -> str:
        return f"{self.brand} truck engine starting: ROAR!"


# Register vehicles
VehicleFactory.register('car', Car)
VehicleFactory.register('motorcycle', Motorcycle)
VehicleFactory.register('truck', Truck)


def main() -> None:
    """Demonstration of Factory Pattern."""
    print("=" * 70)
    print("FACTORY DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Simple Factory
    print("Example 1: Simple Factory Pattern")
    print("-" * 70)
    
    circle = ShapeFactory.create_shape('circle', 5.0)
    print(circle.draw())
    print(f"Area: {circle.area():.2f}")
    
    rectangle = ShapeFactory.create_shape('rectangle', 4.0, 6.0)
    print(rectangle.draw())
    print(f"Area: {rectangle.area():.2f}")
    
    triangle = ShapeFactory.create_shape('triangle', 3.0, 4.0)
    print(triangle.draw())
    print(f"Area: {triangle.area():.2f}")
    print()
    
    # Example 2: Factory Method Pattern
    print("Example 2: Factory Method Pattern")
    print("-" * 70)
    
    pdf_doc = PDFDocument()
    pdf_doc.print_document()
    
    print()
    
    word_doc = WordDocument()
    word_doc.print_document()
    print()
    
    # Example 3: Registry-based Factory
    print("Example 3: Registry-based Factory")
    print("-" * 70)
    
    car = VehicleFactory.create('car', 'Toyota')
    print(car.start())
    
    motorcycle = VehicleFactory.create('motorcycle', 'Harley-Davidson')
    print(motorcycle.start())
    
    truck = VehicleFactory.create('truck', 'Volvo')
    print(truck.start())
    print()
    
    # Example 4: Multiple shapes
    print("Example 4: Creating Multiple Objects")
    print("-" * 70)
    
    shape_specs = [
        ('circle', [3.0]),
        ('rectangle', [5.0, 2.0]),
        ('triangle', [4.0, 3.0]),
        ('circle', [7.0]),
    ]
    
    total_area = 0
    for shape_type, args in shape_specs:
        shape = ShapeFactory.create_shape(shape_type, *args)
        print(shape.draw())
        area = shape.area()
        print(f"  Area: {area:.2f}")
        total_area += area
    
    print(f"\nTotal area of all shapes: {total_area:.2f}")
    print()
    
    # Example 5: Error handling
    print("Example 5: Error Handling")
    print("-" * 70)
    
    try:
        invalid_shape = ShapeFactory.create_shape('hexagon', 5.0)
    except ValueError as e:
        print(f"Error: {e}")
    
    try:
        invalid_vehicle = VehicleFactory.create('airplane', 'Boeing')
    except ValueError as e:
        print(f"Error: {e}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Define an interface for creating objects, but let")
    print("  subclasses decide which class to instantiate.")
    print("\nKey Advantages:")
    print("  - Loose coupling between client and concrete classes")
    print("  - Single Responsibility Principle")
    print("  - Open/Closed Principle (easy to add new types)")
    print("  - Centralizes object creation logic")
    print("\nKey Disadvantages:")
    print("  - Can add complexity")
    print("  - May require many subclasses")
    print("\nWhen to Use:")
    print("  - Class can't anticipate objects it must create")
    print("  - Class wants subclasses to specify objects")
    print("  - Need to delegate creation to helper subclasses")
    print("  - Want to provide library/framework hook")
    print("\nWhen Not to Use:")
    print("  - Only one type of object")
    print("  - Object creation is simple")
    print("  - Adds unnecessary complexity")
    print("\nVariations:")
    print("  - Simple Factory: Not true pattern, but useful")
    print("  - Factory Method: Subclasses decide which class")
    print("  - Abstract Factory: Families of related objects")
    print("  - Registry Factory: Dynamic registration")
    print("\nReal-world Examples:")
    print("  - GUI frameworks (creating widgets)")
    print("  - Database drivers (creating connections)")
    print("  - Document processors (PDF, Word, etc.)")
    print("  - Game engines (creating game objects)")
    print("=" * 70)


if __name__ == "__main__":
    main()
