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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("Example 1: News Agency")
    logger.info("-" * 70)
    
    agency = NewsAgency()
    
    channel1 = NewsChannel("CNN")
    channel2 = NewsChannel("BBC")
    subscriber = EmailSubscriber("user@example.com")
    
    agency.attach(channel1)
    agency.attach(channel2)
    agency.attach(subscriber)
    
    logger.info("Breaking news published:")
    agency.set_news("Breaking: New technology breakthrough!")
    logger.info()
    
    agency.detach(channel2)
    logger.info("BBC unsubscribed. Publishing another news:")
    agency.set_news("Update: Technology details released")
    logger.info()
    
    # Example 2: Weather Station
    logger.info("Example 2: Weather Station")
    logger.info("-" * 70)
    
    weather_station = WeatherData()
    display = CurrentConditionsDisplay()
    
    weather_station.attach(display)
    
    logger.info("Weather measurements updated:")
    weather_station.set_measurements(75.0, 65.0, 30.4)
    logger.info()
    
    weather_station.set_measurements(80.0, 70.0, 29.2)
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Observer")
    
    def observer_operations():
        agency = NewsAgency()
        for i in range(10):
            channel = NewsChannel(f"Channel{i}")
            agency.attach(channel)
        agency.set_news("Test news")
        return len(agency.observers)
    
    result, metrics = timer.measure(observer_operations)
    logger.info(f"Time to notify 10 observers: {metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Define a one-to-many dependency between objects so that")
    logger.info("  when one object changes state, all its dependents are")
    logger.info("  notified and updated automatically.")
    logger.info("\nKey Advantages:")
    logger.info("  - Loose coupling between subject and observers")
    logger.info("  - Dynamic subscription/unsubscription")
    logger.info("  - Broadcast communication")
    logger.info("  - Open/Closed Principle support")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Unexpected updates")
    logger.info("  - Memory leaks if observers not detached")
    logger.info("  - Order of notification not guaranteed")
    logger.info("\nWhen to Use:")
    logger.info("  - Change to one object requires changing others")
    logger.info("  - Number of dependent objects is unknown")
    logger.info("  - Objects should be loosely coupled")
    logger.info("  - Event-driven systems")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Model-View architectures")
    logger.info("  - Event handling systems")
    logger.info("  - Publish-Subscribe systems")
    logger.info("  - GUI frameworks")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()