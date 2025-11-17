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
        
    """
    Proxy implementation.
    
    Args:
        *args: Variable arguments
        **kwargs: Keyword arguments
        
    Returns:
        Algorithm result
    """
    # Implementation for proxy
    logger.info(f"Executing proxy")
    return None


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