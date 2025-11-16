#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Retry Pattern.

Automatically retries failed operations with configurable strategies
like exponential backoff, maximum attempts, and jitter.
"""

import sys
from pathlib import Path
import time
import random
from typing import Callable, Any, Optional, Type
from dataclasses import dataclass
from enum import Enum

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class RetryStrategy(Enum):
    """Retry strategies."""
    FIXED = "fixed"           # Fixed delay
    EXPONENTIAL = "exponential"  # Exponential backoff
    LINEAR = "linear"         # Linear backoff


@dataclass
class RetryConfig:
    """Retry configuration."""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL
    jitter: bool = True
    retryable_exceptions: tuple = (Exception,)


class RetryHandler:
    """Retry handler with configurable strategies."""
    
    def __init__(self, config: RetryConfig = None):
        """
        Initialize retry handler.
        
        Args:
            config: Retry configuration
        """
        self.config = config or RetryConfig()
    
    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with retry logic.
        
        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
            
        Raises:
            Exception: Last exception if all retries fail
        """
        last_exception = None
        
        for attempt in range(1, self.config.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                # Check if exception is retryable
                if not isinstance(e, self.config.retryable_exceptions):
                    raise
                
                # Don't wait after last attempt
                if attempt < self.config.max_attempts:
                    delay = self._calculate_delay(attempt)
                    logger.info(f"Attempt {attempt} failed: {e}. Retrying in {delay:.2f}s...")
                    time.sleep(delay)
                else:
                    logger.info(f"Attempt {attempt} failed: {e}. Max attempts reached.")
        
        raise last_exception
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt."""
        if self.config.strategy == RetryStrategy.FIXED:
            delay = self.config.initial_delay
        elif self.config.strategy == RetryStrategy.LINEAR:
            delay = self.config.initial_delay * attempt
        else:  # EXPONENTIAL
            delay = self.config.initial_delay * (2 ** (attempt - 1))
        
        # Apply jitter
        if self.config.jitter:
            jitter_amount = delay * 0.1  # 10% jitter
            delay += random.uniform(-jitter_amount, jitter_amount)
        
        # Cap at max delay
        return min(delay, self.config.max_delay)


# Decorator version
def retry(config: RetryConfig = None):
    """
    Retry decorator.
    
    Args:
        config: Retry configuration
    """
    def decorator(func: Callable) -> Callable:
        handler = RetryHandler(config)
        
        def wrapper(*args, **kwargs):
            return handler.execute(func, *args, **kwargs)
        
        return wrapper
    return decorator


# Example: Unreliable service
class UnreliableService:
    """Service that may fail."""
    
    def __init__(self, success_rate: float = 0.3):
        """
        Initialize service.
        
        Args:
            success_rate: Probability of success (0.0 to 1.0)
        """
        self.success_rate = success_rate
        self.call_count = 0
    
    def call(self) -> str:
        """Call service."""
        self.call_count += 1
        
        if random.random() < self.success_rate:
            return f"Success on attempt {self.call_count}"
        else:
            raise Exception(f"Service failed on attempt {self.call_count}")


def main() -> None:
    """Demonstration of Retry Pattern."""
    logger.info("=" * 70)
    logger.info("RETRY PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Basic Retry
    logger.info("Example 1: Basic Retry with Exponential Backoff")
    logger.info("-" * 70)
    
    config = RetryConfig(
        max_attempts=5,
        initial_delay=0.5,
        strategy=RetryStrategy.EXPONENTIAL,
        jitter=True
    )
    handler = RetryHandler(config)
    service = UnreliableService(success_rate=0.2)  # 20% success rate
    
    try:
        result = handler.execute(service.call)
        logger.info(f"Final result: {result}")
    except Exception as e:
        logger.info(f"All retries failed: {e}")
    logger.info()
    
    # Example 2: Fixed Delay Retry
    logger.info("Example 2: Fixed Delay Retry")
    logger.info("-" * 70)
    
    config = RetryConfig(
        max_attempts=3,
        initial_delay=1.0,
        strategy=RetryStrategy.FIXED,
        jitter=False
    )
    handler = RetryHandler(config)
    service = UnreliableService(success_rate=0.4)
    
    try:
        result = handler.execute(service.call)
        logger.info(f"Final result: {result}")
    except Exception as e:
        logger.info(f"All retries failed: {e}")
    logger.info()
    
    # Example 3: Retry Decorator
    logger.info("Example 3: Retry Decorator")
    logger.info("-" * 70)
    
    @retry(config=RetryConfig(max_attempts=3, initial_delay=0.3))
    def unreliable_function():
        if random.random() < 0.3:
            return "Success!"
        raise Exception("Temporary failure")
    
    try:
        result = unreliable_function()
        logger.info(f"Result: {result}")
    except Exception as e:
        logger.info(f"Failed: {e}")
    logger.info()
    
    # Example 4: Performance measurement
    logger.info("Example 4: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Retry Pattern")
    
    def retry_operations():
        handler = RetryHandler(RetryConfig(max_attempts=3, initial_delay=0.01))
        service = UnreliableService(success_rate=0.5)
        
        success_count = 0
        for _ in range(10):
            try:
                handler.execute(service.call)
                success_count += 1
            except:
                pass
        
        return success_count
    
    result, metrics = timer.measure(retry_operations)
    logger.info(f"Time to process 10 operations with retries: "
          f"{metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Successful operations: {result}/10")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Automatically retries failed operations with configurable")
    logger.info("  strategies like exponential backoff, maximum attempts, and jitter.")
    logger.info("\nKey Advantages:")
    logger.info("  - Handles transient failures")
    logger.info("  - Configurable retry strategies")
    logger.info("  - Exponential backoff reduces load")
    logger.info("  - Jitter prevents thundering herd")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Can delay failure detection")
    logger.info("  - May increase load on failing service")
    logger.info("  - Configuration complexity")
    logger.info("\nWhen to Use:")
    logger.info("  - Network operations")
    logger.info("  - External service calls")
    logger.info("  - Transient failures expected")
    logger.info("  - Idempotent operations")
    logger.info("\nCommon Use Cases:")
    logger.info("  - HTTP requests")
    logger.info("  - Database connections")
    logger.info("  - API calls")
    logger.info("  - File operations")
    logger.info("\nRetry Strategies:")
    logger.info("  - Fixed: Constant delay between retries")
    logger.info("  - Linear: Delay increases linearly")
    logger.info("  - Exponential: Delay doubles each retry")
    logger.info("  - Jitter: Random variation to prevent synchronization")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()