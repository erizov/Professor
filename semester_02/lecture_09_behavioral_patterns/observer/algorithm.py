#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Observer implementation.

This file contains the implementation of the Observer algorithm.
"""

from typing import List, Optional, Dict, Set


class Observer:
    """Observer interface."""
    def update(self, message: str) -> None:
        pass

class Subject:
    """Subject class that notifies observers."""
    def __init__(self):
        self._observers: List[Observer] = []
        self._state = None
    
    def attach(self, observer: Observer) -> None:
        """Attach observer."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Detach observer."""
        self._observers.remove(observer)
    
    def notify(self, message: str) -> None:
        """Notify all observers."""
        for observer in self._observers:
            observer.update(message)
    
    def set_state(self, state: any) -> None:
        """Set state and notify observers."""
        self._state = state
        self.notify(f"State changed to: {state}")

class ConcreteObserver(Observer):
    """Concrete observer implementation."""
    def __init__(self, name: str):
        self.name = name
    
    def update(self, message: str) -> None:
        print(f"{self.name} received: {message}")


def main() -> None:
    """Demonstrate Observer."""
    print("=" * 70)
    print("OBSERVER")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Observer")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
