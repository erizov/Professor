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

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# ❌ BAD: Violates DIP - high-level depends on low-level
class BadMySQLConnection:
    """Low-level MySQL connection."""
    
    def connect(self) -> None:
        print("Connecting to MySQL database...")
    
    def query(self, sql: str) -> list:
        print(f"Executing MySQL query: {sql}")
        return []


class BadPostgreSQLConnection:
    """Low-level PostgreSQL connection."""
    
    def connect(self) -> None:
        print("Connecting to PostgreSQL database...")
    
    def query(self, sql: str) -> list:
        print(f"Executing PostgreSQL query: {sql}")
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
        print("Connecting to MySQL database...")
    
    def query(self, sql: str) -> list:
        print(f"Executing MySQL query: {sql}")
        return []


class PostgreSQLConnection(DatabaseConnection):
    """PostgreSQL implementation (detail)."""
    
    def connect(self) -> None:
        print("Connecting to PostgreSQL database...")
    
    def query(self, sql: str) -> list:
        print(f"Executing PostgreSQL query: {sql}")
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
        print(f"Sending email: {message}")


class BadSMSService:
    """SMS service - concrete implementation."""
    
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")


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
        print(f"Sending email: {message}")


class SMSService(MessageService):
    """SMS implementation (detail)."""
    
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")


class PushNotificationService(MessageService):
    """Push notification implementation (detail)."""
    
    def send(self, message: str) -> None:
        print(f"Sending push notification: {message}")


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
        print(f"Processing ${amount} via credit card")
        return True


class PayPalProcessor(PaymentProcessor):
    """PayPal processor (detail)."""
    
    def process_payment(self, amount: float) -> bool:
        print(f"Processing ${amount} via PayPal")
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
    print("=" * 70)
    print("DEPENDENCY INVERSION PRINCIPLE (DIP) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Database Connection
    print("Example 1: Database Connection")
    print("-" * 70)
    
    print("❌ BAD: High-level depends on low-level")
    bad_service = BadUserService()
    bad_service.get_users()
    print()
    
    print("✅ GOOD: Both depend on abstraction")
    # Can easily switch implementations
    mysql_db = MySQLConnection()
    user_service_mysql = UserService(mysql_db)
    user_service_mysql.get_users()
    
    postgres_db = PostgreSQLConnection()
    user_service_postgres = UserService(postgres_db)
    user_service_postgres.get_users()
    print()
    
    # Example 2: Notification System
    print("Example 2: Notification System")
    print("-" * 70)
    
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
    print()
    
    # Example 3: Payment Processing
    print("Example 3: Payment Processing")
    print("-" * 70)
    
    credit_card = CreditCardProcessor()
    order_service = OrderService(credit_card)
    order_service.place_order(100.0)
    
    paypal = PayPalProcessor()
    order_service = OrderService(paypal)
    order_service.place_order(50.0)
    print()
    
    print("=" * 70)
    print("\nPrinciple Summary:")
    print("\nDefinition:")
    print("  High-level modules should not depend on low-level modules.")
    print("  Both should depend on abstractions. Abstractions should not")
    print("  depend on details. Details should depend on abstractions.")
    print("\nKey Benefits:")
    print("  - Loose coupling")
    print("  - Easy to test (can inject mocks)")
    print("  - Easy to extend (add new implementations)")
    print("  - Flexible and maintainable")
    print("\nHow to Apply:")
    print("  1. Use dependency injection")
    print("  2. Depend on interfaces/abstractions")
    print("  3. Avoid direct instantiation of concrete classes")
    print("  4. Use inversion of control (IoC) containers")
    print("\nCommon Violations:")
    print("  - Direct instantiation of concrete classes")
    print("  - High-level modules importing low-level modules")
    print("  - Hard-coded dependencies")
    print("  - Difficult to test")
    print("\nDesign Patterns that Help:")
    print("  - Dependency Injection")
    print("  - Strategy Pattern")
    print("  - Factory Pattern")
    print("  - Service Locator Pattern")
    print("=" * 70)


if __name__ == "__main__":
    main()
