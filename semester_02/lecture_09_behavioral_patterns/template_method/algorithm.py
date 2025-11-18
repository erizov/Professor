#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Template Method implementation.

This file contains the implementation of the Template Method algorithm.
"""

from typing import List, Optional, Dict, Set


class AbstractClass:
    """Abstract class with template method."""
    def template_method(self) -> str:
        """Template method."""
        result = []
        result.append(self.operation1())
        result.append(self.operation2())
        result.append(self.operation3())
        return " -> ".join(result)
    
    def operation1(self) -> str:
        """Primitive operation 1."""
        return "AbstractClass.operation1"
    
    def operation2(self) -> str:
        """Primitive operation 2 (hook)."""
        return "AbstractClass.operation2"
    
    def operation3(self) -> str:
        """Primitive operation 3."""
        return "AbstractClass.operation3"

class ConcreteClass(AbstractClass):
    """Concrete class."""
    def operation2(self) -> str:
        """Override operation 2."""
        return "ConcreteClass.operation2"


def main() -> None:
    """Demonstrate Template Method."""
    print("=" * 70)
    print("TEMPLATE METHOD")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Template Method")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
