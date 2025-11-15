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
        print(f"Loading {self.filename} from disk...")
        time.sleep(0.1)  # Simulate slow loading
    
    def display(self) -> None:
        """Display image."""
        print(f"Displaying {self.filename}")


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
            print(f"Withdrew ${amount}. New balance: ${self.balance:.2f}")
            return True
        else:
            print("Insufficient funds")
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
            print("Access denied: Only admins can withdraw")
            return False
    
    def get_balance(self) -> float:
        """Get balance - allowed for all."""
        return self.account.get_balance()


# Example 3: Virtual Proxy (Lazy Initialization)
class ExpensiveObject:
    """Expensive object to create."""
    
    def __init__(self):
        print("Creating expensive object...")
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
        print("Calling remote service...")
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
            print("Returning cached result")
        return self.cache


def main() -> None:
    """Demonstration of Proxy Pattern."""
    print("=" * 70)
    print("PROXY DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Virtual Proxy (Lazy Loading)
    print("Example 1: Virtual Proxy - Lazy Loading")
    print("-" * 70)
    
    print("Creating proxy (no loading yet)...")
    image1 = ProxyImage("photo1.jpg")
    image2 = ProxyImage("photo2.jpg")
    
    print("\nDisplaying image 1 (loads now):")
    image1.display()
    
    print("\nDisplaying image 1 again (already loaded):")
    image1.display()
    
    print("\nDisplaying image 2 (loads now):")
    image2.display()
    print()
    
    # Example 2: Protection Proxy
    print("Example 2: Protection Proxy")
    print("-" * 70)
    
    account = BankAccount(1000.0)
    
    admin_proxy = AccountProxy(account, "admin")
    user_proxy = AccountProxy(account, "user")
    
    print("Admin trying to withdraw:")
    admin_proxy.withdraw(100.0)
    
    print("\nUser trying to withdraw:")
    user_proxy.withdraw(50.0)
    
    print(f"\nBalance (accessible to all): ${account.get_balance():.2f}")
    print()
    
    # Example 3: Virtual Proxy
    print("Example 3: Virtual Proxy - Lazy Initialization")
    print("-" * 70)
    
    print("Creating proxy (no object created yet)...")
    proxy = ExpensiveObjectProxy()
    
    print("Calling process (creates object now):")
    result = proxy.process()
    print(result)
    
    print("\nCalling process again (object already created):")
    result = proxy.process()
    print(result)
    print()
    
    # Example 4: Remote Proxy with Caching
    print("Example 4: Remote Proxy with Caching")
    print("-" * 70)
    
    remote_proxy = RemoteServiceProxy()
    
    print("First call (calls remote service):")
    result1 = remote_proxy.expensive_operation()
    print(f"Result: {result1}")
    
    print("\nSecond call (uses cache):")
    result2 = remote_proxy.expensive_operation()
    print(f"Result: {result2}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Provide a surrogate or placeholder for another object")
    print("  to control access to it.")
    print("\nTypes of Proxies:")
    print("  1. Virtual Proxy: Lazy initialization")
    print("  2. Protection Proxy: Access control")
    print("  3. Remote Proxy: Local representative for remote object")
    print("  4. Smart Proxy: Additional functionality (caching, logging)")
    print("\nKey Advantages:")
    print("  - Control access to real subject")
    print("  - Lazy initialization")
    print("  - Additional functionality (caching, logging)")
    print("  - Security and access control")
    print("\nKey Disadvantages:")
    print("  - Additional layer of indirection")
    print("  - Can complicate code")
    print("  - Performance overhead")
    print("\nWhen to Use:")
    print("  - Lazy initialization")
    print("  - Access control")
    print("  - Remote object access")
    print("  - Caching")
    print("  - Logging and monitoring")
    print("\nCommon Use Cases:")
    print("  - Lazy loading (images, data)")
    print("  - Access control")
    print("  - Caching")
    print("  - Remote method invocation")
    print("  - Logging and monitoring")
    print("=" * 70)


if __name__ == "__main__":
    main()
