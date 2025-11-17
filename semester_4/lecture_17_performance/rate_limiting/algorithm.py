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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
        
    """
    Rate Limiting implementation.
    
    Args:
        *args: Variable arguments
        **kwargs: Keyword arguments
        
    Returns:
        Algorithm result
    """
    # Implementation for rate_limiting
    logger.info(f"Executing rate_limiting")
    return None


def main() -> None:
    """Demonstration of Rate Limiting Pattern."""
    logger.info("=" * 70)
    logger.info("RATE LIMITING PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Token Bucket
    logger.info("Example 1: Token Bucket Rate Limiter")
    logger.info("-" * 70)
    
    config = RateLimitConfig(max_requests=5, window_seconds=10.0)
    limiter = TokenBucketRateLimiter(config)
    
    client_id = "client1"
    logger.info(f"Rate limit: {config.max_requests} requests per {config.window_seconds}s")
    logger.info(f"\nMaking requests as {client_id}:")
    
    for i in range(8):
        allowed = limiter.is_allowed(client_id)
        remaining = limiter.get_remaining(client_id)
        status = "ALLOWED" if allowed else "DENIED"
        logger.info(f"  Request {i+1}: {status} (remaining: {remaining})")
        time.sleep(0.1)
    logger.info()
    
    # Example 2: Sliding Window
    logger.info("Example 2: Sliding Window Rate Limiter")
    logger.info("-" * 70)
    
    config = RateLimitConfig(max_requests=3, window_seconds=5.0)
    limiter = SlidingWindowRateLimiter(config)
    
    client_id = "client2"
    logger.info(f"Rate limit: {config.max_requests} requests per {config.window_seconds}s")
    logger.info(f"\nMaking requests as {client_id}:")
    
    for i in range(5):
        allowed = limiter.is_allowed(client_id)
        remaining = limiter.get_remaining(client_id)
        status = "ALLOWED" if allowed else "DENIED"
        logger.info(f"  Request {i+1}: {status} (remaining: {remaining})")
        time.sleep(0.5)
    logger.info()
    
    # Example 3: Fixed Window
    logger.info("Example 3: Fixed Window Rate Limiter")
    logger.info("-" * 70)
    
    config = RateLimitConfig(max_requests=4, window_seconds=10.0)
    limiter = FixedWindowRateLimiter(config)
    
    client_id = "client3"
    logger.info(f"Rate limit: {config.max_requests} requests per {config.window_seconds}s")
    logger.info(f"\nMaking requests as {client_id}:")
    
    for i in range(6):
        allowed = limiter.is_allowed(client_id)
        remaining = limiter.get_remaining(client_id)
        status = "ALLOWED" if allowed else "DENIED"
        logger.info(f"  Request {i+1}: {status} (remaining: {remaining})")
        time.sleep(0.2)
    logger.info()
    
    # Example 4: Multiple Clients
    logger.info("Example 4: Rate Limiting Multiple Clients")
    logger.info("-" * 70)
    
    limiter = TokenBucketRateLimiter(RateLimitConfig(max_requests=3, window_seconds=5.0))
    
    clients = ["client_a", "client_b", "client_c"]
    logger.info("Distributing requests across clients:")
    
    for i in range(12):
        client = clients[i % len(clients)]
        allowed = limiter.is_allowed(client)
        remaining = limiter.get_remaining(client)
        status = "✓" if allowed else "✗"
        logger.info(f"  Request {i+1} ({client}): {status} (remaining: {remaining})")
    logger.info()
    
    # Example 5: Performance measurement
    logger.info("Example 5: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Rate Limiting")
    
    def rate_limiting_operations():
        limiter = TokenBucketRateLimiter(RateLimitConfig(max_requests=100, window_seconds=60.0))
        
        allowed_count = 0
        for i in range(200):
            if limiter.is_allowed(f"client{i % 10}"):
                allowed_count += 1
        
        return allowed_count
    
    result, metrics = timer.measure(rate_limiting_operations)
    logger.info(f"Time to process 200 rate limit checks: {metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Allowed requests: {result}/200")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Controls the rate of requests sent or received to prevent")
    logger.info("  abuse, ensure fair usage, and protect system resources.")
    logger.info("\nKey Advantages:")
    logger.info("  - Prevents abuse")
    logger.info("  - Protects system resources")
    logger.info("  - Ensures fair usage")
    logger.info("  - DDoS protection")
    logger.info("\nKey Disadvantages:")
    logger.info("  - May block legitimate users")
    logger.info("  - Configuration complexity")
    logger.info("  - Memory overhead")
    logger.info("  - Distributed rate limiting challenges")
    logger.info("\nWhen to Use:")
    logger.info("  - API rate limiting")
    logger.info("  - DDoS protection")
    logger.info("  - Fair resource allocation")
    logger.info("  - Cost control")
    logger.info("\nCommon Use Cases:")
    logger.info("  - API gateways")
    logger.info("  - Web applications")
    logger.info("  - Microservices")
    logger.info("  - CDN services")
    logger.info("\nRate Limiting Algorithms:")
    logger.info("  - Token Bucket: Tokens refill at constant rate")
    logger.info("  - Sliding Window: Tracks requests in time window")
    logger.info("  - Fixed Window: Fixed time windows")
    logger.info("  - Leaky Bucket: Requests leak at constant rate")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()