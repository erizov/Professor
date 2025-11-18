#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Message Queue implementation.

This file contains the implementation of the Message Queue algorithm.
"""

from typing import List, Optional, Dict, Set


from queue import Queue
import threading

class MessageQueue:
    """Simple message queue implementation."""
    def __init__(self, max_size: int = 1000):
        self.queue = Queue(maxsize=max_size)
        self.subscribers: List[callable] = []
        self.running = False
        self.worker_thread = None
    
    def publish(self, message: any) -> bool:
        """Publish message."""
        try:
            self.queue.put(message, block=False)
            return True
        except:
            return False
    
    def subscribe(self, handler: callable) -> None:
        """Subscribe to messages."""
        self.subscribers.append(handler)
    
    def start(self) -> None:
        """Start processing messages."""
        self.running = True
        self.worker_thread = threading.Thread(target=self._process_messages)
        self.worker_thread.start()
    
    def stop(self) -> None:
        """Stop processing messages."""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join()
    
    def _process_messages(self) -> None:
        """Process messages in background."""
        while self.running:
            try:
                message = self.queue.get(timeout=1)
                for handler in self.subscribers:
                    handler(message)
            except:
                continue


def main() -> None:
    """Demonstrate Message Queue."""
    print("=" * 70)
    print("MESSAGE QUEUE")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Message Queue")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
