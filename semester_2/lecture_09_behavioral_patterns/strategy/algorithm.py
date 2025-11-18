#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Strategy Design Pattern.

Defines a family of algorithms, encapsulates each one, and makes them
interchangeable. Strategy lets the algorithm vary independently from
clients that use it.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


# Strategy Interface
class PaymentStrategy(ABC):
    """Abstract payment strategy."""
    
    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Process payment."""
        
    
    
    """
    Strategy pattern implementation.
    """
    def pay(self):
        pass
    
    def execute(self):
        """Execute pattern logic."""
        pass


def main() -> None:
    """Demonstration of Strategy Pattern."""
    logger.info("=" * 70)
    logger.info("STRATEGY DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Payment Strategy
    logger.info("Example 1: Payment Strategy")
    logger.info("-" * 70)
    
    processor = PaymentProcessor()
    
    # Use credit card
    processor.set_strategy(CreditCardStrategy("1234567890123456", "123"))
    processor.process_payment(100.0)
    logger.info()
    
    # Switch to PayPal
    processor.set_strategy(PayPalStrategy("user@paypal.com"))
    processor.process_payment(50.0)
    logger.info()
    
    # Switch to cryptocurrency
    processor.set_strategy(
        CryptocurrencyStrategy("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    )
    processor.process_payment(25.0)
    logger.info()
    
    # Example 2: Sorting Strategy
    logger.info("Example 2: Sorting Strategy")
    logger.info("-" * 70)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    logger.info(f"Original data: {data}")
    
    # Use quick sort
    sorter = Sorter(QuickSortStrategy())
    sorted_data = sorter.sort_data(data.copy())
    logger.info(f"Quick sorted: {sorted_data}")
    
    # Switch to merge sort
    sorter.set_strategy(MergeSortStrategy())
    sorted_data = sorter.sort_data(data.copy())
    logger.info(f"Merge sorted: {sorted_data}")
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Strategy")
    
    large_data = list(range(1000, 0, -1))
    
    def quick_sort_operation():
        sorter = Sorter(QuickSortStrategy())
        return sorter.sort_data(large_data.copy())
    
    def merge_sort_operation():
        sorter = Sorter(MergeSortStrategy())
        return sorter.sort_data(large_data.copy())
    
    result1, metrics1 = timer.measure(quick_sort_operation)
    logger.info(f"Quick Sort: {metrics1['execution_time_ms']:.3f} ms")
    
    result2, metrics2 = timer.measure(merge_sort_operation)
    logger.info(f"Merge Sort: {metrics2['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Define a family of algorithms, encapsulate each one, and")
    logger.info("  make them interchangeable. Strategy lets the algorithm")
    logger.info("  vary independently from clients that use it.")
    logger.info("\nKey Advantages:")
    logger.debug("  - Algorithms can be swapped at runtime")
    logger.info("  - Eliminates conditional statements")
    logger.info("  - Open/Closed Principle")
    logger.info("  - Easy to add new strategies")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Clients must know about strategies")
    logger.info("  - Increased number of classes")
    logger.info("  - Communication overhead")
    logger.info("\nWhen to Use:")
    logger.info("  - Multiple ways to perform a task")
    logger.info("  - Want to avoid conditional statements")
    logger.info("  - Algorithms should be interchangeable")
    logger.info("  - Need runtime algorithm selection")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Payment processing")
    logger.info("  - Sorting algorithms")
    logger.info("  - Compression algorithms")
    logger.info("  - Validation strategies")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()