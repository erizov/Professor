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

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


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
    """News agency subject."""
    
    def __init__(self):
        self.observers: List[Observer] = []
        self.news: str = ""
    
    def attach(self, observer: Observer) -> None:
        """Attach observer."""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach observer."""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify(self) -> None:
        """Notify all observers."""
        for observer in self.observers:
            observer.update(self.news)
    
    def set_news(self, news: str) -> None:
        """Set news and notify observers."""
        self.news = news
        self.notify()


# Concrete Observers
class NewsChannel(Observer):
    """News channel observer."""
    
    def __init__(self, name: str):
        self.name = name
        self.latest_news: str = ""
    
    def update(self, data: Any) -> None:
        """Update with new news."""
        self.latest_news = data
        print(f"{self.name} received: {data}")
    
    def get_latest_news(self) -> str:
        """Get latest news."""
        return self.latest_news


class EmailSubscriber(Observer):
    """Email subscriber observer."""
    
    def __init__(self, email: str):
        self.email = email
        self.news_updates: List[str] = []
    
    def update(self, data: Any) -> None:
        """Update with new news."""
        self.news_updates.append(data)
        print(f"Email sent to {self.email}: {data}")


# Example 2: Weather Station
class WeatherData(Subject):
    """Weather data subject."""
    
    def __init__(self):
        self.observers: List[Observer] = []
        self.temperature: float = 0.0
        self.humidity: float = 0.0
        self.pressure: float = 0.0
    
    def attach(self, observer: Observer) -> None:
        """Attach observer."""
        if observer not in self.observers:
            self.observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach observer."""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify(self) -> None:
        """Notify all observers."""
        data = {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure
        }
        for observer in self.observers:
            observer.update(data)
    
    def set_measurements(self, temperature: float, humidity: float, 
                        pressure: float) -> None:
        """Set measurements and notify."""
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.notify()


class CurrentConditionsDisplay(Observer):
    """Current conditions display observer."""
    
    def __init__(self):
        self.temperature: float = 0.0
        self.humidity: float = 0.0
    
    def update(self, data: Any) -> None:
        """Update display."""
        if isinstance(data, dict):
            self.temperature = data.get('temperature', 0.0)
            self.humidity = data.get('humidity', 0.0)
            self.display()
    
    def display(self) -> None:
        """Display current conditions."""
        print(f"Current conditions: {self.temperature}°F, "
              f"{self.humidity}% humidity")


def main() -> None:
    """Demonstration of Observer Pattern."""
    print("=" * 70)
    print("OBSERVER DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: News Agency
    print("Example 1: News Agency")
    print("-" * 70)
    
    agency = NewsAgency()
    
    channel1 = NewsChannel("CNN")
    channel2 = NewsChannel("BBC")
    subscriber = EmailSubscriber("user@example.com")
    
    agency.attach(channel1)
    agency.attach(channel2)
    agency.attach(subscriber)
    
    print("Breaking news published:")
    agency.set_news("Breaking: New technology breakthrough!")
    print()
    
    agency.detach(channel2)
    print("BBC unsubscribed. Publishing another news:")
    agency.set_news("Update: Technology details released")
    print()
    
    # Example 2: Weather Station
    print("Example 2: Weather Station")
    print("-" * 70)
    
    weather_station = WeatherData()
    display = CurrentConditionsDisplay()
    
    weather_station.attach(display)
    
    print("Weather measurements updated:")
    weather_station.set_measurements(75.0, 65.0, 30.4)
    print()
    
    weather_station.set_measurements(80.0, 70.0, 29.2)
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Observer")
    
    def observer_operations():
        agency = NewsAgency()
        for i in range(10):
            channel = NewsChannel(f"Channel{i}")
            agency.attach(channel)
        agency.set_news("Test news")
        return len(agency.observers)
    
    result, metrics = timer.measure(observer_operations)
    print(f"Time to notify 10 observers: {metrics['execution_time_ms']:.3f} ms")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Define a one-to-many dependency between objects so that")
    print("  when one object changes state, all its dependents are")
    print("  notified and updated automatically.")
    print("\nKey Advantages:")
    print("  - Loose coupling between subject and observers")
    print("  - Dynamic subscription/unsubscription")
    print("  - Broadcast communication")
    print("  - Open/Closed Principle support")
    print("\nKey Disadvantages:")
    print("  - Unexpected updates")
    print("  - Memory leaks if observers not detached")
    print("  - Order of notification not guaranteed")
    print("\nWhen to Use:")
    print("  - Change to one object requires changing others")
    print("  - Number of dependent objects is unknown")
    print("  - Objects should be loosely coupled")
    print("  - Event-driven systems")
    print("\nCommon Use Cases:")
    print("  - Model-View architectures")
    print("  - Event handling systems")
    print("  - Publish-Subscribe systems")
    print("  - GUI frameworks")
    print("=" * 70)


if __name__ == "__main__":
    main()
