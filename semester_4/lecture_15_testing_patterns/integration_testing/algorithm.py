#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration Testing Pattern.

Tests the integration between different components, modules, or systems
to ensure they work together correctly.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


@dataclass
class TestResult:
    """Test result."""
    test_name: str
    passed: bool
    message: str
    execution_time: float = 0.0


class IntegrationTest:
    """Integration test base class."""
    
    def __init__(self, name: str):
        self.name = name
        self.setup_called = False
        self.teardown_called = False
    
    def setup(self) -> None:
        """Setup test environment."""
        self.setup_called = True
    
    def teardown(self) -> None:
        """Cleanup after test."""
        self.teardown_called = True
    
    def run(self) -> TestResult:
        """Run integration test."""
        import time
        start = time.time()
        
        try:
            self.setup()
            result = self.execute()
            self.teardown()
            
            elapsed = time.time() - start
            return TestResult(
                test_name=self.name,
                passed=result,
                message="Test passed" if result else "Test failed",
                execution_time=elapsed
            )
        except Exception as e:
            self.teardown()
            elapsed = time.time() - start
            return TestResult(
                test_name=self.name,
                passed=False,
                message=f"Test error: {str(e)}",
                execution_time=elapsed
            )
    
    def execute(self) -> bool:
        """Execute test logic - to be overridden."""
        return True


# Example: Database Integration Test
class DatabaseService:
    """Simulated database service."""
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
    
    def save(self, key: str, value: Any) -> None:
        """Save data."""
        self.data[key] = value
    
    def get(self, key: str) -> Any:
        """Get data."""
        return self.data.get(key)
    
    def delete(self, key: str) -> None:
        """Delete data."""
        if key in self.data:
            del self.data[key]


class UserService:
    """User service."""
    
    def __init__(self, db: DatabaseService):
        self.db = db
    
    def create_user(self, user_id: str, name: str) -> None:
        """Create user."""
        self.db.save(f"user:{user_id}", {"id": user_id, "name": name})
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get user."""
        return self.db.get(f"user:{user_id}")


class DatabaseIntegrationTest(IntegrationTest):
    """Database integration test."""
    
    def __init__(self):
        super().__init__("Database Integration Test")
        self.db = None
        self.user_service = None
    
    def setup(self) -> None:
        """Setup test database."""
        super().setup()
        self.db = DatabaseService()
        self.user_service = UserService(self.db)
    
    def execute(self) -> bool:
        """Test database operations."""
        # Test create
        self.user_service.create_user("123", "Alice")
        user = self.user_service.get_user("123")
        
        if not user or user["name"] != "Alice":
            return False
        
        return True


# Example: API Integration Test
class APIClient:
    """Simulated API client."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.responses: Dict[str, Any] = {}
    
    def get(self, endpoint: str) -> Dict[str, Any]:
        """GET request."""
        return self.responses.get(endpoint, {})
    
    def post(self, endpoint: str, data: Dict) -> Dict[str, Any]:
        """POST request."""
        self.responses[endpoint] = data
        return {"status": "success", "data": data}


class APIIntegrationTest(IntegrationTest):
    """API integration test."""
    
    def __init__(self):
        super().__init__("API Integration Test")
        self.api_client = None
    
    def setup(self) -> None:
        """Setup API client."""
        super().setup()
        self.api_client = APIClient("http://api.example.com")
    
    def execute(self) -> bool:
        """Test API integration."""
        # Test POST
        response = self.api_client.post("/users", {"name": "Bob"})
        if response["status"] != "success":
            return False
        
        # Test GET
        data = self.api_client.get("/users")
        return bool(data)


class TestRunner:
    """Integration test runner."""
    
    def __init__(self):
        self.tests: List[IntegrationTest] = []
        self.results: List[TestResult] = []
    
    def add_test(self, test: IntegrationTest) -> None:
        """Add test to suite."""
        self.tests.append(test)
    
    def run_all(self) -> List[TestResult]:
        """Run all tests."""
        self.results = []
        
        for test in self.tests:
            result = test.run()
            self.results.append(result)
        
        return self.results
    
    def print_results(self) -> None:
        """Print test results."""
        logger.info("Integration Test Results:")
        logger.info("-" * 70)
        
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        for result in self.results:
            status = "✓ PASS" if result.passed else "✗ FAIL"
            logger.info(f"{status}: {result.test_name}")
            if not result.passed:
                logger.info(f"  Error: {result.message}")
            logger.info(f"  Time: {result.execution_time*1000:.2f} ms")
        
        logger.info("-" * 70)
        logger.info(f"Total: {passed}/{total} passed")
        logger.info()


def main() -> None:
    """Demonstration of Integration Testing Pattern."""
    logger.info("=" * 70)
    logger.info("INTEGRATION TESTING PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Database Integration Test
    logger.info("Example 1: Database Integration Test")
    logger.info("-" * 70)
    
    db_test = DatabaseIntegrationTest()
    result = db_test.run()
    
    logger.info(f"Test: {result.test_name}")
    logger.info(f"Result: {'PASSED' if result.passed else 'FAILED'}")
    logger.info(f"Message: {result.message}")
    logger.info()
    
    # Example 2: API Integration Test
    logger.info("Example 2: API Integration Test")
    logger.info("-" * 70)
    
    api_test = APIIntegrationTest()
    result = api_test.run()
    
    logger.info(f"Test: {result.test_name}")
    logger.info(f"Result: {'PASSED' if result.passed else 'FAILED'}")
    logger.info()
    
    # Example 3: Test Suite
    logger.info("Example 3: Integration Test Suite")
    logger.info("-" * 70)
    
    runner = TestRunner()
    runner.add_test(DatabaseIntegrationTest())
    runner.add_test(APIIntegrationTest())
    
    results = runner.run_all()
    runner.print_results()
    
    # Example 4: Performance measurement
    logger.info("Example 4: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Integration Testing")
    
    def test_suite_execution():
        runner = TestRunner()
        runner.add_test(DatabaseIntegrationTest())
        runner.add_test(APIIntegrationTest())
        return len(runner.run_all())
    
    result, metrics = timer.measure(test_suite_execution)
    logger.info(f"Time to run integration test suite: {metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Tests executed: {result}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Tests the integration between different components, modules,")
    logger.info("  or systems to ensure they work together correctly.")
    logger.info("\nKey Advantages:")
    logger.info("  - Catches integration issues early")
    logger.info("  - Tests real interactions")
    logger.info("  - Validates system behavior")
    logger.info("  - Confidence in deployments")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Slower than unit tests")
    logger.info("  - More complex setup")
    logger.info("  - Harder to debug")
    logger.info("  - May require external dependencies")
    logger.info("\nWhen to Use:")
    logger.info("  - Testing component interactions")
    logger.info("  - API integration")
    logger.info("  - Database integration")
    logger.info("  - End-to-end workflows")
    logger.info("\nCommon Use Cases:")
    logger.info("  - API integration tests")
    logger.info("  - Database integration tests")
    logger.info("  - Service integration tests")
    logger.info("  - End-to-end tests")
    logger.info("\nTesting Pyramid:")
    logger.info("  - Unit Tests: 70% (fast, isolated)")
    logger.info("  - Integration Tests: 20% (component interactions)")
    logger.info("  - E2E Tests: 10% (full system)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()