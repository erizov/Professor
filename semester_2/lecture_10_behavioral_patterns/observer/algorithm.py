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
            print(f"Observer {observer} attached")
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Observer {observer} detached")
    
    def notify(self) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(self._news)
    
    def set_news(self, news: str) -> None:
        """Set news and notify observers."""
        self._news = news
        print(f"\nNews Agency: Publishing news - '{news}'")
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
        print(f"  {self.name}: Received news - '{self.news}'")
    
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
        print(f"  Email to {self.email}: '{self.news}'")
    
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
            print(f"  {self.name} Display:")
            print(f"    Temperature: {self.temperature}°F")
            print(f"    Humidity: {self.humidity}%")
    
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
        
        print(f"\n{self.symbol}: ${old_price:.2f} → ${price:.2f} "
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
            
            print(f"  {self.name}: {data.symbol} = ${price:.2f}", end="")
            
            if self.buy_threshold and price <= self.buy_threshold:
                print(" → BUY SIGNAL!")
            elif self.sell_threshold and price >= self.sell_threshold:
                print(" → SELL SIGNAL!")
            else:
                print()
            
            self.last_price = price
    
    def __repr__(self) -> str:
        return f"StockTrader({self.name})"


def main() -> None:
    """Demonstration of Observer Pattern."""
    print("=" * 70)
    print("OBSERVER DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: News Agency
    print("Example 1: News Agency (Publisher-Subscriber)")
    print("-" * 70)
    
    agency = NewsAgency()
    
    channel1 = NewsChannel("CNN")
    channel2 = NewsChannel("BBC")
    email1 = EmailSubscriber("user@example.com")
    
    agency.attach(channel1)
    agency.attach(channel2)
    agency.attach(email1)
    
    agency.set_news("Breaking: New algorithm discovered!")
    print()
    
    agency.detach(channel2)
    agency.set_news("Update: Algorithm implementation complete!")
    print()
    
    # Example 2: Weather Station
    print("Example 2: Weather Station")
    print("-" * 70)
    
    weather = WeatherData()
    
    display1 = CurrentConditionsDisplay("Mobile App")
    display2 = CurrentConditionsDisplay("Website")
    
    weather.attach(display1)
    weather.attach(display2)
    
    weather.set_measurements(75.0, 65.0, 30.4)
    print()
    
    weather.set_measurements(80.0, 70.0, 30.2)
    print()
    
    # Example 3: Stock Market
    print("Example 3: Stock Market Trading")
    print("-" * 70)
    
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
    print()
    
    # Example 4: Multiple subjects, multiple observers
    print("Example 4: Multiple Subjects and Observers")
    print("-" * 70)
    
    google = Stock("GOOGL", 2500.00)
    microsoft = Stock("MSFT", 350.00)
    
    multi_trader = StockTrader("Charlie")
    
    google.attach(multi_trader)
    microsoft.attach(multi_trader)
    
    google.set_price(2550.00)
    microsoft.set_price(345.00)
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Define a one-to-many dependency between objects so")
    print("  that when one object changes state, all dependents")
    print("  are notified and updated automatically.")
    print("\nKey Advantages:")
    print("  - Loose coupling between subject and observers")
    print("  - Dynamic subscription/unsubscription")
    print("  - Open/Closed Principle (easy to add observers)")
    print("  - Broadcast communication")
    print("\nKey Disadvantages:")
    print("  - Unexpected updates (observers don't know about each other)")
    print("  - Performance overhead (many notifications)")
    print("  - Memory leaks if observers not properly detached")
    print("\nWhen to Use:")
    print("  - When change to one object requires changing others")
    print("  - When number of dependents is unknown or dynamic")
    print("  - When objects should be loosely coupled")
    print("  - Event-driven systems")
    print("\nWhen NOT to Use:")
    print("  - When updates are too frequent (performance)")
    print("  - When tight coupling is acceptable")
    print("  - When order of notifications matters critically")
    print("\nCommon Use Cases:")
    print("  - Model-View-Controller (MVC) architecture")
    print("  - Event handling systems")
    print("  - Publish-Subscribe systems")
    print("  - Stock market monitoring")
    print("  - Weather monitoring systems")
    print("  - GUI frameworks (button clicks, etc.)")
    print("\nVariations:")
    print("  - Push model: Subject sends data to observers")
    print("  - Pull model: Observers request data from subject")
    print("  - Event bus: Centralized event distribution")
    print("=" * 70)


if __name__ == "__main__":
    main()

