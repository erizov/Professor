#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open Closed implementation.

This file contains the implementation of the Open Closed algorithm.
"""

from typing import List, Optional, Dict, Set


class OpenClosed:
    """Open-Closed principle."""
    def __init__(self):
        self.base_classes: Dict[str, List[str]] = {}
        self.extensions: Dict[str, str] = {}
    
    def define_base(self, base_name: str, methods: List[str]) -> None:
        """Define base class."""
        self.base_classes[base_name] = methods
    
    def extend(self, extension_name: str, base_name: str, 
              new_methods: List[str]) -> None:
        """Extend base class."""
        self.extensions[extension_name] = {
            'base': base_name,
            'methods': new_methods
        }
    
    def get_methods(self, class_name: str) -> List[str]:
        """Get all methods for class."""
        if class_name in self.extensions:
            ext = self.extensions[class_name]
            base_methods = self.base_classes.get(ext['base'], [])
            return base_methods + ext['methods']
        return self.base_classes.get(class_name, [])


def main() -> None:
    """Demonstrate Open Closed."""
    print("=" * 70)
    print("OPEN CLOSED")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Open Closed")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
