#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Testing Pattern.

Tests individual units of code (functions, methods, classes) in isolation.
Ensures each unit works correctly before integration.
"""

import sys
from pathlib import Path
from typing import List, Callable, Any
import unittest

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


# Code to test
class Calculator:
    """Simple calculator for testing."""
    
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
            raise ValueError("Cannot divide by zero")
        return a / b


# Manual Unit Tests
class TestCalculator:
    """Manual unit test class."""
    
    def __init__(self):
        self.calculator = Calculator()
        self.tests_passed = 0
        self.tests_failed = 0
    
    def assert_equal(self, actual: Any, expected: Any, test_name: str) -> None:
        """Assert that actual equals expected."""
        if actual == expected:
            logger.info(f"✓ {test_name}: PASSED")
            self.tests_passed += 1
        else:
            logger.info(f"✗ {test_name}: FAILED (expected {expected}, got {actual})")
            self.tests_failed += 1
    
    def assert_raises(self, func: Callable, exception_type: type, 
                     test_name: str, *args, **kwargs) -> None:
        """Assert that function raises exception."""
        try:
            func(*args, **kwargs)
            logger.info(f"✗ {test_name}: FAILED (expected {exception_type.__name__})")
            self.tests_failed += 1
        except exception_type:
            logger.info(f"✓ {test_name}: PASSED")
            self.tests_passed += 1
        except Exception as e:
            logger.info(f"✗ {test_name}: FAILED (got {type(e).__name__})")
            self.tests_failed += 1
    
    def test_add(self) -> None:
        """Test addition."""
        self.assert_equal(self.calculator.add(2, 3), 5, "test_add")
        self.assert_equal(self.calculator.add(-1, 1), 0, "test_add_negative")
        self.assert_equal(self.calculator.add(0, 0), 0, "test_add_zero")
    
    def test_subtract(self) -> None:
        """Test subtraction."""
        self.assert_equal(self.calculator.subtract(5, 3), 2, "test_subtract")
        self.assert_equal(self.calculator.subtract(0, 5), -5, "test_subtract_negative")
    
    def test_multiply(self) -> None:
        """Test multiplication."""
        self.assert_equal(self.calculator.multiply(3, 4), 12, "test_multiply")
        self.assert_equal(self.calculator.multiply(0, 5), 0, "test_multiply_zero")
    
    def test_divide(self) -> None:
        """Test division."""
        self.assert_equal(self.calculator.divide(10, 2), 5, "test_divide")
        self.assert_raises(
            lambda: self.calculator.divide(10, 0),
            ValueError,
            "test_divide_by_zero"
        )
    
    def run_all_tests(self) -> None:
        """Run all tests."""
        logger.info("Running unit tests...")
        logger.info()
        self.test_add()
        self.test_subtract()
        self.test_multiply()
        self.test_divide()
        logger.info()
        logger.info(f"Tests passed: {self.tests_passed}")
        logger.info(f"Tests failed: {self.tests_failed}")
        logger.info(f"Total: {self.tests_passed + self.tests_failed}")


# Using unittest framework
class CalculatorTest(unittest.TestCase):
    """Unit tests using unittest framework."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.calculator = Calculator()
    
    def test_add(self) -> None:
        """Test addition."""
        self.assertEqual(self.calculator.add(2, 3), 5)
        self.assertEqual(self.calculator.add(-1, 1), 0)
    
    def test_subtract(self) -> None:
        """Test subtraction."""
        self.assertEqual(self.calculator.subtract(5, 3), 2)
    
    def test_multiply(self) -> None:
        """Test multiplication."""
        self.assertEqual(self.calculator.multiply(3, 4), 12)
    
    def test_divide(self) -> None:
        """Test division."""
        self.assertEqual(self.calculator.divide(10, 2), 5)
        with self.assertRaises(ValueError):
            self.calculator.divide(10, 0)


# Example 2: Testing User Service
class UserService:
    """User service for testing."""
    
    def __init__(self):
        self.users: List[dict] = []
    
    def create_user(self, username: str, email: str) -> dict:
        """Create user."""
        if not username or not email:
            raise ValueError("Username and email required")
        user = {"id": len(self.users) + 1, "username": username, "email": email}
        self.users.append(user)
        return user
    
    def get_user(self, user_id: int) -> dict:
        """Get user by ID."""
        for user in self.users:
            if user["id"] == user_id:
                return user
        raise ValueError("User not found")


class UserServiceTest(unittest.TestCase):
    """Unit tests for UserService."""
    
    def setUp(self) -> None:
        """Set up test fixtures."""
        self.service = UserService()
    
    def test_create_user(self) -> None:
        """Test user creation."""
        user = self.service.create_user("alice", "alice@example.com")
        self.assertEqual(user["username"], "alice")
        self.assertEqual(user["email"], "alice@example.com")
    
    def test_create_user_invalid(self) -> None:
        """Test invalid user creation."""
        with self.assertRaises(ValueError):
            self.service.create_user("", "email@example.com")
    
    def test_get_user(self) -> None:
        """Test get user."""
        user = self.service.create_user("bob", "bob@example.com")
        found = self.service.get_user(user["id"])
        self.assertEqual(found["username"], "bob")
    
    def test_get_user_not_found(self) -> None:
        """Test get non-existent user."""
        with self.assertRaises(ValueError):
            self.service.get_user(999)


def main() -> None:
    """Demonstration of Unit Testing Pattern."""
    logger.info("=" * 70)
    logger.info("UNIT TESTING PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Manual Unit Tests
    logger.info("Example 1: Manual Unit Tests")
    logger.info("-" * 70)
    
    test_suite = TestCalculator()
    test_suite.run_all_tests()
    logger.info()
    
    # Example 2: Using unittest Framework
    logger.info("Example 2: Using unittest Framework")
    logger.info("-" * 70)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(CalculatorTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    logger.info()
    
    # Example 3: User Service Tests
    logger.info("Example 3: User Service Unit Tests")
    logger.info("-" * 70)
    
    suite = unittest.TestLoader().loadTestsFromTestCase(UserServiceTest)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    logger.info()
    
    # Example 4: Performance measurement
    logger.info("Example 4: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Unit Testing")
    
    def test_execution():
        calc = Calculator()
        results = []
        for i in range(1000):
            results.append(calc.add(i, i + 1))
        return len(results)
    
    result, metrics = timer.measure(test_execution)
    logger.info(f"Time to execute 1000 test operations: "
          f"{metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Test individual units of code (functions, methods, classes)")
    logger.info("  in isolation. Ensures each unit works correctly.")
    logger.info("\nKey Advantages:")
    logger.info("  - Early bug detection")
    logger.info("  - Confidence in code")
    logger.info("  - Documentation through tests")
    logger.info("  - Regression prevention")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Time investment")
    logger.info("  - Maintenance overhead")
    logger.info("  - May not catch integration issues")
    logger.info("\nWhen to Use:")
    logger.info("  - All production code")
    logger.info("  - Critical business logic")
    logger.info("  - Complex algorithms")
    logger.info("  - API endpoints")
    logger.info("\nCommon Use Cases:")
    logger.info("  - JUnit (Java)")
    logger.info("  - pytest (Python)")
    logger.info("  - Jest (JavaScript)")
    logger.info("  - xUnit (.NET)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()