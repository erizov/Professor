#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Composite Design Pattern.

Composes objects into tree structures to represent part-whole hierarchies.
Lets clients treat individual objects and compositions uniformly.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Component Interface
class FileSystemComponent(ABC):
    """Abstract component for file system."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def get_size(self) -> int:
        """Get size in bytes."""
        pass
    
    @abstractmethod
    def display(self, indent: str = "") -> None:
        """Display component."""
        pass


# Leaf
class File(FileSystemComponent):
    """File leaf component."""
    
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self.size = size
    
    def get_size(self) -> int:
        return self.size
    
    def display(self, indent: str = "") -> None:
        print(f"{indent}📄 {self.name} ({self.size} bytes)")


# Composite
class Directory(FileSystemComponent):
    """Directory composite component."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.children: List[FileSystemComponent] = []
    
    def add(self, component: FileSystemComponent) -> None:
        """Add child component."""
        self.children.append(component)
    
    def remove(self, component: FileSystemComponent) -> None:
        """Remove child component."""
        if component in self.children:
            self.children.remove(component)
    
    def get_size(self) -> int:
        """Get total size of directory."""
        return sum(child.get_size() for child in self.children)
    
    def display(self, indent: str = "") -> None:
        print(f"{indent}📁 {self.name}/ ({self.get_size()} bytes)")
        for child in self.children:
            child.display(indent + "  ")


# Example 2: Organization Structure
class Employee(ABC):
    """Employee component."""
    
    def __init__(self, name: str, position: str):
        self.name = name
        self.position = position
    
    @abstractmethod
    def get_salary(self) -> float:
        pass
    
    @abstractmethod
    def show_details(self, indent: str = "") -> None:
        pass


class IndividualEmployee(Employee):
    """Individual employee (leaf)."""
    
    def __init__(self, name: str, position: str, salary: float):
        super().__init__(name, position)
        self.salary = salary
    
    def get_salary(self) -> float:
        return self.salary
    
    def show_details(self, indent: str = "") -> None:
        print(f"{indent}{self.name} - {self.position} (${self.salary:,.2f})")


class Department(Employee):
    """Department (composite)."""
    
    def __init__(self, name: str):
        super().__init__(name, "Department")
        self.members: List[Employee] = []
    
    def add(self, employee: Employee) -> None:
        """Add employee to department."""
        self.members.append(employee)
    
    def get_salary(self) -> float:
        """Get total department salary."""
        return sum(member.get_salary() for member in self.members)
    
    def show_details(self, indent: str = "") -> None:
        print(f"{indent}📊 {self.name} (Total: ${self.get_salary():,.2f})")
        for member in self.members:
            member.show_details(indent + "  ")


# Example 3: Menu System
class MenuComponent(ABC):
    """Menu component."""
    
    @abstractmethod
    def display(self, indent: str = "") -> None:
        pass


class MenuItem(MenuComponent):
    """Menu item (leaf)."""
    
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
    
    def display(self, indent: str = "") -> None:
        print(f"{indent}• {self.name} - ${self.price:.2f}")


class Menu(MenuComponent):
    """Menu (composite)."""
    
    def __init__(self, name: str):
        self.name = name
        self.items: List[MenuComponent] = []
    
    def add(self, component: MenuComponent) -> None:
        """Add menu component."""
        self.items.append(component)
    
    def display(self, indent: str = "") -> None:
        print(f"{indent}📋 {self.name}")
        for item in self.items:
            item.display(indent + "  ")


def main() -> None:
    """Demonstration of Composite Pattern."""
    print("=" * 70)
    print("COMPOSITE DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: File System
    print("Example 1: File System Structure")
    print("-" * 70)
    
    root = Directory("root")
    
    home = Directory("home")
    home.add(File("document.txt", 1024))
    home.add(File("image.jpg", 2048))
    
    documents = Directory("documents")
    documents.add(File("report.pdf", 4096))
    documents.add(File("presentation.pptx", 8192))
    
    home.add(documents)
    root.add(home)
    
    root.add(File("readme.txt", 512))
    
    root.display()
    print()
    
    # Example 2: Organization Structure
    print("Example 2: Organization Structure")
    print("-" * 70)
    
    engineering = Department("Engineering")
    engineering.add(IndividualEmployee("Alice", "Developer", 80000))
    engineering.add(IndividualEmployee("Bob", "Developer", 85000))
    
    qa = Department("QA")
    qa.add(IndividualEmployee("Charlie", "Tester", 70000))
    
    engineering.add(qa)
    
    sales = Department("Sales")
    sales.add(IndividualEmployee("Diana", "Sales Rep", 60000))
    
    company = Department("Company")
    company.add(engineering)
    company.add(sales)
    
    company.show_details()
    print()
    
    # Example 3: Menu System
    print("Example 3: Restaurant Menu")
    print("-" * 70)
    
    breakfast = Menu("Breakfast")
    breakfast.add(MenuItem("Pancakes", 8.99))
    breakfast.add(MenuItem("Waffles", 9.99))
    
    lunch = Menu("Lunch")
    lunch.add(MenuItem("Burger", 12.99))
    lunch.add(MenuItem("Salad", 10.99))
    
    dinner = Menu("Dinner")
    dinner.add(MenuItem("Steak", 24.99))
    dinner.add(MenuItem("Pasta", 16.99))
    
    main_menu = Menu("Main Menu")
    main_menu.add(breakfast)
    main_menu.add(lunch)
    main_menu.add(dinner)
    
    main_menu.display()
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Compose objects into tree structures to represent")
    print("  part-whole hierarchies. Lets clients treat individual")
    print("  objects and compositions uniformly.")
    print("\nKey Advantages:")
    print("  - Uniform treatment of individual and composite objects")
    print("  - Easy to add new component types")
    print("  - Simplifies client code")
    print("  - Makes complex tree structures easier to work with")
    print("\nKey Disadvantages:")
    print("  - Can make design overly general")
    print("  - Hard to restrict component types")
    print("  - Can be difficult to implement")
    print("\nWhen to Use:")
    print("  - Represent part-whole hierarchies")
    print("  - Want clients to ignore composition/individual differences")
    print("  - Tree structures")
    print("  - Recursive structures")
    print("\nCommon Use Cases:")
    print("  - File systems")
    print("  - GUI components (containers)")
    print("  - Organization structures")
    print("  - Menu systems")
    print("  - Expression trees")
    print("=" * 70)


if __name__ == "__main__":
    main()
