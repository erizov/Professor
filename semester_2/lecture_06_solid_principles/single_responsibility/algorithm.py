#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single Responsibility Principle (SRP).

A class should have only one reason to change. Each class should have
a single, well-defined responsibility.
"""

import sys
from pathlib import Path
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# ❌ BAD: Violates SRP - multiple responsibilities
class BadEmployee:
    """Employee class with multiple responsibilities."""
    
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary
    
    def calculate_pay(self) -> float:
        """Calculate employee pay."""
        return self.salary * 0.8  # After tax
    
    def save_to_database(self) -> None:
        """Save employee to database."""
        logger.info(f"Saving {self.name} to database...")
    
    def send_email(self, message: str) -> None:
        """Send email to employee."""
        logger.info(f"Sending email to {self.name}: {message}")
    
    def generate_report(self) -> str:
        """Generate employee report."""
        return f"Report for {self.name}"


# ✅ GOOD: Follows SRP - single responsibility
class Employee:
    """Employee class - only stores employee data."""
    
    def __init__(self, name: str, salary: float):
        self.name = name
        self.salary = salary


class PayCalculator:
    """Responsible only for calculating pay."""
    
    @staticmethod
    def calculate_pay(employee: Employee) -> float:
        """Calculate employee pay."""
        return employee.salary * 0.8  # After tax


class EmployeeRepository:
    """Responsible only for data persistence."""
    
    @staticmethod
    def save(employee: Employee) -> None:
        """Save employee to database."""
        logger.info(f"Saving {self.name} to database...")


class EmailService:
    """Responsible only for sending emails."""
    
    @staticmethod
    def send_email(employee: Employee, message: str) -> None:
        """Send email to employee."""
        logger.info(f"Sending email to {employee.name}: {message}")


class ReportGenerator:
    """Responsible only for generating reports."""
    
    @staticmethod
    def generate_report(employee: Employee) -> str:
        """Generate employee report."""
        return f"Report for {employee.name}"


# Example 2: File Operations
# ❌ BAD: Multiple responsibilities
class BadFileManager:
    """File manager with multiple responsibilities."""
    
    def read_file(self, filename: str) -> str:
        """Read file content."""
        with open(filename, 'r') as f:
            return f.read()
    
    def write_file(self, filename: str, content: str) -> None:
        """Write content to file."""
        with open(filename, 'w') as f:
            f.write(content)
    
    def compress_file(self, filename: str) -> None:
        """Compress file."""
        logger.info(f"Compressing {filename}...")
    
    def encrypt_file(self, filename: str) -> None:
        """Encrypt file."""
        logger.info(f"Encrypting {filename}...")


# ✅ GOOD: Separate responsibilities
class FileReader:
    """Responsible only for reading files."""
    
    @staticmethod
    def read(filename: str) -> str:
        """Read file content."""
        with open(filename, 'r') as f:
            return f.read()


class FileWriter:
    """Responsible only for writing files."""
    
    @staticmethod
    def write(filename: str, content: str) -> None:
        """Write content to file."""
        with open(filename, 'w') as f:
            f.write(content)


class FileCompressor:
    """Responsible only for compressing files."""
    
    @staticmethod
    def compress(filename: str) -> None:
        """Compress file."""
        logger.info(f"Compressing {filename}...")


class FileEncryptor:
    """Responsible only for encrypting files."""
    
    @staticmethod
    def encrypt(filename: str) -> None:
        """Encrypt file."""
        logger.info(f"Encrypting {filename}...")


# Example 3: Order Processing
# ❌ BAD: Multiple responsibilities
class BadOrder:
    """Order with multiple responsibilities."""
    
    def __init__(self, items: list, customer: str):
        self.items = items
        self.customer = customer
        self.total = sum(item['price'] for item in items)
    
    def calculate_total(self) -> float:
        """Calculate order total."""
        return self.total
    
    def validate(self) -> bool:
        """Validate order."""
        return len(self.items) > 0
    
    def save(self) -> None:
        """Save order to database."""
        logger.info(f"Saving order for {self.customer}...")
    
    def send_confirmation(self) -> None:
        """Send confirmation email."""
        logger.info(f"Sending confirmation to {self.customer}...")


# ✅ GOOD: Separate responsibilities
class Order:
    """Order - only stores order data."""
    
    def __init__(self, items: list, customer: str):
        self.items = items
        self.customer = customer


class OrderCalculator:
    """Responsible only for calculations."""
    
    @staticmethod
    def calculate_total(order: Order) -> float:
        """Calculate order total."""
        return sum(item['price'] for item in order.items)


class OrderValidator:
    """Responsible only for validation."""
    
    @staticmethod
    def validate(order: Order) -> bool:
        """Validate order."""
        return len(order.items) > 0


class OrderRepository:
    """Responsible only for persistence."""
    
    @staticmethod
    def save(order: Order) -> None:
        """Save order to database."""
        logger.info(f"Saving order for {order.customer}...")


class OrderNotifier:
    """Responsible only for notifications."""
    
    @staticmethod
    def send_confirmation(order: Order) -> None:
        """Send confirmation email."""
        logger.info(f"Sending confirmation to {order.customer}...")


def main() -> None:
    """Demonstration of Single Responsibility Principle."""
    logger.info("=" * 70)
    logger.info("SINGLE RESPONSIBILITY PRINCIPLE (SRP) DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Employee Management
    logger.info("Example 1: Employee Management")
    logger.info("-" * 70)
    
    logger.info("❌ BAD: Single class with multiple responsibilities")
    bad_emp = BadEmployee("John", 50000)
    bad_emp.calculate_pay()
    bad_emp.save_to_database()
    bad_emp.send_email("Welcome!")
    logger.info()
    
    logger.info("✅ GOOD: Separate classes with single responsibilities")
    emp = Employee("John", 50000)
    pay = PayCalculator.calculate_pay(emp)
    logger.info(f"Pay: ${pay:.2f}")
    EmailService.send_email(emp, "Welcome!")
    report = ReportGenerator.generate_report(emp)
    logger.info(f"Report: {report}")
    logger.info()
    
    # Example 2: Order Processing
    logger.info("Example 2: Order Processing")
    logger.info("-" * 70)
    
    items = [
        {'name': 'Laptop', 'price': 999.99},
        {'name': 'Mouse', 'price': 29.99}
    ]
    
    order = Order(items, "Alice")
    
    # Use separate services
    total = OrderCalculator.calculate_total(order)
    is_valid = OrderValidator.validate(order)
    
    logger.info(f"Order total: ${total:.2f}")
    logger.info(f"Order valid: {is_valid}")
    
    if is_valid:
        OrderRepository.save(order)
        OrderNotifier.send_confirmation(order)
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPrinciple Summary:")
    logger.info("\nDefinition:")
    logger.info("  A class should have only one reason to change.")
    logger.info("  Each class should have a single, well-defined responsibility.")
    logger.info("\nKey Benefits:")
    logger.info("  - Easier to understand and maintain")
    logger.info("  - Easier to test")
    logger.info("  - Reduced coupling")
    logger.info("  - Better code organization")
    logger.info("  - Easier to modify")
    logger.info("\nSigns of Violation:")
    logger.info("  - Class has multiple reasons to change")
    logger.info("  - Class does too many things")
    logger.info("  - Methods are unrelated")
    logger.info("  - Hard to name the class clearly")
    logger.info("\nHow to Apply:")
    logger.info("  1. Identify responsibilities")
    logger.info("  2. Separate concerns")
    logger.info("  3. Create focused classes")
    logger.info("  4. Use composition")
    logger.info("\nCommon Violations:")
    logger.info("  - God classes (do everything)")
    logger.info("  - Mixed data and behavior")
    logger.info("  - Business logic in data classes")
    logger.info("  - Multiple unrelated methods")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()