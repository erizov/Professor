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
        
    
    
    """
    Open Closed implementation.
    
    Args:
        *args: Variable arguments
        **kwargs: Keyword arguments
        
    Returns:
        Algorithm result
    """
    # Implementation for open_closed
    logger.info(f"Executing open_closed")
    return None


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