#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test-Driven Development (TDD) Pattern.

Development approach where tests are written before implementation.
Follows Red-Green-Refactor cycle: Write test (Red), Implement (Green), Refactor.
"""

import sys
from pathlib import Path
from typing import List, Optional, Callable, Any

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


# TDD Example: Calculator
class Calculator:
    """Calculator implementation following TDD."""
    
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        
    """
    Tdd implementation.
    
    Args:
        *args: Variable arguments
        **kwargs: Keyword arguments
        
    Returns:
        Algorithm result
    """
    # Implementation for tdd
    logger.info(f"Executing tdd")
    return None


def main() -> None:
    """Demonstration of TDD Pattern."""
    logger.info("=" * 70)
    logger.info("TEST-DRIVEN DEVELOPMENT (TDD) PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: TDD Cycle Demonstration
    logger.info("Example 1: TDD Red-Green-Refactor Cycle")
    logger.info("-" * 70)
    
    logger.info("TDD Cycle:")
    logger.info("  1. RED: Write failing test")
    logger.info("  2. GREEN: Write minimal code to pass")
    logger.info("  3. REFACTOR: Improve code while keeping tests green")
    logger.info()
    
    # Example 2: Running TDD Tests
    logger.info("Example 2: Running TDD Tests")
    logger.info("-" * 70)
    
    runner = TDDTestRunner()
    runner.run_tests()
    
    # Example 3: TDD Benefits
    logger.info("Example 3: TDD Benefits Demonstration")
    logger.info("-" * 70)
    
    # Well-tested code
    calc = Calculator()
    
    # Test various scenarios
    test_cases = [
        (calc.add, (1, 2), 3),
        (calc.multiply, (4, 5), 20),
        (calc.divide, (15, 3), 5.0),
    ]
    
    logger.info("Testing calculator with multiple scenarios:")
    for func, args, expected in test_cases:
        result = func(*args)
        status = "✓" if result == expected else "✗"
        logger.info(f"  {status} {func.__name__}{args} = {result} (expected {expected})")
    logger.info()
    
    # Example 4: Performance measurement
    logger.info("Example 4: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("TDD")
    
    def tdd_operations():
        calc = Calculator()
        stack = Stack()
        
        # Perform operations
        for i in range(100):
            calc.add(i, i+1)
            stack.push(i)
        
        return stack.size()
    
    result, metrics = timer.measure(tdd_operations)
    logger.info(f"Time to perform TDD operations: {metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Development approach where tests are written before")
    logger.info("  implementation. Follows Red-Green-Refactor cycle.")
    logger.info("\nTDD Cycle:")
    logger.info("  1. RED: Write failing test")
    logger.info("  2. GREEN: Write minimal code to make test pass")
    logger.info("  3. REFACTOR: Improve code while keeping tests green")
    logger.info("  4. Repeat")
    logger.info("\nKey Advantages:")
    logger.info("  - Better code design")
    logger.info("  - Comprehensive test coverage")
    logger.info("  - Confidence in refactoring")
    logger.info("  - Documentation through tests")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Slower initial development")
    logger.info("  - Learning curve")
    logger.info("  - Can be overkill for simple code")
    logger.info("  - Requires discipline")
    logger.info("\nWhen to Use:")
    logger.info("  - Complex logic")
    logger.info("  - Critical functionality")
    logger.info("  - API development")
    logger.info("  - When requirements are clear")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Algorithm implementation")
    logger.info("  - API development")
    logger.info("  - Business logic")
    logger.info("  - Library development")
    logger.info("\nBest Practices:")
    logger.info("  - Write one test at a time")
    logger.info("  - Keep tests simple")
    logger.info("  - Test behavior, not implementation")
    logger.info("  - Refactor regularly")
    logger.info("  - Maintain test quality")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()