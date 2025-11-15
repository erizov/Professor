#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Singleton Design Pattern.

Ensures a class has only one instance and provides global access to it.
"""

import sys
from pathlib import Path
from threading import Lock
from typing import Optional

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


class Singleton:
    """
    Thread-safe Singleton implementation using metaclass.
    
    This is the most Pythonic way to implement Singleton.
    """
    _instances = {}
    _lock: Lock = Lock()
    
    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                # Double-checked locking
                if cls not in cls._instances:
                    instance = super().__new__(cls)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigurationManager(Singleton):
    """Example: Configuration Manager as Singleton."""
    
    def __init__(self):
        # Only initialize once
        if not hasattr(self, 'initialized'):
            self.config = {}
            self.initialized = True
    
    def set(self, key: str, value: any) -> None:
        """Set configuration value."""
        self.config[key] = value
    
    def get(self, key: str, default: any = None) -> any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def __repr__(self) -> str:
        return f"ConfigurationManager(config={self.config})"


class DatabaseConnection(Singleton):
    """Example: Database Connection as Singleton."""
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection_string = None
            self.connected = False
            self.initialized = True
    
    def connect(self, connection_string: str) -> None:
        """Establish database connection."""
        if not self.connected:
            self.connection_string = connection_string
            self.connected = True
            print(f"Connected to database: {connection_string}")
    
    def disconnect(self) -> None:
        """Close database connection."""
        if self.connected:
            self.connected = False
            print("Disconnected from database")
    
    def execute_query(self, query: str) -> str:
        """Execute database query."""
        if not self.connected:
            return "Error: Not connected to database"
        return f"Executed query: {query}"


# Alternative implementation using decorator
def singleton(cls):
    """Singleton decorator for simple cases."""
    instances = {}
    lock = Lock()
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Logger:
    """Example: Logger as Singleton using decorator."""
    
    def __init__(self):
        self.log_level = "INFO"
        self.logs = []
    
    def log(self, message: str, level: str = "INFO") -> None:
        """Log a message."""
        log_entry = f"[{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def get_logs(self) -> list:
        """Get all logs."""
        return self.logs.copy()


# Metaclass implementation (advanced)
class SingletonMeta(type):
    """
    Metaclass that creates a Singleton instance.
    
    This is the most flexible implementation.
    """
    _instances = {}
    _lock: Lock = Lock()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class CacheManager(metaclass=SingletonMeta):
    """Example: Cache Manager using metaclass."""
    
    def __init__(self):
        self.cache = {}
    
    def set(self, key: str, value: any) -> None:
        """Set cache value."""
        self.cache[key] = value
    
    def get(self, key: str) -> Optional[any]:
        """Get cache value."""
        return self.cache.get(key)
    
    def clear(self) -> None:
        """Clear all cache."""
        self.cache.clear()


def main() -> None:
    """Demonstration of Singleton Pattern."""
    print("=" * 70)
    print("SINGLETON DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic Singleton
    print("Example 1: Configuration Manager Singleton")
    print("-" * 70)
    
    config1 = ConfigurationManager()
    config1.set("database_url", "localhost:5432")
    config1.set("debug", True)
    
    config2 = ConfigurationManager()
    print(f"config1 is config2: {config1 is config2}")
    print(f"config1 ID: {id(config1)}")
    print(f"config2 ID: {id(config2)}")
    print(f"config2.get('database_url'): {config2.get('database_url')}")
    print(f"config2.get('debug'): {config2.get('debug')}")
    print()
    
    # Example 2: Database Connection Singleton
    print("Example 2: Database Connection Singleton")
    print("-" * 70)
    
    db1 = DatabaseConnection()
    db1.connect("postgresql://localhost:5432/mydb")
    
    db2 = DatabaseConnection()
    print(f"db1 is db2: {db1 is db2}")
    print(db2.execute_query("SELECT * FROM users"))
    
    db1.disconnect()
    print()
    
    # Example 3: Logger with Decorator
    print("Example 3: Logger Singleton (Decorator Pattern)")
    print("-" * 70)
    
    logger1 = Logger()
    logger1.log("Application started")
    logger1.log("User logged in", "INFO")
    
    logger2 = Logger()
    logger2.log("Processing request", "DEBUG")
    
    print(f"\nlogger1 is logger2: {logger1 is logger2}")
    print(f"Total logs: {len(logger1.get_logs())}")
    print()
    
    # Example 4: Cache Manager with Metaclass
    print("Example 4: Cache Manager (Metaclass Implementation)")
    print("-" * 70)
    
    cache1 = CacheManager()
    cache1.set("user_123", {"name": "John", "age": 30})
    cache1.set("user_456", {"name": "Jane", "age": 25})
    
    cache2 = CacheManager()
    print(f"cache1 is cache2: {cache1 is cache2}")
    print(f"cache2.get('user_123'): {cache2.get('user_123')}")
    print(f"Cache contents: {cache2.cache}")
    print()
    
    # Example 5: Thread Safety Demonstration
    print("Example 5: Thread Safety")
    print("-" * 70)
    
    import threading
    
    instances = []
    
    def create_instance():
        instance = ConfigurationManager()
        instances.append(instance)
    
    threads = [threading.Thread(target=create_instance) 
               for _ in range(10)]
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # Check all instances are the same
    all_same = all(inst is instances[0] for inst in instances)
    print(f"Created {len(instances)} instances")
    print(f"All instances are the same: {all_same}")
    print(f"Unique IDs: {len(set(id(inst) for inst in instances))}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Ensure a class has only one instance and provide")
    print("  global access to it.")
    print("\nKey Advantages:")
    print("  - Controlled access to sole instance")
    print("  - Reduced namespace pollution")
    print("  - Lazy initialization possible")
    print("  - Can be subclassed")
    print("\nKey Disadvantages:")
    print("  - Violates Single Responsibility Principle")
    print("  - Can make unit testing difficult")
    print("  - Hides dependencies")
    print("  - Requires special care in multithreaded environments")
    print("\nWhen to Use:")
    print("  - Logging")
    print("  - Configuration management")
    print("  - Connection pools")
    print("  - Cache managers")
    print("  - Thread pools")
    print("\nWhen Not to Use:")
    print("  - When multiple instances are needed")
    print("  - For objects with no shared state")
    print("  - When it complicates testing")
    print("\nImplementation Notes:")
    print("  - Python: Use __new__, decorator, or metaclass")
    print("  - Thread safety: Use locks for thread-safe access")
    print("  - Lazy vs Eager: Choose based on initialization cost")
    print("=" * 70)


if __name__ == "__main__":
    main()
