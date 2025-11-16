#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proxy Design Pattern.

Provides a surrogate or placeholder for another object to control
access to it.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
import time
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Subject Interface
class Image(ABC):
    """Image interface."""
    
    @abstractmethod
    def display(self) -> None:
        """Display image."""
        pass


# Real Subject
class RealImage(Image):
    """Real image - expensive to load."""
    
    def __init__(self, filename: str):
        self.filename = filename
        self._load_from_disk()
    
    def _load_from_disk(self) -> None:
        """Simulate loading from disk."""
        logger.info(f"Loading {self.filename} from disk...")
        time.sleep(0.1)  # Simulate slow loading
    
    def display(self) -> None:
        """Display image."""
        logger.info(f"Displaying {self.filename}")


# Proxy
class ProxyImage(Image):
    """Proxy for image - lazy loading."""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.real_image: RealImage = None
    
    def display(self) -> None:
        """Display image - loads on demand."""
        if self.real_image is None:
            self.real_image = RealImage(self.filename)
        self.real_image.display()


# Example 2: Protection Proxy
class BankAccount:
    """Bank account."""
    
    def __init__(self, balance: float):
        self.balance = balance
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw money."""
        if amount <= self.balance:
            self.balance -= amount
            logger.info(f"Withdrew ${amount}. New balance: ${self.balance:.2f}")
            return True
        else:
            logger.info("Insufficient funds")
            return False
    
    def get_balance(self) -> float:
        """Get balance."""
        return self.balance


class AccountProxy:
    """Protection proxy for bank account."""
    
    def __init__(self, account: BankAccount, user_role: str):
        self.account = account
        self.user_role = user_role
    
    def withdraw(self, amount: float) -> bool:
        """Withdraw with permission check."""
        if self.user_role == "admin":
            return self.account.withdraw(amount)
        else:
            logger.info("Access denied: Only admins can withdraw")
            return False
    
    def get_balance(self) -> float:
        """Get balance - allowed for all."""
        return self.account.get_balance()


# Example 3: Virtual Proxy (Lazy Initialization)
class ExpensiveObject:
    """Expensive object to create."""
    
    def __init__(self):
        logger.info("Creating expensive object...")
        time.sleep(0.1)  # Simulate expensive creation
        self.data = "Expensive data loaded"
    
    def process(self) -> str:
        """Process data."""
        return f"Processing: {self.data}"


class ExpensiveObjectProxy:
    """Proxy for expensive object."""
    
    def __init__(self):
        self._object: ExpensiveObject = None
    
    def process(self) -> str:
        """Process - creates object on demand."""
        if self._object is None:
            self._object = ExpensiveObject()
        return self._object.process()


# Example 4: Remote Proxy (simulated)
class RemoteService:
    """Remote service (simulated)."""
    
    def expensive_operation(self) -> str:
        """Expensive remote operation."""
        logger.info("Calling remote service...")
        time.sleep(0.2)  # Simulate network delay
        return "Result from remote service"


class RemoteServiceProxy:
    """Proxy for remote service with caching."""
    
    def __init__(self):
        self.service = RemoteService()
        self.cache: str = None
    
    def expensive_operation(self) -> str:
        """Expensive operation with caching."""
        if self.cache is None:
            self.cache = self.service.expensive_operation()
        else:
            logger.info("Returning cached result")
        return self.cache


def main() -> None:
    """Demonstration of Proxy Pattern."""
    logger.info("=" * 70)
    logger.info("PROXY DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Virtual Proxy (Lazy Loading)
    logger.info("Example 1: Virtual Proxy - Lazy Loading")
    logger.info("-" * 70)
    
    logger.info("Creating proxy (no loading yet)...")
    image1 = ProxyImage("photo1.jpg")
    image2 = ProxyImage("photo2.jpg")
    
    logger.info("\nDisplaying image 1 (loads now):")
    image1.display()
    
    logger.info("\nDisplaying image 1 again (already loaded):")
    image1.display()
    
    logger.info("\nDisplaying image 2 (loads now):")
    image2.display()
    logger.info()
    
    # Example 2: Protection Proxy
    logger.info("Example 2: Protection Proxy")
    logger.info("-" * 70)
    
    account = BankAccount(1000.0)
    
    admin_proxy = AccountProxy(account, "admin")
    user_proxy = AccountProxy(account, "user")
    
    logger.info("Admin trying to withdraw:")
    admin_proxy.withdraw(100.0)
    
    logger.info("\nUser trying to withdraw:")
    user_proxy.withdraw(50.0)
    
    logger.info(f"\nBalance (accessible to all): ${account.get_balance():.2f}")
    logger.info()
    
    # Example 3: Virtual Proxy
    logger.info("Example 3: Virtual Proxy - Lazy Initialization")
    logger.info("-" * 70)
    
    logger.info("Creating proxy (no object created yet)...")
    proxy = ExpensiveObjectProxy()
    
    logger.info("Calling process (creates object now):")
    result = proxy.process()
    logger.info(result)
    
    logger.info("\nCalling process again (object already created):")
    result = proxy.process()
    logger.info(result)
    logger.info()
    
    # Example 4: Remote Proxy with Caching
    logger.info("Example 4: Remote Proxy with Caching")
    logger.info("-" * 70)
    
    remote_proxy = RemoteServiceProxy()
    
    logger.info("First call (calls remote service):")
    result1 = remote_proxy.expensive_operation()
    logger.info(f"Result: {result1}")
    
    logger.info("\nSecond call (uses cache):")
    result2 = remote_proxy.expensive_operation()
    logger.info(f"Result: {result2}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Provide a surrogate or placeholder for another object")
    logger.info("  to control access to it.")
    logger.info("\nTypes of Proxies:")
    logger.info("  1. Virtual Proxy: Lazy initialization")
    logger.info("  2. Protection Proxy: Access control")
    logger.info("  3. Remote Proxy: Local representative for remote object")
    logger.info("  4. Smart Proxy: Additional functionality (caching, logging)")
    logger.info("\nKey Advantages:")
    logger.info("  - Control access to real subject")
    logger.info("  - Lazy initialization")
    logger.info("  - Additional functionality (caching, logging)")
    logger.info("  - Security and access control")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Additional layer of indirection")
    logger.info("  - Can complicate code")
    logger.info("  - Performance overhead")
    logger.info("\nWhen to Use:")
    logger.info("  - Lazy initialization")
    logger.info("  - Access control")
    logger.info("  - Remote object access")
    logger.info("  - Caching")
    logger.info("  - Logging and monitoring")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Lazy loading (images, data)")
    logger.info("  - Access control")
    logger.info("  - Caching")
    logger.info("  - Remote method invocation")
    logger.info("  - Logging and monitoring")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()