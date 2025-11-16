#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hash Table implementation with chaining for collision resolution.

Efficient key-value storage with average O(1) operations.
"""

import sys
from pathlib import Path
from typing import Optional, List, Tuple, Any

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class HashTable:
    """
    Hash Table with chaining collision resolution.
    
    Uses a list of lists (buckets) to handle collisions.
    """
    
    def __init__(self, initial_capacity: int = 16, load_factor: float = 0.75):
        """
        Initialize hash table.
        
        Args:
            initial_capacity: Initial number of buckets
            load_factor: Threshold for resizing (0.0 to 1.0)
        """
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets: List[List[Tuple[Any, Any]]] = [[] for _ in range(self.capacity)]
    
    def _hash(self, key: Any) -> int:
        """
        Hash function for key.
        
        Args:
            key: Key to hash
            
        Returns:
            Hash index
        """
        if isinstance(key, int):
            return key % self.capacity
        elif isinstance(key, str):
            hash_value = 0
            for char in key:
                hash_value = (hash_value * 31 + ord(char)) % self.capacity
            return hash_value
        else:
            return hash(key) % self.capacity
    
    def _resize(self) -> None:
        """Resize hash table when load factor exceeded."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]
        
        # Rehash all entries
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def put(self, key: Any, value: Any) -> None:
        """
        Insert or update key-value pair.
        
        Args:
            key: Key
            value: Value
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing
                return
        
        # Add new entry
        bucket.append((key, value))
        self.size += 1
        
        # Check if resize needed
        if self.size > self.capacity * self.load_factor:
            self._resize()
    
    def get(self, key: Any) -> Optional[Any]:
        """
        Get value by key.
        
        Args:
            key: Key to look up
            
        Returns:
            Value if found, None otherwise
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return None
    
    def remove(self, key: Any) -> bool:
        """
        Remove key-value pair.
        
        Args:
            key: Key to remove
            
        Returns:
            True if removed, False if not found
        """
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        
        return False
    
    def contains(self, key: Any) -> bool:
        """
        Check if key exists.
        
        Args:
            key: Key to check
            
        Returns:
            True if key exists
        """
        return self.get(key) is not None
    
    def keys(self) -> List[Any]:
        """Get all keys."""
        result = []
        for bucket in self.buckets:
            for key, _ in bucket:
                result.append(key)
        return result
    
    def values(self) -> List[Any]:
        """Get all values."""
        result = []
        for bucket in self.buckets:
            for _, value in bucket:
                result.append(value)
        return result
    
    def items(self) -> List[Tuple[Any, Any]]:
        """Get all key-value pairs."""
        result = []
        for bucket in self.buckets:
            result.extend(bucket)
        return result
    
    def __len__(self) -> int:
        """Get number of entries."""
        return self.size
    
    def __str__(self) -> str:
        """String representation."""
        items = self.items()
        return "{" + ", ".join(f"{k}: {v}" for k, v in items) + "}"


def main() -> None:
    """Demonstration of Hash Table."""
    logger.info("=" * 70)
    logger.info("HASH TABLE DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic operations
    logger.info("Example 1: Basic Operations")
    logger.info("-" * 70)
    
    ht = HashTable()
    
    # Insert operations
    ht.put("apple", 5)
    ht.put("banana", 3)
    ht.put("cherry", 8)
    ht.put("date", 2)
    
    logger.info(f"Hash table: {ht}")
    logger.info(f"Size: {len(ht)}")
    logger.info(f"Get 'apple': {ht.get('apple')}")
    logger.info(f"Get 'banana': {ht.get('banana')}")
    logger.info(f"Contains 'cherry': {ht.contains('cherry')}")
    logger.info(f"Contains 'grape': {ht.contains('grape')}")
    logger.info()
    
    # Example 2: Update and remove
    logger.info("Example 2: Update and Remove")
    logger.info("-" * 70)
    
    ht.put("apple", 10)  # Update
    logger.info(f"After updating 'apple' to 10: {ht}")
    
    ht.remove("banana")
    logger.info(f"After removing 'banana': {ht}")
    logger.info(f"Size: {len(ht)}")
    logger.info()
    
    # Example 3: Integer keys
    logger.info("Example 3: Integer Keys")
    logger.info("-" * 70)
    
    ht2 = HashTable()
    ht2.put(1, "one")
    ht2.put(2, "two")
    ht2.put(3, "three")
    ht2.put(100, "hundred")
    
    logger.info(f"Hash table with integers: {ht2}")
    logger.info(f"Get key 100: {ht2.get(100)}")
    logger.info()
    
    # Example 4: Collision handling
    logger.info("Example 4: Collision Handling")
    logger.info("-" * 70)
    
    ht3 = HashTable(initial_capacity=5)  # Small capacity to force collisions
    test_keys = ["a", "b", "c", "d", "e", "f", "g"]
    
    for i, key in enumerate(test_keys):
        ht3.put(key, i * 10)
    
    logger.info(f"Hash table with collisions (capacity={ht3.capacity}):")
    logger.info(f"  Size: {len(ht3)}")
    logger.info(f"  All keys: {ht3.keys()}")
    logger.info(f"  All values: {ht3.values()}")
    
    # Verify all keys are retrievable
    logger.info("\nVerifying all keys are retrievable:")
    for key in test_keys:
        value = ht3.get(key)
        logger.info(f"  {key} -> {value}")
    logger.info()
    
    # Example 5: Performance measurement
    logger.info("Example 5: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Hash Table")
    
    def test_operations(n):
        ht = HashTable()
        # Insert
        for i in range(n):
            ht.put(f"key_{i}", i)
        # Lookup
        for i in range(n):
            _ = ht.get(f"key_{i}")
        # Remove
        for i in range(n):
            ht.remove(f"key_{i}")
        return ht
    
    for n in [100, 1000, 10000]:
        _, metrics = timer.measure(test_operations, n)
        logger.info(f"Operations on {n} elements:")
        logger.info(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        logger.info(f"  Memory: {metrics['memory_peak_kb']:.2f} KB")
    
    logger.info()
    logger.info("=" * 70)
    logger.info("\nComplexity Summary:")
    logger.info("  Average Case:")
    logger.info("    Insert: O(1)")
    logger.info("    Lookup: O(1)")
    logger.info("    Delete: O(1)")
    logger.info("  Worst Case (all collisions):")
    logger.info("    All operations: O(n)")
    logger.info("  Space: O(n)")
    logger.info("\nKey Advantages:")
    logger.info("  - Fast average-case operations")
    logger.info("  - Flexible key types")
    logger.info("  - Dynamic resizing")
    logger.info("  - Simple implementation")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Worst-case O(n) with many collisions")
    logger.info("  - Memory overhead (buckets)")
    logger.info("  - Not ordered")
    logger.info("  - Hash function quality matters")
    logger.info("\nWhen to Use:")
    logger.info("  - Fast key-value lookups")
    logger.info("  - Dictionary/map data structure")
    logger.info("  - Caching")
    logger.info("  - Counting frequencies")
    logger.info("  - Removing duplicates")
    logger.info("\nWhen NOT to Use:")
    logger.info("  - Need ordered data (use TreeMap)")
    logger.info("  - Need range queries")
    logger.info("  - Memory is very constrained")
    logger.info("  - Keys have poor hash distribution")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Database indexing")
    logger.info("  - Caching (LRU cache)")
    logger.info("  - Symbol tables")
    logger.info("  - Counting word frequencies")
    logger.info("  - Implementing sets")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()