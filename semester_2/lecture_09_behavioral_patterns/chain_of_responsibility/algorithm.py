#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chain of Responsibility Design Pattern.

Avoids coupling the sender of a request to its receiver by giving more
than one object a chance to handle the request. Chain the receiving
objects and pass the request along the chain until an object handles it.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Handler Interface
class Handler(ABC):
    """Abstract handler."""
    
    def __init__(self):
        self.next_handler: Optional['Handler'] = None
    
    def set_next(self, handler: 'Handler') -> 'Handler':
        """Set next handler in chain."""
        self.next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, request: str) -> Optional[str]:
        """Handle request."""
        pass


# Concrete Handlers
class MonkeyHandler(Handler):
    """Monkey handler."""
    
    def handle(self, request: str) -> Optional[str]:
        if request == "Banana":
            return f"Monkey: I'll eat the {request}"
        elif self.next_handler:
            return self.next_handler.handle(request)
        return None


class SquirrelHandler(Handler):
    """Squirrel handler."""
    
    def handle(self, request: str) -> Optional[str]:
        if request == "Nut":
            return f"Squirrel: I'll eat the {request}"
        elif self.next_handler:
            return self.next_handler.handle(request)
        return None


class DogHandler(Handler):
    """Dog handler."""
    
    def handle(self, request: str) -> Optional[str]:
        if request == "MeatBall":
            return f"Dog: I'll eat the {request}"
        elif self.next_handler:
            return self.next_handler.handle(request)
        return None


# Example 2: Logger Chain
class Logger(ABC):
    """Abstract logger."""
    
    def __init__(self, level: int):
        self.level = level
        self.next_logger: Optional['Logger'] = None
    
    def set_next(self, logger: 'Logger') -> 'Logger':
        """Set next logger in chain."""
        self.next_logger = logger
        return logger
    
    def log_message(self, level: int, message: str) -> None:
        """Log message if level matches."""
        if self.level <= level:
            self.write(message)
        
        if self.next_logger:
            self.next_logger.log_message(level, message)
    
    @abstractmethod
    def write(self, message: str) -> None:
        """Write log message."""
        pass


class ConsoleLogger(Logger):
    """Console logger."""
    
    def __init__(self, level: int):
        super().__init__(level)
    
    def write(self, message: str) -> None:
        print(f"Console Logger: {message}")


class FileLogger(Logger):
    """File logger."""
    
    def __init__(self, level: int):
        super().__init__(level)
    
    def write(self, message: str) -> None:
        print(f"File Logger: {message}")


class ErrorLogger(Logger):
    """Error logger."""
    
    def __init__(self, level: int):
        super().__init__(level)
    
    def write(self, message: str) -> None:
        print(f"Error Logger: {message}")


# Example 3: Purchase Approval
class PurchaseHandler(ABC):
    """Purchase approval handler."""
    
    def __init__(self):
        self.next_handler: Optional['PurchaseHandler'] = None
    
    def set_next(self, handler: 'PurchaseHandler') -> 'PurchaseHandler':
        """Set next handler."""
        self.next_handler = handler
        return handler
    
    @abstractmethod
    def can_approve(self, amount: float) -> bool:
        """Check if can approve amount."""
        pass
    
    def handle(self, amount: float) -> Optional[str]:
        """Handle purchase request."""
        if self.can_approve(amount):
            return self.approve(amount)
        elif self.next_handler:
            return self.next_handler.handle(amount)
        return "Purchase rejected - exceeds all approval limits"
    
    @abstractmethod
    def approve(self, amount: float) -> str:
        """Approve purchase."""
        pass


class ManagerHandler(PurchaseHandler):
    """Manager can approve up to $1000."""
    
    def can_approve(self, amount: float) -> bool:
        return amount <= 1000
    
    def approve(self, amount: float) -> str:
        return f"Manager approved purchase of ${amount:.2f}"


class DirectorHandler(PurchaseHandler):
    """Director can approve up to $10000."""
    
    def can_approve(self, amount: float) -> bool:
        return amount <= 10000
    
    def approve(self, amount: float) -> str:
        return f"Director approved purchase of ${amount:.2f}"


class VPHandler(PurchaseHandler):
    """VP can approve up to $100000."""
    
    def can_approve(self, amount: float) -> bool:
        return amount <= 100000
    
    def approve(self, amount: float) -> str:
        return f"VP approved purchase of ${amount:.2f}"


def main() -> None:
    """Demonstration of Chain of Responsibility Pattern."""
    print("=" * 70)
    print("CHAIN OF RESPONSIBILITY DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Animal Handler Chain
    print("Example 1: Animal Handler Chain")
    print("-" * 70)
    
    monkey = MonkeyHandler()
    squirrel = SquirrelHandler()
    dog = DogHandler()
    
    monkey.set_next(squirrel).set_next(dog)
    
    foods = ["Nut", "Banana", "Coffee", "MeatBall"]
    
    for food in foods:
        result = monkey.handle(food)
        if result:
            print(f"  {result}")
        else:
            print(f"  {food} was left untouched")
    print()
    
    # Example 2: Logger Chain
    print("Example 2: Logger Chain")
    print("-" * 70)
    
    # Levels: 1=INFO, 2=DEBUG, 3=ERROR
    console_logger = ConsoleLogger(1)
    file_logger = FileLogger(2)
    error_logger = ErrorLogger(3)
    
    console_logger.set_next(file_logger).set_next(error_logger)
    
    console_logger.log_message(1, "This is an information.")
    console_logger.log_message(2, "This is a debug level information.")
    console_logger.log_message(3, "This is an error information.")
    print()
    
    # Example 3: Purchase Approval
    print("Example 3: Purchase Approval Chain")
    print("-" * 70)
    
    manager = ManagerHandler()
    director = DirectorHandler()
    vp = VPHandler()
    
    manager.set_next(director).set_next(vp)
    
    amounts = [500.0, 5000.0, 50000.0, 200000.0]
    
    for amount in amounts:
        result = manager.handle(amount)
        print(f"  Purchase ${amount:.2f}: {result}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Avoid coupling the sender of a request to its receiver")
    print("  by giving more than one object a chance to handle the")
    print("  request. Chain the receiving objects and pass the request")
    print("  along the chain until an object handles it.")
    print("\nKey Advantages:")
    print("  - Decouples sender and receiver")
    print("  - Dynamic chain composition")
    print("  - Flexible request handling")
    print("  - Can add/remove handlers easily")
    print("\nKey Disadvantages:")
    print("  - No guarantee request will be handled")
    print("  - Performance overhead (chain traversal)")
    print("  - Can be hard to debug")
    print("\nWhen to Use:")
    print("  - Multiple objects can handle request")
    print("  - Don't know which handler will process")
    print("  - Want to decouple sender and receivers")
    print("  - Need dynamic chain composition")
    print("\nCommon Use Cases:")
    print("  - Event handling systems")
    print("  - Exception handling")
    print("  - Request processing pipelines")
    print("  - Approval workflows")
    print("  - Middleware in web frameworks")
    print("=" * 70)


if __name__ == "__main__":
    main()
