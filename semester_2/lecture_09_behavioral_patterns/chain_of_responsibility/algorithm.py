#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chain Of Responsibility implementation.

This file contains the implementation of the Chain Of Responsibility algorithm.
"""

from typing import List, Optional, Dict, Set


class Handler:
    """Handler interface."""
    def __init__(self):
        self.next_handler: Optional['Handler'] = None
    
    def set_next(self, handler: 'Handler') -> 'Handler':
        """Set next handler."""
        self.next_handler = handler
        return handler
    
    def handle(self, request: str) -> Optional[str]:
        """Handle request."""
        if self.next_handler:
            return self.next_handler.handle(request)
        return None

class ConcreteHandlerA(Handler):
    """Concrete handler A."""
    def handle(self, request: str) -> Optional[str]:
        if request == "A":
            return f"ConcreteHandlerA handled {request}"
        return super().handle(request)

class ConcreteHandlerB(Handler):
    """Concrete handler B."""
    def handle(self, request: str) -> Optional[str]:
        if request == "B":
            return f"ConcreteHandlerB handled {request}"
        return super().handle(request)


def main() -> None:
    """Demonstrate Chain Of Responsibility."""
    print("=" * 70)
    print("CHAIN OF RESPONSIBILITY")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Chain Of Responsibility")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
