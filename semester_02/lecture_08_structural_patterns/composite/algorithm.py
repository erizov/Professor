#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Composite implementation.

This file contains the implementation of the Composite algorithm.
"""

from typing import List, Optional, Dict, Set


class Component:
    """Component interface."""

    def operation(self) -> str:
        pass


class Leaf(Component):
    """Leaf component."""

    def __init__(self, name: str):
        self.name = name

    def operation(self) -> str:
        return f"Leaf({self.name})"


class Composite(Component):
    """Composite component."""

    def __init__(self, name: str):
        self.name = name
        self.children: List[Component] = []

    def add(self, component: Component) -> None:
        """Add child component."""
        self.children.append(component)

    def remove(self, component: Component) -> None:
        """Remove child component."""
        self.children.remove(component)

    def operation(self) -> str:
        results = [f"Composite({self.name})"]
        for child in self.children:
            results.append(child.operation())
        return " -> ".join(results)


def main() -> None:
    """Demonstrate Composite."""
    print("=" * 70)
    print("COMPOSITE")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Composite")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
