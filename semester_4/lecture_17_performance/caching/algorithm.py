#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Caching Pattern.

Stores frequently accessed data in fast storage to improve performance.
Reduces load on primary data source and speeds up response times.
"""

import sys
from pathlib import Path
from typing import Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import OrderedDict
import time

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


@dataclass
class CacheEntry:
    """Cache entry with expiration."""
    key: str
    value: Any
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    def is_expired(self) -> bool:
        """Check if entry is expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at


class LRUCache:
    """Least Recently Used (LRU) cache."""
    
    def __init__(self, capacity: int = 100, ttl: Optional[float] = None):
        """
        Initialize LRU cache.
        
        Args:
            capacity: Maximum number of entries
            ttl: Time to live in seconds (None for no expiration)
        """
        self.capacity = capacity
        self.ttl = ttl
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        
        # Check expiration
        if entry.is_expired():
            del self.cache[key]
            return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return entry.value
    
    def put(self, key: str, value: Any) -> None:
        """
        Put value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        now = datetime.now()
        expires_at = None
        
        if self.ttl:
            expires_at = now + timedelta(seconds=self.ttl)
        
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=now,
            expires_at=expires_at
        )
        
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                # Remove least recently used
                self.cache.popitem(last=False)
        
        self.cache[key] = entry
    
    def invalidate(self, key: str) -> None:
        """Invalidate cache entry."""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
    
    def size(self) -> int:
        """Get cache size."""
        return len(self.cache)


class CacheDecorator:
    """Cache decorator for functions."""
    
    def __init__(self, cache: LRUCache):
        self.cache = cache
    
    def __call__(self, func: Callable) -> Callable:
        """Decorate function with caching."""
        def wrapper(*args, **kwargs):
            # Create cache key from arguments
            key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Try to get from cache
            cached = self.cache.get(key)
            if cached is not None:
                return cached
            
            # Compute and cache
            result = func(*args, **kwargs)
            self.cache.put(key, result)
            return result
        
        return wrapper


# Example: Expensive computation
def expensive_computation(n: int) -> int:
    """Simulate expensive computation."""
    time.sleep(0.1)  # Simulate computation time
    return n * n


def expensive_database_query(user_id: int) -> dict:
    """Simulate database query."""
    time.sleep(0.05)  # Simulate database latency
    return {
        "user_id": user_id,
        "name": f"User{user_id}",
        "email": f"user{user_id}@example.com"
    }


def main() -> None:
    """Demonstration of Caching Pattern."""
    logger.info("=" * 70)
    logger.info("CACHING PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic LRU Cache
    logger.info("Example 1: Basic LRU Cache")
    logger.info("-" * 70)
    
    cache = LRUCache(capacity=3)
    
    logger.info("Adding items to cache:")
    for i in range(5):
        cache.put(f"key{i}", f"value{i}")
        logger.info(f"  Added key{i}, Cache size: {cache.size()}")
    logger.info()
    
    logger.info("Accessing items:")
    for i in range(5):
        value = cache.get(f"key{i}")
        if value:
            logger.info(f"  key{i}: {value} (HIT)")
        else:
            logger.info(f"  key{i}: None (MISS)")
    logger.info()
    
    # Example 2: Cache with TTL
    logger.info("Example 2: Cache with Time-to-Live (TTL)")
    logger.info("-" * 70)
    
    cache = LRUCache(capacity=10, ttl=2.0)  # 2 second TTL
    
    cache.put("temp", "temporary_value")
    logger.info("Added entry with 2s TTL")
    logger.info(f"  Immediate get: {cache.get('temp')}")
    
    time.sleep(2.1)
    logger.info(f"  After 2.1s: {cache.get('temp')} (expired)")
    logger.info()
    
    # Example 3: Function Caching
    logger.info("Example 3: Function Caching Decorator")
    logger.info("-" * 70)
    
    cache = LRUCache(capacity=100)
    cached_func = CacheDecorator(cache)(expensive_computation)
    
    logger.info("First call (cache miss):")
    start = time.time()
    result1 = cached_func(5)
    time1 = time.time() - start
    logger.info(f"  Result: {result1}, Time: {time1:.3f}s")
    
    logger.info("Second call (cache hit):")
    start = time.time()
    result2 = cached_func(5)
    time2 = time.time() - start
    logger.info(f"  Result: {result2}, Time: {time2:.3f}s")
    logger.info(f"  Speedup: {time1/time2:.1f}x")
    logger.info()
    
    # Example 4: Database Query Caching
    logger.info("Example 4: Database Query Caching")
    logger.info("-" * 70)
    
    query_cache = LRUCache(capacity=50, ttl=60.0)  # 1 minute TTL
    
    def get_user_cached(user_id: int) -> dict:
        """Get user with caching."""
        cache_key = f"user:{user_id}"
        cached = query_cache.get(cache_key)
        if cached:
            return cached
        
        result = expensive_database_query(user_id)
        query_cache.put(cache_key, result)
        return result
    
    logger.info("Querying users:")
    for user_id in [1, 2, 1, 3, 1]:  # User 1 queried multiple times
        start = time.time()
        user = get_user_cached(user_id)
        elapsed = time.time() - start
        logger.info(f"  User {user_id}: {user['name']} ({elapsed:.3f}s)")
    logger.info()
    
    # Example 5: Performance measurement
    logger.info("Example 5: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Caching")
    
    def cache_operations():
        cache = LRUCache(capacity=1000)
        
        # Fill cache
        for i in range(1000):
            cache.put(f"key{i}", f"value{i}")
        
        # Access (should all be hits)
        hits = 0
        for i in range(1000):
            if cache.get(f"key{i}"):
                hits += 1
        
        return hits
    
    result, metrics = timer.measure(cache_operations)
    logger.info(f"Time to perform 1000 cache operations: "
          f"{metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Cache hits: {result}/1000")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Stores frequently accessed data in fast storage to improve")
    logger.info("  performance and reduce load on primary data source.")
    logger.info("\nKey Advantages:")
    logger.info("  - Faster response times")
    logger.info("  - Reduced load on data source")
    logger.info("  - Better scalability")
    logger.info("  - Cost reduction")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Memory usage")
    logger.info("  - Stale data risk")
    logger.info("  - Cache invalidation complexity")
    logger.info("  - Additional complexity")
    logger.info("\nWhen to Use:")
    logger.info("  - Expensive computations")
    logger.info("  - Database queries")
    logger.info("  - API responses")
    logger.info("  - Frequently accessed data")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Redis")
    logger.info("  - Memcached")
    logger.info("  - In-memory caches")
    logger.info("  - CDN caching")
    logger.info("  - Browser caching")
    logger.info("\nCache Strategies:")
    logger.info("  - LRU (Least Recently Used)")
    logger.info("  - LFU (Least Frequently Used)")
    logger.info("  - FIFO (First In First Out)")
    logger.info("  - TTL (Time To Live)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()