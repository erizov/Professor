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
        pass


# Subject Interface
class Subject(ABC):
    """Abstract subject interface."""
    
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        pass
    
    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        pass
    
    @abstractmethod
    def notify(self) -> None:
        """Notify all observers."""
        pass


# Concrete Subject
class NewsAgency(Subject):
    """News agency that publishes news."""
    
    def __init__(self):
        self._observers: List[Observer] = []
        self._news: str = ""
    
    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
            logger.info(f"Observer {observer} attached")
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
            logger.info(f"Observer {observer} detached")
    
    def notify(self) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(self._news)
    
    def set_news(self, news: str) -> None:
        """Set news and notify observers."""
        self._news = news
        logger.info(f"\nNews Agency: Publishing news - '{news}'")
        self.notify()


# Concrete Observers
class NewsChannel(Observer):
    """News channel that displays news."""
    
    def __init__(self, name: str):
        self.name = name
        self.news: str = ""
    
    def update(self, data: str) -> None:
        """Update with new news."""
        self.news = data
        logger.info(f"  {self.name}: Received news - '{self.news}'")
    
    def __repr__(self) -> str:
        return f"NewsChannel({self.name})"


class EmailSubscriber(Observer):
    """Email subscriber that receives news via email."""
    
    def __init__(self, email: str):
        self.email = email
        self.news: str = ""
    
    def update(self, data: str) -> None:
        """Update with new news."""
        self.news = data
        logger.info(f"  Email to {self.email}: '{self.news}'")
    
    def __repr__(self) -> str:
        return f"EmailSubscriber({self.email})"


# Weather Station Example
class WeatherData(Subject):
    """Weather station that publishes weather updates."""
    
    def __init__(self):
        self._observers: List[Observer] = []
        self._temperature: float = 0.0
        self._humidity: float = 0.0
        self._pressure: float = 0.0
    
    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(self)
    
    def set_measurements(self, temperature: float, 
                        humidity: float, pressure: float) -> None:
        """Set weather measurements and notify."""
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self.notify()
    
    def get_temperature(self) -> float:
        return self._temperature
    
    def get_humidity(self) -> float:
        return self._humidity
    
    def get_pressure(self) -> float:
        return self._pressure


class CurrentConditionsDisplay(Observer):
    """Display current weather conditions."""
    
    def __init__(self, name: str):
        self.name = name
        self.temperature: float = 0.0
        self.humidity: float = 0.0
    
    def update(self, data: Any) -> None:
        """Update with weather data."""
        if isinstance(data, WeatherData):
            self.temperature = data.get_temperature()
            self.humidity = data.get_humidity()
            logger.info(f"  {self.name} Display:")
            logger.info(f"    Temperature: {self.temperature}°F")
            logger.info(f"    Humidity: {self.humidity}%")
    
    def __repr__(self) -> str:
        return f"CurrentConditionsDisplay({self.name})"


# Stock Market Example
class Stock(Subject):
    """Stock that notifies observers of price changes."""
    
    def __init__(self, symbol: str, price: float):
        self._observers: List[Observer] = []
        self.symbol = symbol
        self._price = price
    
    def attach(self, observer: Observer) -> None:
        """Attach an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(self)
    
    def set_price(self, price: float) -> None:
        """Set price and notify observers."""
        old_price = self._price
        self._price = price
        change = price - old_price
        change_pct = (change / old_price * 100) if old_price > 0 else 0
        
        logger.info(f"\n{self.symbol}: ${old_price:.2f} → ${price:.2f} "
              f"({change:+.2f}, {change_pct:+.2f}%)")
        self.notify()
    
    def get_price(self) -> float:
        return self._price


class StockTrader(Observer):
    """Trader that reacts to stock price changes."""
    
    def __init__(self, name: str, buy_threshold: float = None,
                 sell_threshold: float = None):
        self.name = name
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.last_price: float = 0.0
    
    def update(self, data: Any) -> None:
        """React to stock price change."""
        if isinstance(data, Stock):
            price = data.get_price()
            change = price - self.last_price if self.last_price > 0 else 0
            
            logger.info(f"  {self.name}: {data.symbol} = ${price:.2f}")
            
            if self.buy_threshold and price <= self.buy_threshold:
                logger.info(" → BUY SIGNAL!")
            elif self.sell_threshold and price >= self.sell_threshold:
                logger.info(" → SELL SIGNAL!")
            else:
                logger.info()
            
            self.last_price = price
    
    def __repr__(self) -> str:
        return f"StockTrader({self.name})"


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