#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Message Queue Pattern.

Asynchronous communication pattern where messages are sent to a queue
and processed by consumers. Decouples producers from consumers.
"""

import sys
from pathlib import Path
import queue
import threading
import time
from typing import Any, Callable, Optional
from dataclasses import dataclass
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


@dataclass
class Message:
    """Message structure."""
    id: int
    topic: str
    payload: Any
    timestamp: datetime
    
    def __str__(self) -> str:
        return f"Message(id={self.id}, topic='{self.topic}', payload='{self.payload}')"


class MessageQueue:
    """Simple message queue implementation."""
    
    def __init__(self, maxsize: int = 100):
        """
        Initialize message queue.
        
        Args:
            maxsize: Maximum queue size
        """
        self.queue = queue.Queue(maxsize=maxsize)
        self.message_id = 0
        self.lock = threading.Lock()
    
    def publish(self, topic: str, payload: Any) -> int:
        """
        Publish message to queue.
        
        Args:
            topic: Message topic
            payload: Message payload
            
        Returns:
            Message ID
        """
        with self.lock:
            self.message_id += 1
            message = Message(
                id=self.message_id,
                topic=topic,
                payload=payload,
                timestamp=datetime.now()
            )
            self.queue.put(message)
            return message.id
    
    def consume(self, timeout: Optional[float] = None) -> Optional[Message]:
        """
        Consume message from queue.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Message or None if timeout
        """
        try:
            return self.queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def size(self) -> int:
        """Get queue size."""
        return self.queue.qsize()


class Producer:
    """Message producer."""
    
    def __init__(self, name: str, message_queue: MessageQueue):
        self.name = name
        self.queue = message_queue
    
    def send(self, topic: str, payload: Any) -> int:
        """Send message."""
        msg_id = self.queue.publish(topic, payload)
        logger.info(f"[{self.name}] Published: {topic} - {payload}")
        return msg_id


class Consumer:
    """Message consumer."""
    
    def __init__(self, name: str, message_queue: MessageQueue, 
                 topics: list = None):
        self.name = name
        self.queue = message_queue
        self.topics = topics or []
        self.running = False
        self.thread: Optional[threading.Thread] = None
    
    def start(self) -> None:
        """Start consuming messages."""
        self.running = True
        self.thread = threading.Thread(target=self._consume_loop, daemon=True)
        self.thread.start()
    
    def stop(self) -> None:
        """Stop consuming messages."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
    
    def _consume_loop(self) -> None:
        """Consume messages in loop."""
        while self.running:
            message = self.queue.consume(timeout=1)
            if message:
                if not self.topics or message.topic in self.topics:
                    self.process(message)
    
    def process(self, message: Message) -> None:
        """Process message."""
        logger.info(f"[{self.name}] Consumed: {message}")
        # Mark message as processed
        self.queue.queue.task_done()


# Example 2: Topic-based Queue
class TopicQueue:
    """Topic-based message queue."""
    
    def __init__(self):
        self.queues: dict[str, queue.Queue] = {}
        self.lock = threading.Lock()
    
    def create_topic(self, topic: str, maxsize: int = 100) -> None:
        """Create topic queue."""
        with self.lock:
            if topic not in self.queues:
                self.queues[topic] = queue.Queue(maxsize=maxsize)
    
    def publish(self, topic: str, payload: Any) -> bool:
        """Publish to topic."""
        if topic not in self.queues:
            self.create_topic(topic)
        
        try:
            self.queues[topic].put(payload, block=False)
            return True
        except queue.Full:
            return False
    
    def subscribe(self, topic: str, callback: Callable) -> None:
        """Subscribe to topic."""
        if topic not in self.queues:
            self.create_topic(topic)
        
        def consume():
            while True:
                try:
                    payload = self.queues[topic].get(timeout=1)
                    callback(topic, payload)
                    self.queues[topic].task_done()
                except queue.Empty:
                    continue
        
        thread = threading.Thread(target=consume, daemon=True)
        thread.start()


def main() -> None:
    """Demonstration of Message Queue Pattern."""
    logger.info("=" * 70)
    logger.info("MESSAGE QUEUE PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic Message Queue
    logger.info("Example 1: Basic Message Queue")
    logger.info("-" * 70)
    
    mq = MessageQueue()
    
    # Create producer and consumers
    producer = Producer("Producer1", mq)
    consumer1 = Consumer("Consumer1", mq)
    consumer2 = Consumer("Consumer2", mq)
    
    # Start consumers
    consumer1.start()
    consumer2.start()
    
    # Produce messages
    producer.send("orders", "Order #1001")
    producer.send("orders", "Order #1002")
    producer.send("notifications", "User logged in")
    producer.send("orders", "Order #1003")
    
    time.sleep(0.5)  # Allow consumers to process
    
    consumer1.stop()
    consumer2.stop()
    logger.info()
    
    # Example 2: Topic-based Queue
    logger.info("Example 2: Topic-based Message Queue")
    logger.info("-" * 70)
    
    topic_queue = TopicQueue()
    
    def order_handler(topic: str, payload: Any) -> None:
        logger.info(f"Order handler received: {payload}")
    
    def notification_handler(topic: str, payload: Any) -> None:
        logger.info(f"Notification handler received: {payload}")
    
    # Subscribe to topics
    topic_queue.subscribe("orders", order_handler)
    topic_queue.subscribe("notifications", notification_handler)
    
    # Publish messages
    topic_queue.publish("orders", "Order #2001")
    topic_queue.publish("notifications", "Email sent")
    topic_queue.publish("orders", "Order #2002")
    
    time.sleep(0.5)
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Message Queue")
    
    def queue_operations():
        mq = MessageQueue()
        producer = Producer("P", mq)
        
        for i in range(100):
            producer.send("test", f"Message {i}")
        return mq.size()
    
    result, metrics = timer.measure(queue_operations)
    logger.info(f"Time to publish 100 messages: {metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Queue size: {result}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Asynchronous communication pattern where messages are")
    logger.info("  sent to a queue and processed by consumers. Decouples")
    logger.info("  producers from consumers.")
    logger.info("\nKey Advantages:")
    logger.info("  - Decouples producers and consumers")
    logger.info("  - Asynchronous processing")
    logger.info("  - Load balancing")
    logger.info("  - Reliability (messages persist)")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Additional infrastructure")
    logger.info("  - Message ordering challenges")
    logger.info("  - Complexity in error handling")
    logger.info("  - Potential message loss")
    logger.info("\nWhen to Use:")
    logger.info("  - Asynchronous processing needed")
    logger.info("  - Decouple components")
    logger.info("  - Load balancing")
    logger.info("  - Event-driven architecture")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Apache Kafka")
    logger.info("  - RabbitMQ")
    logger.info("  - Amazon SQS")
    logger.info("  - Azure Service Bus")
    logger.info("  - Microservices communication")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()