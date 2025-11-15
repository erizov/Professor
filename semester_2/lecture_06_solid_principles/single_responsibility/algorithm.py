#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single Responsibility Principle (SRP).

A class should have only one reason to change. Each class should have
a single, well-defined responsibility.
"""

import sys
from pathlib import Path

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
        print(f"Saving {self.name} to database...")
    
    def send_email(self, message: str) -> None:
        """Send email to employee."""
        print(f"Sending email to {self.name}: {message}")
    
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
        print(f"Saving {self.name} to database...")


class EmailService:
    """Responsible only for sending emails."""
    
    @staticmethod
    def send_email(employee: Employee, message: str) -> None:
        """Send email to employee."""
        print(f"Sending email to {employee.name}: {message}")


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
        print(f"Compressing {filename}...")
    
    def encrypt_file(self, filename: str) -> None:
        """Encrypt file."""
        print(f"Encrypting {filename}...")


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
        print(f"Compressing {filename}...")


class FileEncryptor:
    """Responsible only for encrypting files."""
    
    @staticmethod
    def encrypt(filename: str) -> None:
        """Encrypt file."""
        print(f"Encrypting {filename}...")


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
        print(f"Saving order for {self.customer}...")
    
    def send_confirmation(self) -> None:
        """Send confirmation email."""
        print(f"Sending confirmation to {self.customer}...")


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
        print(f"Saving order for {order.customer}...")


class OrderNotifier:
    """Responsible only for notifications."""
    
    @staticmethod
    def send_confirmation(order: Order) -> None:
        """Send confirmation email."""
        print(f"Sending confirmation to {order.customer}...")


def main() -> None:
    """Demonstration of Single Responsibility Principle."""
    print("=" * 70)
    print("SINGLE RESPONSIBILITY PRINCIPLE (SRP) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Employee Management
    print("Example 1: Employee Management")
    print("-" * 70)
    
    print("❌ BAD: Single class with multiple responsibilities")
    bad_emp = BadEmployee("John", 50000)
    bad_emp.calculate_pay()
    bad_emp.save_to_database()
    bad_emp.send_email("Welcome!")
    print()
    
    print("✅ GOOD: Separate classes with single responsibilities")
    emp = Employee("John", 50000)
    pay = PayCalculator.calculate_pay(emp)
    print(f"Pay: ${pay:.2f}")
    EmailService.send_email(emp, "Welcome!")
    report = ReportGenerator.generate_report(emp)
    print(f"Report: {report}")
    print()
    
    # Example 2: Order Processing
    print("Example 2: Order Processing")
    print("-" * 70)
    
    items = [
        {'name': 'Laptop', 'price': 999.99},
        {'name': 'Mouse', 'price': 29.99}
    ]
    
    order = Order(items, "Alice")
    
    # Use separate services
    total = OrderCalculator.calculate_total(order)
    is_valid = OrderValidator.validate(order)
    
    print(f"Order total: ${total:.2f}")
    print(f"Order valid: {is_valid}")
    
    if is_valid:
        OrderRepository.save(order)
        OrderNotifier.send_confirmation(order)
    print()
    
    print("=" * 70)
    print("\nPrinciple Summary:")
    print("\nDefinition:")
    print("  A class should have only one reason to change.")
    print("  Each class should have a single, well-defined responsibility.")
    print("\nKey Benefits:")
    print("  - Easier to understand and maintain")
    print("  - Easier to test")
    print("  - Reduced coupling")
    print("  - Better code organization")
    print("  - Easier to modify")
    print("\nSigns of Violation:")
    print("  - Class has multiple reasons to change")
    print("  - Class does too many things")
    print("  - Methods are unrelated")
    print("  - Hard to name the class clearly")
    print("\nHow to Apply:")
    print("  1. Identify responsibilities")
    print("  2. Separate concerns")
    print("  3. Create focused classes")
    print("  4. Use composition")
    print("\nCommon Violations:")
    print("  - God classes (do everything)")
    print("  - Mixed data and behavior")
    print("  - Business logic in data classes")
    print("  - Multiple unrelated methods")
    print("=" * 70)


if __name__ == "__main__":
    main()
