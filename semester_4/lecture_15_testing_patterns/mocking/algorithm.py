#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mocking Pattern.

Creates mock objects that simulate the behavior of real objects for testing.
Allows testing in isolation without dependencies on external systems.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Dict
from unittest.mock import Mock, MagicMock, patch
from dataclasses import dataclass

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


class PaymentGateway(ABC):
    """Payment gateway interface."""
    
    @abstractmethod
    def process_payment(self, amount: float, card_number: str) -> bool:
        """Process payment."""
        pass


class RealPaymentGateway(PaymentGateway):
    """Real payment gateway (expensive to call in tests)."""
    
    def process_payment(self, amount: float, card_number: str) -> bool:
        """Process payment - would make real API call."""
        # In real implementation, this would call external API
        return True


class MockPaymentGateway(PaymentGateway):
    """Mock payment gateway for testing."""
    
    def __init__(self):
        self.call_count = 0
        self.last_amount = None
        self.should_succeed = True
    
    def process_payment(self, amount: float, card_number: str) -> bool:
        """Mock payment processing."""
        self.call_count += 1
        self.last_amount = amount
        return self.should_succeed


class OrderService:
    """Order service that depends on payment gateway."""
    
    def __init__(self, payment_gateway: PaymentGateway):
        self.payment_gateway = payment_gateway
    
    def place_order(self, amount: float, card_number: str) -> bool:
        """Place order and process payment."""
        if amount <= 0:
            return False
        
        return self.payment_gateway.process_payment(amount, card_number)


# Example: Using unittest.mock
class EmailService:
    """Email service."""
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email - would send real email."""
        return True


class NotificationService:
    """Notification service."""
    
    def __init__(self, email_service: EmailService):
        self.email_service = email_service
    
    def notify_user(self, user_email: str, message: str) -> bool:
        """Notify user via email."""
        return self.email_service.send_email(
            to=user_email,
            subject="Notification",
            body=message
        )


# Example: Stub implementation
class DatabaseStub:
    """Database stub for testing."""
    
    def __init__(self):
        self.data: Dict[str, Any] = {}
    
    def save(self, key: str, value: Any) -> None:
        """Save data."""
        self.data[key] = value
    
    def get(self, key: str) -> Optional[Any]:
        """Get data."""
        return self.data.get(key)
    
    def delete(self, key: str) -> bool:
        """Delete data."""
        if key in self.data:
            del self.data[key]
            return True
        return False


def main() -> None:
    """Demonstration of Mocking Pattern."""
    logger.info("=" * 70)
    logger.info("MOCKING PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Manual Mock
    logger.info("Example 1: Manual Mock Object")
    logger.info("-" * 70)
    
    mock_gateway = MockPaymentGateway()
    order_service = OrderService(mock_gateway)
    
    result = order_service.place_order(100.0, "1234-5678-9012-3456")
    
    logger.info(f"Order placed: {result}")
    logger.info(f"Payment gateway called: {mock_gateway.call_count} times")
    logger.info(f"Last amount: ${mock_gateway.last_amount}")
    logger.info()
    
    # Example 2: Mock with unittest.mock
    logger.info("Example 2: Using unittest.mock")
    logger.info("-" * 70)
    
    mock_email = Mock(spec=EmailService)
    mock_email.send_email.return_value = True
    
    notification_service = NotificationService(mock_email)
    result = notification_service.notify_user("user@example.com", "Test message")
    
    logger.info(f"Notification sent: {result}")
    logger.info(f"Email service called: {mock_email.send_email.called}")
    mock_email.send_email.assert_called_once_with(
        to="user@example.com",
        subject="Notification",
        body="Test message"
    )
    logger.info("Mock assertions passed")
    logger.info()
    
    # Example 3: Mock with patch
    logger.info("Example 3: Using patch decorator")
    logger.info("-" * 70)
    
    with patch('builtins.print') as mock_print:
        logger.info("This won't actually print")
        mock_print.assert_called_once_with("This won't actually print")
    
    logger.info("Patch test completed")
    logger.info()
    
    # Example 4: Stub implementation
    logger.info("Example 4: Stub Implementation")
    logger.info("-" * 70)
    
    db_stub = DatabaseStub()
    db_stub.save("user:123", {"name": "Alice", "email": "alice@example.com"})
    
    user = db_stub.get("user:123")
    logger.info(f"Retrieved user: {user}")
    
    deleted = db_stub.delete("user:123")
    logger.info(f"User deleted: {deleted}")
    logger.info(f"User still exists: {db_stub.get('user:123') is not None}")
    logger.info()
    
    # Example 5: Mock with side effects
    logger.info("Example 5: Mock with Side Effects")
    logger.info("-" * 70)
    
    mock_service = Mock()
    mock_service.process.side_effect = [True, False, Exception("Error")]
    
    logger.info(f"First call: {mock_service.process()}")
    logger.info(f"Second call: {mock_service.process()}")
    try:
        mock_service.process()
    except Exception as e:
        logger.info(f"Third call raised: {e}")
    logger.info()
    
    # Example 6: Performance measurement
    logger.info("Example 6: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Mocking")
    
    def mock_operations():
        mock_gateway = MockPaymentGateway()
        service = OrderService(mock_gateway)
        
        for _ in range(100):
            service.place_order(50.0, "1234-5678")
        
        return mock_gateway.call_count
    
    result, metrics = timer.measure(mock_operations)
    logger.info(f"Time to process 100 orders with mock: {metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Mock calls: {result}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Creates mock objects that simulate the behavior of real")
    logger.info("  objects for testing. Allows testing in isolation.")
    logger.info("\nKey Advantages:")
    logger.info("  - Fast test execution")
    logger.info("  - Isolated testing")
    logger.info("  - No external dependencies")
    logger.info("  - Predictable behavior")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Mocks may not match real behavior")
    logger.info("  - Maintenance overhead")
    logger.info("  - Can hide integration issues")
    logger.info("  - May make tests less realistic")
    logger.info("\nWhen to Use:")
    logger.info("  - External service dependencies")
    logger.info("  - Slow operations")
    logger.info("  - Unpredictable behavior")
    logger.info("  - Isolated unit testing")
    logger.info("\nCommon Use Cases:")
    logger.info("  - API mocking")
    logger.info("  - Database mocking")
    logger.info("  - File system mocking")
    logger.info("  - Network mocking")
    logger.info("\nMock Types:")
    logger.info("  - Mock: Generic mock object")
    logger.info("  - Stub: Returns predefined values")
    logger.info("  - Spy: Wraps real object, records calls")
    logger.info("  - Fake: Working implementation for testing")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()