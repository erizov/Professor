#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Circuit Breaker Pattern.

Prevents cascading failures by stopping requests to a failing service
and allowing it time to recover. Provides fallback mechanisms.
"""

import sys
from pathlib import Path
from enum import Enum
from typing import Callable, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import time

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration."""
    failure_threshold: int = 5  # Open circuit after N failures
    success_threshold: int = 2  # Close circuit after N successes
    timeout: float = 60.0  # Time before trying half-open (seconds)
    timeout_duration: float = 30.0  # Time to wait in open state


class CircuitBreaker:
    """Circuit breaker implementation."""
    
    def __init__(self, config: CircuitBreakerConfig = None):
        """
        Initialize circuit breaker.
        
        Args:
            config: Circuit breaker configuration
        """
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.last_state_change: datetime = datetime.now()
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function through circuit breaker.
        
        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerOpenError: If circuit is open
            Exception: If function call fails
        """
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
                self.last_state_change = datetime.now()
            else:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if should attempt reset to half-open."""
        if self.last_failure_time is None:
            return True
        
        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.config.timeout_duration
    
    def _on_success(self) -> None:
        """Handle successful call."""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                self.last_state_change = datetime.now()
    
    def _on_failure(self) -> None:
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.last_state_change = datetime.now()
        elif self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            self.last_state_change = datetime.now()
    
    def get_state(self) -> CircuitState:
        """Get current state."""
        return self.state
    
    def reset(self) -> None:
        """Manually reset circuit breaker."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.last_state_change = datetime.now()


class CircuitBreakerOpenError(Exception):
    """Exception raised when circuit breaker is open."""
    pass


# Example: Service with Circuit Breaker
class ExternalService:
    """Simulated external service."""
    
    def __init__(self, failure_rate: float = 0.0):
        """
        Initialize service.
        
        Args:
            failure_rate: Probability of failure (0.0 to 1.0)
        """
        self.failure_rate = failure_rate
        self.call_count = 0
    
    def call(self) -> str:
        """Call service."""
        self.call_count += 1
        
        import random
        if random.random() < self.failure_rate:
            raise Exception("Service unavailable")
        
        return f"Service response #{self.call_count}"


def fallback_function() -> str:
    """Fallback function when circuit is open."""
    return "Fallback response: Service temporarily unavailable"


def main() -> None:
    """Demonstration of Circuit Breaker Pattern."""
    print("=" * 70)
    print("CIRCUIT BREAKER PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic Circuit Breaker
    print("Example 1: Basic Circuit Breaker")
    print("-" * 70)
    
    config = CircuitBreakerConfig(
        failure_threshold=3,
        success_threshold=2,
        timeout_duration=5.0
    )
    breaker = CircuitBreaker(config)
    service = ExternalService(failure_rate=0.7)  # 70% failure rate
    
    print("Making calls through circuit breaker:")
    for i in range(10):
        try:
            result = breaker.call(service.call)
            print(f"  Call {i+1}: {result} (State: {breaker.get_state().value})")
        except CircuitBreakerOpenError:
            print(f"  Call {i+1}: Circuit OPEN - using fallback")
            result = fallback_function()
            print(f"  Fallback: {result}")
        except Exception as e:
            print(f"  Call {i+1}: Failed - {e} (State: {breaker.get_state().value})")
        
        time.sleep(0.1)
    print()
    
    # Example 2: Circuit Breaker Recovery
    print("Example 2: Circuit Breaker Recovery")
    print("-" * 70)
    
    breaker.reset()
    service = ExternalService(failure_rate=0.0)  # No failures
    
    print("Testing recovery (service now working):")
    for i in range(5):
        try:
            result = breaker.call(service.call)
            print(f"  Call {i+1}: {result} (State: {breaker.get_state().value})")
        except Exception as e:
            print(f"  Call {i+1}: {e}")
        time.sleep(0.1)
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Circuit Breaker")
    
    def circuit_breaker_operations():
        breaker = CircuitBreaker()
        service = ExternalService(failure_rate=0.1)
        
        success_count = 0
        for _ in range(100):
            try:
                breaker.call(service.call)
                success_count += 1
            except:
                pass
        
        return success_count
    
    result, metrics = timer.measure(circuit_breaker_operations)
    print(f"Time to process 100 calls: {metrics['execution_time_ms']:.3f} ms")
    print(f"Successful calls: {result}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Prevents cascading failures by stopping requests to a")
    print("  failing service and allowing it time to recover.")
    print("\nKey Advantages:")
    print("  - Prevents cascading failures")
    print("  - Fast failure detection")
    print("  - Automatic recovery")
    print("  - Fallback mechanisms")
    print("\nKey Disadvantages:")
    print("  - Additional complexity")
    print("  - Configuration tuning needed")
    print("  - May delay legitimate requests")
    print("\nWhen to Use:")
    print("  - External service calls")
    print("  - Network operations")
    print("  - Database connections")
    print("  - Microservices communication")
    print("\nCommon Use Cases:")
    print("  - Netflix Hystrix")
    print("  - Resilience4j")
    print("  - Polly (.NET)")
    print("  - API gateway patterns")
    print("=" * 70)


if __name__ == "__main__":
    main()
