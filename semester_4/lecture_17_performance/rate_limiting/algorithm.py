#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rate Limiting Pattern.

Controls the rate of requests sent or received to prevent abuse,
ensure fair usage, and protect system resources.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import deque
import time

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


@dataclass
class RateLimitConfig:
    """Rate limit configuration."""
    max_requests: int = 100
    window_seconds: float = 60.0  # Time window in seconds


class RateLimiter(ABC):
    """Abstract rate limiter."""
    
    @abstractmethod
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed.
        
        Args:
            identifier: Client identifier (IP, user ID, etc.)
            
        Returns:
            True if allowed, False otherwise
        """
        pass
    
    @abstractmethod
    def get_remaining(self, identifier: str) -> int:
        """
        Get remaining requests in current window.
        
        Args:
            identifier: Client identifier
            
        Returns:
            Number of remaining requests
        """
        pass


class TokenBucketRateLimiter(RateLimiter):
    """Token bucket rate limiter."""
    
    def __init__(self, config: RateLimitConfig):
        """
        Initialize token bucket rate limiter.
        
        Args:
            config: Rate limit configuration
        """
        self.config = config
        self.buckets: Dict[str, dict] = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed using token bucket."""
        now = datetime.now()
        
        if identifier not in self.buckets:
            self.buckets[identifier] = {
                'tokens': self.config.max_requests,
                'last_refill': now
            }
        
        bucket = self.buckets[identifier]
        
        # Refill tokens
        elapsed = (now - bucket['last_refill']).total_seconds()
        tokens_to_add = int((elapsed / self.config.window_seconds) * self.config.max_requests)
        
        if tokens_to_add > 0:
            bucket['tokens'] = min(
                self.config.max_requests,
                bucket['tokens'] + tokens_to_add
            )
            bucket['last_refill'] = now
        
        # Check if token available
        if bucket['tokens'] > 0:
            bucket['tokens'] -= 1
            return True
        
        return False
    
    def get_remaining(self, identifier: str) -> int:
        """Get remaining tokens."""
        if identifier not in self.buckets:
            return self.config.max_requests
        
        bucket = self.buckets[identifier]
        now = datetime.now()
        elapsed = (now - bucket['last_refill']).total_seconds()
        tokens_to_add = int((elapsed / self.config.window_seconds) * self.config.max_requests)
        
        current_tokens = min(
            self.config.max_requests,
            bucket['tokens'] + tokens_to_add
        )
        
        return max(0, int(current_tokens))


class SlidingWindowRateLimiter(RateLimiter):
    """Sliding window rate limiter."""
    
    def __init__(self, config: RateLimitConfig):
        """
        Initialize sliding window rate limiter.
        
        Args:
            config: Rate limit configuration
        """
        self.config = config
        self.windows: Dict[str, deque] = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed using sliding window."""
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.config.window_seconds)
        
        if identifier not in self.windows:
            self.windows[identifier] = deque()
        
        window = self.windows[identifier]
        
        # Remove old requests
        while window and window[0] < cutoff:
            window.popleft()
        
        # Check limit
        if len(window) < self.config.max_requests:
            window.append(now)
            return True
        
        return False
    
    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests in window."""
        if identifier not in self.windows:
            return self.config.max_requests
        
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.config.window_seconds)
        window = self.windows[identifier]
        
        # Remove old requests
        while window and window[0] < cutoff:
            window.popleft()
        
        return max(0, self.config.max_requests - len(window))


class FixedWindowRateLimiter(RateLimiter):
    """Fixed window rate limiter."""
    
    def __init__(self, config: RateLimitConfig):
        """
        Initialize fixed window rate limiter.
        
        Args:
            config: Rate limit configuration
        """
        self.config = config
        self.windows: Dict[str, dict] = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed using fixed window."""
        now = datetime.now()
        window_start = now.replace(second=0, microsecond=0)
        
        if identifier not in self.windows:
            self.windows[identifier] = {
                'window_start': window_start,
                'count': 0
            }
        
        window = self.windows[identifier]
        
        # Reset if new window
        if window['window_start'] < window_start:
            window['window_start'] = window_start
            window['count'] = 0
        
        # Check limit
        if window['count'] < self.config.max_requests:
            window['count'] += 1
            return True
        
        return False
    
    def get_remaining(self, identifier: str) -> int:
        """Get remaining requests in current window."""
        if identifier not in self.windows:
            return self.config.max_requests
        
        window = self.windows[identifier]
        now = datetime.now()
        window_start = now.replace(second=0, microsecond=0)
        
        # Reset if new window
        if window['window_start'] < window_start:
            return self.config.max_requests
        
        return max(0, self.config.max_requests - window['count'])


def main() -> None:
    """Demonstration of Rate Limiting Pattern."""
    print("=" * 70)
    print("RATE LIMITING PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Token Bucket
    print("Example 1: Token Bucket Rate Limiter")
    print("-" * 70)
    
    config = RateLimitConfig(max_requests=5, window_seconds=10.0)
    limiter = TokenBucketRateLimiter(config)
    
    client_id = "client1"
    print(f"Rate limit: {config.max_requests} requests per {config.window_seconds}s")
    print(f"\nMaking requests as {client_id}:")
    
    for i in range(8):
        allowed = limiter.is_allowed(client_id)
        remaining = limiter.get_remaining(client_id)
        status = "ALLOWED" if allowed else "DENIED"
        print(f"  Request {i+1}: {status} (remaining: {remaining})")
        time.sleep(0.1)
    print()
    
    # Example 2: Sliding Window
    print("Example 2: Sliding Window Rate Limiter")
    print("-" * 70)
    
    config = RateLimitConfig(max_requests=3, window_seconds=5.0)
    limiter = SlidingWindowRateLimiter(config)
    
    client_id = "client2"
    print(f"Rate limit: {config.max_requests} requests per {config.window_seconds}s")
    print(f"\nMaking requests as {client_id}:")
    
    for i in range(5):
        allowed = limiter.is_allowed(client_id)
        remaining = limiter.get_remaining(client_id)
        status = "ALLOWED" if allowed else "DENIED"
        print(f"  Request {i+1}: {status} (remaining: {remaining})")
        time.sleep(0.5)
    print()
    
    # Example 3: Fixed Window
    print("Example 3: Fixed Window Rate Limiter")
    print("-" * 70)
    
    config = RateLimitConfig(max_requests=4, window_seconds=10.0)
    limiter = FixedWindowRateLimiter(config)
    
    client_id = "client3"
    print(f"Rate limit: {config.max_requests} requests per {config.window_seconds}s")
    print(f"\nMaking requests as {client_id}:")
    
    for i in range(6):
        allowed = limiter.is_allowed(client_id)
        remaining = limiter.get_remaining(client_id)
        status = "ALLOWED" if allowed else "DENIED"
        print(f"  Request {i+1}: {status} (remaining: {remaining})")
        time.sleep(0.2)
    print()
    
    # Example 4: Multiple Clients
    print("Example 4: Rate Limiting Multiple Clients")
    print("-" * 70)
    
    limiter = TokenBucketRateLimiter(RateLimitConfig(max_requests=3, window_seconds=5.0))
    
    clients = ["client_a", "client_b", "client_c"]
    print("Distributing requests across clients:")
    
    for i in range(12):
        client = clients[i % len(clients)]
        allowed = limiter.is_allowed(client)
        remaining = limiter.get_remaining(client)
        status = "✓" if allowed else "✗"
        print(f"  Request {i+1} ({client}): {status} (remaining: {remaining})")
    print()
    
    # Example 5: Performance measurement
    print("Example 5: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Rate Limiting")
    
    def rate_limiting_operations():
        limiter = TokenBucketRateLimiter(RateLimitConfig(max_requests=100, window_seconds=60.0))
        
        allowed_count = 0
        for i in range(200):
            if limiter.is_allowed(f"client{i % 10}"):
                allowed_count += 1
        
        return allowed_count
    
    result, metrics = timer.measure(rate_limiting_operations)
    print(f"Time to process 200 rate limit checks: {metrics['execution_time_ms']:.3f} ms")
    print(f"Allowed requests: {result}/200")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Controls the rate of requests sent or received to prevent")
    print("  abuse, ensure fair usage, and protect system resources.")
    print("\nKey Advantages:")
    print("  - Prevents abuse")
    print("  - Protects system resources")
    print("  - Ensures fair usage")
    print("  - DDoS protection")
    print("\nKey Disadvantages:")
    print("  - May block legitimate users")
    print("  - Configuration complexity")
    print("  - Memory overhead")
    print("  - Distributed rate limiting challenges")
    print("\nWhen to Use:")
    print("  - API rate limiting")
    print("  - DDoS protection")
    print("  - Fair resource allocation")
    print("  - Cost control")
    print("\nCommon Use Cases:")
    print("  - API gateways")
    print("  - Web applications")
    print("  - Microservices")
    print("  - CDN services")
    print("\nRate Limiting Algorithms:")
    print("  - Token Bucket: Tokens refill at constant rate")
    print("  - Sliding Window: Tracks requests in time window")
    print("  - Fixed Window: Fixed time windows")
    print("  - Leaky Bucket: Requests leak at constant rate")
    print("=" * 70)


if __name__ == "__main__":
    main()
