#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Publish Subscribe implementation.

This file contains the implementation of the Publish Subscribe algorithm.
"""

from typing import List, Optional, Dict, Set


class PubSub:
    """Publish-subscribe pattern."""

    def __init__(self):
        self.topics: Dict[str, List[callable]] = {}

    def subscribe(self, topic: str, callback: callable) -> None:
        """Subscribe to topic."""
        if topic not in self.topics:
            self.topics[topic] = []
        if callback not in self.topics[topic]:
            self.topics[topic].append(callback)

    def publish(self, topic: str, message: any) -> None:
        """Publish message to topic."""
        if topic in self.topics:
            for callback in self.topics[topic]:
                callback(message)

    def unsubscribe(self, topic: str, callback: callable) -> None:
        """Unsubscribe from topic."""
        if topic in self.topics:
            if callback in self.topics[topic]:
                self.topics[topic].remove(callback)


def main() -> None:
    """Demonstrate Publish Subscribe."""
    print("=" * 70)
    print("PUBLISH SUBSCRIBE")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Publish Subscribe")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
