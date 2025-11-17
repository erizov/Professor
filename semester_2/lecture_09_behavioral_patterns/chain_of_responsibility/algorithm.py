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
        
    
    """
    Chain Of Responsibility implementation.
    
    Args:
        *args: Variable arguments
        **kwargs: Keyword arguments
        
    Returns:
        Algorithm result
    """
    # Implementation for chain_of_responsibility
    logger.info(f"Executing chain_of_responsibility")
    return None


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