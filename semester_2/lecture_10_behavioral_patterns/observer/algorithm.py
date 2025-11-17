#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Observer Design Pattern.

Defines a one-to-many dependency between objects so that when one object
changes state, all its dependents are notified and updated automatically.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Any
from enum import Enum
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Observer Interface
class Observer(ABC):
    """Abstract observer interface."""
    
    @abstractmethod
    def update(self, data: Any) -> None:
        """Called when subject notifies observers."""
        
    
    """
    Observer pattern implementation.
    """
    def update(self):
        pass
    
    def execute(self):
        """Execute pattern logic."""
        pass


def main() -> None:
    """Demonstration of Observer Pattern."""
    logger.info("=" * 70)
    logger.info("OBSERVER DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: News Agency
    logger.info("Example 1: News Agency (Publisher-Subscriber)")
    logger.info("-" * 70)
    
    agency = NewsAgency()
    
    channel1 = NewsChannel("CNN")
    channel2 = NewsChannel("BBC")
    email1 = EmailSubscriber("user@example.com")
    
    agency.attach(channel1)
    agency.attach(channel2)
    agency.attach(email1)
    
    agency.set_news("Breaking: New algorithm discovered!")
    logger.info()
    
    agency.detach(channel2)
    agency.set_news("Update: Algorithm implementation complete!")
    logger.info()
    
    # Example 2: Weather Station
    logger.info("Example 2: Weather Station")
    logger.info("-" * 70)
    
    weather = WeatherData()
    
    display1 = CurrentConditionsDisplay("Mobile App")
    display2 = CurrentConditionsDisplay("Website")
    
    weather.attach(display1)
    weather.attach(display2)
    
    weather.set_measurements(75.0, 65.0, 30.4)
    logger.info()
    
    weather.set_measurements(80.0, 70.0, 30.2)
    logger.info()
    
    # Example 3: Stock Market
    logger.info("Example 3: Stock Market Trading")
    logger.info("-" * 70)
    
    apple = Stock("AAPL", 150.00)
    
    trader1 = StockTrader("Alice", buy_threshold=145.0, 
                         sell_threshold=160.0)
    trader2 = StockTrader("Bob", buy_threshold=140.0)
    
    apple.attach(trader1)
    apple.attach(trader2)
    
    apple.set_price(148.50)  # Price drop
    apple.set_price(142.00)  # Below buy threshold
    apple.set_price(155.00)  # Price rise
    apple.set_price(162.00)  # Above sell threshold
    logger.info()
    
    # Example 4: Multiple subjects, multiple observers
    logger.info("Example 4: Multiple Subjects and Observers")
    logger.info("-" * 70)
    
    google = Stock("GOOGL", 2500.00)
    microsoft = Stock("MSFT", 350.00)
    
    multi_trader = StockTrader("Charlie")
    
    google.attach(multi_trader)
    microsoft.attach(multi_trader)
    
    google.set_price(2550.00)
    microsoft.set_price(345.00)
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Define a one-to-many dependency between objects so")
    logger.info("  that when one object changes state, all dependents")
    logger.info("  are notified and updated automatically.")
    logger.info("\nKey Advantages:")
    logger.info("  - Loose coupling between subject and observers")
    logger.info("  - Dynamic subscription/unsubscription")
    logger.info("  - Open/Closed Principle (easy to add observers)")
    logger.info("  - Broadcast communication")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Unexpected updates (observers don't know about each other)")
    logger.info("  - Performance overhead (many notifications)")
    logger.info("  - Memory leaks if observers not properly detached")
    logger.info("\nWhen to Use:")
    logger.info("  - When change to one object requires changing others")
    logger.info("  - When number of dependents is unknown or dynamic")
    logger.info("  - When objects should be loosely coupled")
    logger.info("  - Event-driven systems")
    logger.info("\nWhen NOT to Use:")
    logger.info("  - When updates are too frequent (performance)")
    logger.info("  - When tight coupling is acceptable")
    logger.info("  - When order of notifications matters critically")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Model-View-Controller (MVC) architecture")
    logger.info("  - Event handling systems")
    logger.info("  - Publish-Subscribe systems")
    logger.info("  - Stock market monitoring")
    logger.info("  - Weather monitoring systems")
    logger.info("  - GUI frameworks (button clicks, etc.)")
    logger.info("\nVariations:")
    logger.info("  - Push model: Subject sends data to observers")
    logger.info("  - Pull model: Observers request data from subject")
    logger.info("  - Event bus: Centralized event distribution")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()