#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publish-Subscribe (Pub-Sub) Pattern.

Decouples publishers from subscribers. Publishers send messages to
topics/channels without knowing who subscribes. Subscribers listen to
topics they're interested in.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, List, Callable, Any
import threading

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class Subscriber(ABC):
    """Abstract subscriber interface."""
    
    @abstractmethod
    def update(self, topic: str, message: Any) -> None:
        """Receive message from topic."""
        
    """
    Publish Subscribe implementation.
    
    Args:
        *args: Variable arguments
        **kwargs: Keyword arguments
        
    Returns:
        Algorithm result
    """
    # Implementation for publish_subscribe
    logger.info(f"Executing publish_subscribe")
    return None


def main() -> None:
    """Demonstration of Publish-Subscribe Pattern."""
    logger.info("=" * 70)
    logger.info("PUBLISH-SUBSCRIBE (PUB-SUB) PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic Pub-Sub
    logger.info("Example 1: Basic Publish-Subscribe")
    logger.info("-" * 70)
    
    broker = MessageBroker()
    publisher = Publisher(broker)
    
    # Create subscribers
    email_sub = EmailSubscriber("user@example.com")
    log_sub = LogSubscriber()
    notif_sub = NotificationSubscriber("user123")
    
    # Subscribe to topics
    broker.subscribe("orders", email_sub)
    broker.subscribe("orders", log_sub)
    broker.subscribe("notifications", notif_sub)
    broker.subscribe("notifications", log_sub)
    
    # Publish messages
    logger.info("Publishing messages:")
    publisher.publish("orders", "New order #1001")
    publisher.publish("notifications", "User logged in")
    publisher.publish("orders", "Order #1001 shipped")
    logger.info()
    
    # Example 2: Event-driven Pub-Sub
    logger.info("Example 2: Event-driven Pub-Sub")
    logger.info("-" * 70)
    
    event_bus = EventBus()
    
    def order_handler(event: Event) -> None:
        logger.info(f"Order handler: {event.data}")
    
    def user_handler(event: Event) -> None:
        logger.info(f"User handler: {event.data}")
    
    event_bus.subscribe("order.created", order_handler)
    event_bus.subscribe("user.registered", user_handler)
    
    logger.info("Publishing events:")
    event_bus.publish(Event("order.created", "Order #2001"))
    event_bus.publish(Event("user.registered", "User: alice"))
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Pub-Sub")
    
    def pub_sub_operations():
        broker = MessageBroker()
        publisher = Publisher(broker)
        
        # Create multiple subscribers
        for i in range(10):
            sub = EmailSubscriber(f"user{i}@example.com")
            broker.subscribe("test", sub)
        
        # Publish messages
        for i in range(100):
            publisher.publish("test", f"Message {i}")
        
        return len(broker.subscribers.get("test", []))
    
    result, metrics = timer.measure(pub_sub_operations)
    logger.info(f"Time to publish 100 messages to 10 subscribers: "
          f"{metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Decouples publishers from subscribers. Publishers send")
    logger.info("  messages to topics without knowing subscribers.")
    logger.info("\nKey Advantages:")
    logger.info("  - Loose coupling")
    logger.info("  - Scalable")
    logger.info("  - Dynamic subscription")
    logger.info("  - Multiple subscribers per topic")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Message delivery not guaranteed")
    logger.info("  - Ordering challenges")
    logger.info("  - Debugging complexity")
    logger.info("\nWhen to Use:")
    logger.info("  - Event-driven architecture")
    logger.info("  - Microservices communication")
    logger.info("  - Real-time notifications")
    logger.info("  - Decoupled systems")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Apache Kafka")
    logger.info("  - RabbitMQ")
    logger.info("  - Redis Pub/Sub")
    logger.info("  - Event-driven systems")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()