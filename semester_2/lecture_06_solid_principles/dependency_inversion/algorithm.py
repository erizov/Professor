#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dependency Inversion Principle (DIP).

High-level modules should not depend on low-level modules. Both should
depend on abstractions. Abstractions should not depend on details.
Details should depend on abstractions.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# ❌ BAD: Violates DIP - high-level depends on low-level
class BadMySQLConnection:
    """Low-level MySQL connection."""
    
    def connect(self) -> None:
        logger.info("Connecting to MySQL database...")
    
    def query(self, sql: str) -> list:
        logger.info(f"Executing MySQL query: {sql}")
        return []


class BadPostgreSQLConnection:
    """Low-level PostgreSQL connection."""
    
    def connect(self) -> None:
        logger.info("Connecting to PostgreSQL database...")
    
    def query(self, sql: str) -> list:
        logger.info(f"Executing PostgreSQL query: {sql}")
        return []


class BadUserService:
    """High-level service - depends on concrete implementations!"""
    
    def __init__(self):
        # Direct dependency on concrete class - violates DIP!
        self.db = BadMySQLConnection()
        self.db.connect()
    
    def get_users(self) -> list:
        return self.db.query("SELECT * FROM users")


# ✅ GOOD: Follows DIP - depends on abstraction
class DatabaseConnection(ABC):
    """Abstract database connection (abstraction)."""
    
    @abstractmethod
    def connect(self) -> None:
        """Connect to database."""
        pass
    
    @abstractmethod
    def query(self, sql: str) -> list:
        """Execute query."""
        pass


class MySQLConnection(DatabaseConnection):
    """MySQL implementation (detail)."""
    
    def connect(self) -> None:
        logger.info("Connecting to MySQL database...")
    
    def query(self, sql: str) -> list:
        logger.info(f"Executing MySQL query: {sql}")
        return []


class PostgreSQLConnection(DatabaseConnection):
    """PostgreSQL implementation (detail)."""
    
    def connect(self) -> None:
        logger.info("Connecting to PostgreSQL database...")
    
    def query(self, sql: str) -> list:
        logger.info(f"Executing PostgreSQL query: {sql}")
        return []


class UserService:
    """High-level service - depends on abstraction."""
    
    def __init__(self, db: DatabaseConnection):
        # Depends on abstraction, not concrete class
        self.db = db
        self.db.connect()
    
    def get_users(self) -> list:
        return self.db.query("SELECT * FROM users")


# Example 2: Notification System
# ❌ BAD: Violates DIP
class BadEmailService:
    """Email service - concrete implementation."""
    
    def send(self, message: str) -> None:
        logger.info(f"Sending email: {message}")


class BadSMSService:
    """SMS service - concrete implementation."""
    
    def send(self, message: str) -> None:
        logger.info(f"Sending SMS: {message}")


class BadNotificationService:
    """Notification service - depends on concrete classes."""
    
    def __init__(self):
        # Direct dependency - violates DIP!
        self.email = BadEmailService()
    
    def notify(self, message: str) -> None:
        self.email.send(message)


# ✅ GOOD: Follows DIP
class MessageService(ABC):
    """Abstract message service (abstraction)."""
    
    @abstractmethod
    def send(self, message: str) -> None:
        """Send message."""
        pass


class EmailService(MessageService):
    """Email implementation (detail)."""
    
    def send(self, message: str) -> None:
        logger.info(f"Sending email: {message}")


class SMSService(MessageService):
    """SMS implementation (detail)."""
    
    def send(self, message: str) -> None:
        logger.info(f"Sending SMS: {message}")


class PushNotificationService(MessageService):
    """Push notification implementation (detail)."""
    
    def send(self, message: str) -> None:
        logger.info(f"Sending push notification: {message}")


class NotificationService:
    """Notification service - depends on abstraction."""
    
    def __init__(self, message_service: MessageService):
        # Depends on abstraction
        self.message_service = message_service
    
    def notify(self, message: str) -> None:
        self.message_service.send(message)


# Example 3: Payment Processing
class PaymentProcessor(ABC):
    """Abstract payment processor (abstraction)."""
    
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Process payment."""
        pass


class CreditCardProcessor(PaymentProcessor):
    """Credit card processor (detail)."""
    
    def process_payment(self, amount: float) -> bool:
        logger.info(f"Processing ${amount} via credit card")
        return True


class PayPalProcessor(PaymentProcessor):
    """PayPal processor (detail)."""
    
    def process_payment(self, amount: float) -> bool:
        logger.info(f"Processing ${amount} via PayPal")
        return True


class OrderService:
    """Order service - depends on abstraction."""
    
    def __init__(self, payment_processor: PaymentProcessor):
        # Depends on abstraction
        self.payment_processor = payment_processor
    
    def place_order(self, amount: float) -> bool:
        return self.payment_processor.process_payment(amount)


def main() -> None:
    """Demonstration of Dependency Inversion Principle."""
    logger.info("=" * 70)
    logger.info("DEPENDENCY INVERSION PRINCIPLE (DIP) DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Database Connection
    logger.info("Example 1: Database Connection")
    logger.info("-" * 70)
    
    logger.info("❌ BAD: High-level depends on low-level")
    bad_service = BadUserService()
    bad_service.get_users()
    logger.info()
    
    logger.info("✅ GOOD: Both depend on abstraction")
    # Can easily switch implementations
    mysql_db = MySQLConnection()
    user_service_mysql = UserService(mysql_db)
    user_service_mysql.get_users()
    
    postgres_db = PostgreSQLConnection()
    user_service_postgres = UserService(postgres_db)
    user_service_postgres.get_users()
    logger.info()
    
    # Example 2: Notification System
    logger.info("Example 2: Notification System")
    logger.info("-" * 70)
    
    # Can inject any implementation
    email_service = EmailService()
    notification = NotificationService(email_service)
    notification.notify("Hello via email")
    
    sms_service = SMSService()
    notification = NotificationService(sms_service)
    notification.notify("Hello via SMS")
    
    push_service = PushNotificationService()
    notification = NotificationService(push_service)
    notification.notify("Hello via push")
    logger.info()
    
    # Example 3: Payment Processing
    logger.info("Example 3: Payment Processing")
    logger.info("-" * 70)
    
    credit_card = CreditCardProcessor()
    order_service = OrderService(credit_card)
    order_service.place_order(100.0)
    
    paypal = PayPalProcessor()
    order_service = OrderService(paypal)
    order_service.place_order(50.0)
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPrinciple Summary:")
    logger.info("\nDefinition:")
    logger.info("  High-level modules should not depend on low-level modules.")
    logger.info("  Both should depend on abstractions. Abstractions should not")
    logger.info("  depend on details. Details should depend on abstractions.")
    logger.info("\nKey Benefits:")
    logger.info("  - Loose coupling")
    logger.info("  - Easy to test (can inject mocks)")
    logger.info("  - Easy to extend (add new implementations)")
    logger.info("  - Flexible and maintainable")
    logger.info("\nHow to Apply:")
    logger.info("  1. Use dependency injection")
    logger.info("  2. Depend on interfaces/abstractions")
    logger.info("  3. Avoid direct instantiation of concrete classes")
    logger.info("  4. Use inversion of control (IoC) containers")
    logger.info("\nCommon Violations:")
    logger.info("  - Direct instantiation of concrete classes")
    logger.info("  - High-level modules importing low-level modules")
    logger.info("  - Hard-coded dependencies")
    logger.info("  - Difficult to test")
    logger.info("\nDesign Patterns that Help:")
    logger.info("  - Dependency Injection")
    logger.info("  - Strategy Pattern")
    logger.info("  - Factory Pattern")
    logger.info("  - Service Locator Pattern")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()