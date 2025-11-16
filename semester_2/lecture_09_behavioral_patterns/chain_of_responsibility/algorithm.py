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
from framework.logging_utils import get_logger
logger = get_logger(__name__)

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
        logger.info(f"Console Logger: {message}")


class FileLogger(Logger):
    """File logger."""
    
    def __init__(self, level: int):
        super().__init__(level)
    
    def write(self, message: str) -> None:
        logger.info(f"File Logger: {message}")


class ErrorLogger(Logger):
    """Error logger."""
    
    def __init__(self, level: int):
        super().__init__(level)
    
    def write(self, message: str) -> None:
        logger.info(f"Error Logger: {message}")


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
    logger.info("=" * 70)
    logger.info("CHAIN OF RESPONSIBILITY DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Animal Handler Chain
    logger.info("Example 1: Animal Handler Chain")
    logger.info("-" * 70)
    
    monkey = MonkeyHandler()
    squirrel = SquirrelHandler()
    dog = DogHandler()
    
    monkey.set_next(squirrel).set_next(dog)
    
    foods = ["Nut", "Banana", "Coffee", "MeatBall"]
    
    for food in foods:
        result = monkey.handle(food)
        if result:
            logger.info(f"  {result}")
        else:
            logger.info(f"  {food} was left untouched")
    logger.info()
    
    # Example 2: Logger Chain
    logger.info("Example 2: Logger Chain")
    logger.info("-" * 70)
    
    # Levels: 1=INFO, 2=DEBUG, 3=ERROR
    console_logger = ConsoleLogger(1)
    file_logger = FileLogger(2)
    error_logger = ErrorLogger(3)
    
    console_logger.set_next(file_logger).set_next(error_logger)
    
    console_logger.log_message(1, "This is an information.")
    console_logger.log_message(2, "This is a debug level information.")
    console_logger.log_message(3, "This is an error information.")
    logger.info()
    
    # Example 3: Purchase Approval
    logger.info("Example 3: Purchase Approval Chain")
    logger.info("-" * 70)
    
    manager = ManagerHandler()
    director = DirectorHandler()
    vp = VPHandler()
    
    manager.set_next(director).set_next(vp)
    
    amounts = [500.0, 5000.0, 50000.0, 200000.0]
    
    for amount in amounts:
        result = manager.handle(amount)
        logger.info(f"  Purchase ${amount:.2f}: {result}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Avoid coupling the sender of a request to its receiver")
    logger.info("  by giving more than one object a chance to handle the")
    logger.info("  request. Chain the receiving objects and pass the request")
    logger.info("  along the chain until an object handles it.")
    logger.info("\nKey Advantages:")
    logger.info("  - Decouples sender and receiver")
    logger.info("  - Dynamic chain composition")
    logger.info("  - Flexible request handling")
    logger.info("  - Can add/remove handlers easily")
    logger.info("\nKey Disadvantages:")
    logger.info("  - No guarantee request will be handled")
    logger.info("  - Performance overhead (chain traversal)")
    logger.info("  - Can be hard to debug")
    logger.info("\nWhen to Use:")
    logger.info("  - Multiple objects can handle request")
    logger.info("  - Don't know which handler will process")
    logger.info("  - Want to decouple sender and receivers")
    logger.info("  - Need dynamic chain composition")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Event handling systems")
    logger.info("  - Exception handling")
    logger.info("  - Request processing pipelines")
    logger.info("  - Approval workflows")
    logger.info("  - Middleware in web frameworks")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()