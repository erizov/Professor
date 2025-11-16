#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Open/Closed Principle (OCP).

Software entities should be open for extension but closed for modification.
You should be able to add new functionality without changing existing code.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# ❌ BAD: Violates OCP - must modify existing code to add new shapes
class BadAreaCalculator:
    """Area calculator that violates OCP."""
    
    def calculate_area(self, shape: dict) -> float:
        """Calculate area - requires modification for new shapes."""
        shape_type = shape['type']
        
        if shape_type == 'rectangle':
            return shape['width'] * shape['height']
        elif shape_type == 'circle':
            return 3.14159 * shape['radius'] ** 2
        elif shape_type == 'triangle':
            return 0.5 * shape['base'] * shape['height']
        # Must modify this method to add new shapes!
        else:
            raise ValueError(f"Unknown shape: {shape_type}")


# ✅ GOOD: Follows OCP - open for extension, closed for modification
class Shape(ABC):
    """Abstract shape interface."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate area."""
        pass


class Rectangle(Shape):
    """Rectangle shape."""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height


class Circle(Shape):
    """Circle shape."""
    
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2


class Triangle(Shape):
    """Triangle shape."""
    
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height
    
    def area(self) -> float:
        return 0.5 * self.base * self.height


# Can add new shapes without modifying AreaCalculator!
class Square(Shape):
    """Square shape - added without modifying existing code."""
    
    def __init__(self, side: float):
        self.side = side
    
    def area(self) -> float:
        return self.side ** 2


class AreaCalculator:
    """Area calculator that follows OCP."""
    
    def calculate_total_area(self, shapes: List[Shape]) -> float:
        """Calculate total area - no modification needed for new shapes."""
        return sum(shape.area() for shape in shapes)


# Example 2: Payment Processing
# ❌ BAD: Must modify for new payment methods
class BadPaymentProcessor:
    """Payment processor that violates OCP."""
    
    def process_payment(self, amount: float, method: str) -> bool:
        """Process payment - requires modification for new methods."""
        if method == 'credit_card':
            return self._process_credit_card(amount)
        elif method == 'paypal':
            return self._process_paypal(amount)
        # Must modify to add new payment methods!
        else:
            raise ValueError(f"Unknown payment method: {method}")
    
    def _process_credit_card(self, amount: float) -> bool:
        logger.info(f"Processing ${amount} via credit card")
        return True
    
    def _process_paypal(self, amount: float) -> bool:
        logger.info(f"Processing ${amount} via PayPal")
        return True


# ✅ GOOD: Open for extension
class PaymentMethod(ABC):
    """Abstract payment method."""
    
    @abstractmethod
    def process(self, amount: float) -> bool:
        """Process payment."""
        pass


class CreditCardPayment(PaymentMethod):
    """Credit card payment."""
    
    def process(self, amount: float) -> bool:
        logger.info(f"Processing ${amount} via credit card")
        return True


class PayPalPayment(PaymentMethod):
    """PayPal payment."""
    
    def process(self, amount: float) -> bool:
        logger.info(f"Processing ${amount} via PayPal")
        return True


# Can add new payment methods without modifying processor!
class CryptocurrencyPayment(PaymentMethod):
    """Cryptocurrency payment - added without modification."""
    
    def process(self, amount: float) -> bool:
        logger.info(f"Processing ${amount} via cryptocurrency")
        return True


class PaymentProcessor:
    """Payment processor that follows OCP."""
    
    def process_payment(self, method: PaymentMethod, amount: float) -> bool:
        """Process payment - no modification needed for new methods."""
        return method.process(amount)


# Example 3: Discount System
class Discount(ABC):
    """Abstract discount."""
    
    @abstractmethod
    def apply(self, price: float) -> float:
        """Apply discount."""
        pass


class NoDiscount(Discount):
    """No discount."""
    
    def apply(self, price: float) -> float:
        return price


class PercentageDiscount(Discount):
    """Percentage discount."""
    
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def apply(self, price: float) -> float:
        return price * (1 - self.percentage / 100)


class FixedDiscount(Discount):
    """Fixed amount discount."""
    
    def __init__(self, amount: float):
        self.amount = amount
    
    def apply(self, price: float) -> float:
        return max(0, price - self.amount)


# Can add new discount types without modifying price calculator!
class BuyOneGetOneDiscount(Discount):
    """BOGO discount - added without modification."""
    
    def apply(self, price: float) -> float:
        return price / 2  # Pay for one, get one free


class PriceCalculator:
    """Price calculator that follows OCP."""
    
    def calculate_final_price(self, base_price: float, 
                             discount: Discount) -> float:
        """Calculate final price - no modification needed for new discounts."""
        return discount.apply(base_price)


def main() -> None:
    """Demonstration of Open/Closed Principle."""
    logger.info("=" * 70)
    logger.info("OPEN/CLOSED PRINCIPLE (OCP) DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Shape Area Calculation
    logger.info("Example 1: Shape Area Calculation")
    logger.info("-" * 70)
    
    logger.info("❌ BAD: Must modify AreaCalculator to add new shapes")
    bad_calc = BadAreaCalculator()
    logger.info(f"Rectangle area: {bad_calc.calculate_area({'type': 'rectangle', 'width': 5, 'height': 3})}")
    logger.info()
    
    logger.info("✅ GOOD: Can add new shapes without modifying AreaCalculator")
    shapes = [
        Rectangle(5, 3),
        Circle(2),
        Triangle(4, 3),
        Square(4)  # New shape added without modification!
    ]
    
    calc = AreaCalculator()
    total = calc.calculate_total_area(shapes)
    logger.info(f"Total area of all shapes: {total:.2f}")
    logger.info()
    
    # Example 2: Payment Processing
    logger.info("Example 2: Payment Processing")
    logger.info("-" * 70)
    
    processor = PaymentProcessor()
    
    # Existing payment methods
    processor.process_payment(CreditCardPayment(), 100.0)
    processor.process_payment(PayPalPayment(), 50.0)
    
    # New payment method - no modification needed!
    processor.process_payment(CryptocurrencyPayment(), 75.0)
    logger.info()
    
    # Example 3: Discount System
    logger.info("Example 3: Discount System")
    logger.info("-" * 70)
    
    base_price = 100.0
    
    discounts = [
        NoDiscount(),
        PercentageDiscount(10),
        FixedDiscount(20),
        BuyOneGetOneDiscount()  # New discount type!
    ]
    
    calculator = PriceCalculator()
    for discount in discounts:
        final = calculator.calculate_final_price(base_price, discount)
        logger.info(f"Base: ${base_price:.2f}, Final: ${final:.2f} ({discount.__class__.__name__})")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPrinciple Summary:")
    logger.info("\nDefinition:")
    logger.info("  Software entities should be open for extension but")
    logger.info("  closed for modification.")
    logger.info("\nKey Benefits:")
    logger.info("  - Add new features without breaking existing code")
    logger.info("  - Reduce risk of introducing bugs")
    logger.info("  - Better code stability")
    logger.info("  - Easier to maintain")
    logger.info("\nHow to Apply:")
    logger.info("  1. Use abstraction (interfaces/abstract classes)")
    logger.info("  2. Use polymorphism")
    logger.info("  3. Use strategy pattern")
    logger.info("  4. Avoid if/else chains for types")
    logger.info("\nCommon Violations:")
    logger.info("  - if/else chains for type checking")
    logger.info("  - switch statements for types")
    logger.info("  - Modifying existing classes for new features")
    logger.info("  - God classes that do everything")
    logger.info("\nDesign Patterns that Help:")
    logger.info("  - Strategy Pattern")
    logger.info("  - Template Method")
    logger.info("  - Decorator Pattern")
    logger.info("  - Factory Pattern")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()