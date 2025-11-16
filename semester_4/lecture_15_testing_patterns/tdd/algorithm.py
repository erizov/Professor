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
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers."""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Division by zero")
        return a / b


# TDD Example: Stack
class Stack:
    """Stack implementation following TDD."""
    
    def __init__(self):
        self.items: List[Any] = []
    
    def push(self, item: Any) -> None:
        """Push item onto stack."""
        self.items.append(item)
    
    def pop(self) -> Any:
        """Pop item from stack."""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()
    
    def peek(self) -> Any:
        """Peek at top item."""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]
    
    def is_empty(self) -> bool:
        """Check if stack is empty."""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Get stack size."""
        return len(self.items)


class TDDTestRunner:
    """Simple test runner for TDD demonstration."""
    
    def __init__(self):
        self.tests: List[tuple] = []
        self.passed = 0
        self.failed = 0
    
    def assert_equal(self, actual: Any, expected: Any, message: str = "") -> bool:
        """Assert two values are equal."""
        if actual == expected:
            self.passed += 1
            return True
        else:
            self.failed += 1
            logger.info(f"  ✗ FAIL: {message}")
            logger.info(f"    Expected: {expected}, Got: {actual}")
            return False
    
    def assert_raises(self, func: Callable, exception_type: type, message: str = "") -> bool:
        """Assert function raises exception."""
        try:
            func()
            self.failed += 1
            logger.info(f"  ✗ FAIL: {message} - Expected {exception_type.__name__}")
            return False
        except exception_type:
            self.passed += 1
            return True
        except Exception as e:
            self.failed += 1
            logger.info(f"  ✗ FAIL: {message} - Got {type(e).__name__} instead of {exception_type.__name__}")
            return False
    
    def run_tests(self) -> None:
        """Run all tests."""
        logger.info("Running TDD Tests:")
        logger.info("-" * 70)
        
        # Calculator tests
        calc = Calculator()
        
        self.assert_equal(calc.add(2, 3), 5, "Add 2 + 3 = 5")
        self.assert_equal(calc.subtract(5, 3), 2, "Subtract 5 - 3 = 2")
        self.assert_equal(calc.multiply(4, 3), 12, "Multiply 4 * 3 = 12")
        self.assert_equal(calc.divide(10, 2), 5.0, "Divide 10 / 2 = 5")
        
        self.assert_raises(
            lambda: calc.divide(10, 0),
            ValueError,
            "Division by zero raises ValueError"
        )
        
        # Stack tests
        stack = Stack()
        
        self.assert_equal(stack.is_empty(), True, "New stack is empty")
        self.assert_equal(stack.size(), 0, "New stack size is 0")
        
        stack.push(1)
        self.assert_equal(stack.is_empty(), False, "Stack not empty after push")
        self.assert_equal(stack.size(), 1, "Stack size is 1 after one push")
        self.assert_equal(stack.peek(), 1, "Peek returns top item")
        
        stack.push(2)
        self.assert_equal(stack.peek(), 2, "Peek returns new top item")
        
        popped = stack.pop()
        self.assert_equal(popped, 2, "Pop returns top item")
        self.assert_equal(stack.size(), 1, "Stack size after pop")
        
        self.assert_raises(
            lambda: Stack().pop(),
            IndexError,
            "Pop from empty stack raises IndexError"
        )
        
        logger.info("-" * 70)
        logger.info(f"Tests: {self.passed} passed, {self.failed} failed")
        logger.info()


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