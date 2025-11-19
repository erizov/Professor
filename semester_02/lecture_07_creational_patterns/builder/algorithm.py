#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builder implementation.

This file contains the implementation of the Builder algorithm.
"""

from typing import List, Optional, Dict, Set


class Product:
    """Product class."""

    def __init__(self):
        self.parts: List[str] = []

    def add_part(self, part: str) -> None:
        """Add part to product."""
        self.parts.append(part)

    def show(self) -> str:
        """Show product parts."""
        return ", ".join(self.parts)


class Builder:
    """Builder interface."""

    def build_part_a(self) -> None:
        pass

    def build_part_b(self) -> None:
        pass

    def get_result(self) -> Product:
        pass


class ConcreteBuilder(Builder):
    """Concrete builder."""

    def __init__(self):
        self.product = Product()

    def build_part_a(self) -> None:
        self.product.add_part("PartA")

    def build_part_b(self) -> None:
        self.product.add_part("PartB")

    def get_result(self) -> Product:
        return self.product


class Director:
    """Director that uses builder."""

    def __init__(self, builder: Builder):
        self.builder = builder

    def construct(self) -> Product:
        """Construct product."""
        self.builder.build_part_a()
        self.builder.build_part_b()
        return self.builder.get_result()


def main() -> None:
    """Demonstrate Builder."""
    print("=" * 70)
    print("BUILDER")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Builder")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
