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
    print("=" * 70)
    print("HASH TABLE DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic operations
    print("Example 1: Basic Operations")
    print("-" * 70)
    
    ht = HashTable()
    
    # Insert operations
    ht.put("apple", 5)
    ht.put("banana", 3)
    ht.put("cherry", 8)
    ht.put("date", 2)
    
    print(f"Hash table: {ht}")
    print(f"Size: {len(ht)}")
    print(f"Get 'apple': {ht.get('apple')}")
    print(f"Get 'banana': {ht.get('banana')}")
    print(f"Contains 'cherry': {ht.contains('cherry')}")
    print(f"Contains 'grape': {ht.contains('grape')}")
    print()
    
    # Example 2: Update and remove
    print("Example 2: Update and Remove")
    print("-" * 70)
    
    ht.put("apple", 10)  # Update
    print(f"After updating 'apple' to 10: {ht}")
    
    ht.remove("banana")
    print(f"After removing 'banana': {ht}")
    print(f"Size: {len(ht)}")
    print()
    
    # Example 3: Integer keys
    print("Example 3: Integer Keys")
    print("-" * 70)
    
    ht2 = HashTable()
    ht2.put(1, "one")
    ht2.put(2, "two")
    ht2.put(3, "three")
    ht2.put(100, "hundred")
    
    print(f"Hash table with integers: {ht2}")
    print(f"Get key 100: {ht2.get(100)}")
    print()
    
    # Example 4: Collision handling
    print("Example 4: Collision Handling")
    print("-" * 70)
    
    ht3 = HashTable(initial_capacity=5)  # Small capacity to force collisions
    test_keys = ["a", "b", "c", "d", "e", "f", "g"]
    
    for i, key in enumerate(test_keys):
        ht3.put(key, i * 10)
    
    print(f"Hash table with collisions (capacity={ht3.capacity}):")
    print(f"  Size: {len(ht3)}")
    print(f"  All keys: {ht3.keys()}")
    print(f"  All values: {ht3.values()}")
    
    # Verify all keys are retrievable
    print("\nVerifying all keys are retrievable:")
    for key in test_keys:
        value = ht3.get(key)
        print(f"  {key} -> {value}")
    print()
    
    # Example 5: Performance measurement
    print("Example 5: Performance Measurement")
    print("-" * 70)
    
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
        print(f"Operations on {n} elements:")
        print(f"  Time: {metrics['execution_time_ms']:.3f} ms")
        print(f"  Memory: {metrics['memory_peak_kb']:.2f} KB")
    
    print()
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Average Case:")
    print("    Insert: O(1)")
    print("    Lookup: O(1)")
    print("    Delete: O(1)")
    print("  Worst Case (all collisions):")
    print("    All operations: O(n)")
    print("  Space: O(n)")
    print("\nKey Advantages:")
    print("  - Fast average-case operations")
    print("  - Flexible key types")
    print("  - Dynamic resizing")
    print("  - Simple implementation")
    print("\nKey Disadvantages:")
    print("  - Worst-case O(n) with many collisions")
    print("  - Memory overhead (buckets)")
    print("  - Not ordered")
    print("  - Hash function quality matters")
    print("\nWhen to Use:")
    print("  - Fast key-value lookups")
    print("  - Dictionary/map data structure")
    print("  - Caching")
    print("  - Counting frequencies")
    print("  - Removing duplicates")
    print("\nWhen NOT to Use:")
    print("  - Need ordered data (use TreeMap)")
    print("  - Need range queries")
    print("  - Memory is very constrained")
    print("  - Keys have poor hash distribution")
    print("\nCommon Use Cases:")
    print("  - Database indexing")
    print("  - Caching (LRU cache)")
    print("  - Symbol tables")
    print("  - Counting word frequencies")
    print("  - Implementing sets")
    print("=" * 70)


if __name__ == "__main__":
    main()
