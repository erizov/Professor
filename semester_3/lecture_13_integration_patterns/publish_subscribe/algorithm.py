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


class Subscriber(ABC):
    """Abstract subscriber interface."""
    
    @abstractmethod
    def update(self, topic: str, message: Any) -> None:
        """Receive message from topic."""
        pass


class Publisher:
    """Publisher that sends messages to topics."""
    
    def __init__(self, broker: 'MessageBroker'):
        self.broker = broker
    
    def publish(self, topic: str, message: Any) -> None:
        """Publish message to topic."""
        self.broker.publish(topic, message)


class MessageBroker:
    """Message broker managing topics and subscribers."""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Subscriber]] = {}
        self.lock = threading.Lock()
    
    def subscribe(self, topic: str, subscriber: Subscriber) -> None:
        """Subscribe to topic."""
        with self.lock:
            if topic not in self.subscribers:
                self.subscribers[topic] = []
            if subscriber not in self.subscribers[topic]:
                self.subscribers[topic].append(subscriber)
    
    def unsubscribe(self, topic: str, subscriber: Subscriber) -> None:
        """Unsubscribe from topic."""
        with self.lock:
            if topic in self.subscribers:
                if subscriber in self.subscribers[topic]:
                    self.subscribers[topic].remove(subscriber)
    
    def publish(self, topic: str, message: Any) -> None:
        """Publish message to all subscribers of topic."""
        with self.lock:
            if topic in self.subscribers:
                for subscriber in self.subscribers[topic]:
                    subscriber.update(topic, message)


# Concrete Subscribers
class EmailSubscriber(Subscriber):
    """Email subscriber."""
    
    def __init__(self, email: str):
        self.email = email
        self.messages: List[tuple] = []
    
    def update(self, topic: str, message: Any) -> None:
        """Receive message."""
        self.messages.append((topic, message))
        print(f"[Email to {self.email}] Topic: {topic}, Message: {message}")


class LogSubscriber(Subscriber):
    """Logging subscriber."""
    
    def __init__(self):
        self.logs: List[tuple] = []
    
    def update(self, topic: str, message: Any) -> None:
        """Receive message."""
        self.logs.append((topic, message))
        print(f"[LOG] {topic}: {message}")


class NotificationSubscriber(Subscriber):
    """Notification subscriber."""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.notifications: List[tuple] = []
    
    def update(self, topic: str, message: Any) -> None:
        """Receive message."""
        self.notifications.append((topic, message))
        print(f"[Notification to User {self.user_id}] {topic}: {message}")


# Example 2: Event-driven Pub-Sub
class Event:
    """Event object."""
    
    def __init__(self, event_type: str, data: Any):
        self.event_type = event_type
        self.data = data
        self.timestamp = None


class EventBus:
    """Event bus for pub-sub."""
    
    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}
        self.lock = threading.Lock()
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to event type."""
        with self.lock:
            if event_type not in self.handlers:
                self.handlers[event_type] = []
            if handler not in self.handlers[event_type]:
                self.handlers[event_type].append(handler)
    
    def publish(self, event: Event) -> None:
        """Publish event."""
        with self.lock:
            if event.event_type in self.handlers:
                for handler in self.handlers[event.event_type]:
                    handler(event)


def main() -> None:
    """Demonstration of Publish-Subscribe Pattern."""
    print("=" * 70)
    print("PUBLISH-SUBSCRIBE (PUB-SUB) PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic Pub-Sub
    print("Example 1: Basic Publish-Subscribe")
    print("-" * 70)
    
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
    print("Publishing messages:")
    publisher.publish("orders", "New order #1001")
    publisher.publish("notifications", "User logged in")
    publisher.publish("orders", "Order #1001 shipped")
    print()
    
    # Example 2: Event-driven Pub-Sub
    print("Example 2: Event-driven Pub-Sub")
    print("-" * 70)
    
    event_bus = EventBus()
    
    def order_handler(event: Event) -> None:
        print(f"Order handler: {event.data}")
    
    def user_handler(event: Event) -> None:
        print(f"User handler: {event.data}")
    
    event_bus.subscribe("order.created", order_handler)
    event_bus.subscribe("user.registered", user_handler)
    
    print("Publishing events:")
    event_bus.publish(Event("order.created", "Order #2001"))
    event_bus.publish(Event("user.registered", "User: alice"))
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
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
    print(f"Time to publish 100 messages to 10 subscribers: "
          f"{metrics['execution_time_ms']:.3f} ms")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Decouples publishers from subscribers. Publishers send")
    print("  messages to topics without knowing subscribers.")
    print("\nKey Advantages:")
    print("  - Loose coupling")
    print("  - Scalable")
    print("  - Dynamic subscription")
    print("  - Multiple subscribers per topic")
    print("\nKey Disadvantages:")
    print("  - Message delivery not guaranteed")
    print("  - Ordering challenges")
    print("  - Debugging complexity")
    print("\nWhen to Use:")
    print("  - Event-driven architecture")
    print("  - Microservices communication")
    print("  - Real-time notifications")
    print("  - Decoupled systems")
    print("\nCommon Use Cases:")
    print("  - Apache Kafka")
    print("  - RabbitMQ")
    print("  - Redis Pub/Sub")
    print("  - Event-driven systems")
    print("=" * 70)


if __name__ == "__main__":
    main()
