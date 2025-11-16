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
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get strategy name."""
        pass


# Concrete Strategies
class CreditCardStrategy(PaymentStrategy):
    """Credit card payment strategy."""
    
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv
    
    def pay(self, amount: float) -> bool:
        """Process credit card payment."""
        logger.info(f"Processing ${amount:.2f} payment using Credit Card")
        logger.info(f"Card: ****{self.card_number[-4:]}")
        return True
    
    def get_name(self) -> str:
        return "Credit Card"


class PayPalStrategy(PaymentStrategy):
    """PayPal payment strategy."""
    
    def __init__(self, email: str):
        self.email = email
    
    def pay(self, amount: float) -> bool:
        """Process PayPal payment."""
        logger.info(f"Processing ${amount:.2f} payment using PayPal")
        logger.info(f"Email: {self.email}")
        return True
    
    def get_name(self) -> str:
        return "PayPal"


class CryptocurrencyStrategy(PaymentStrategy):
    """Cryptocurrency payment strategy."""
    
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
    
    def pay(self, amount: float) -> bool:
        """Process cryptocurrency payment."""
        logger.info(f"Processing ${amount:.2f} payment using Cryptocurrency")
        logger.info(f"Wallet: {self.wallet_address[:10]}...")
        return True
    
    def get_name(self) -> str:
        return "Cryptocurrency"


# Context
class PaymentProcessor:
    """Payment processor context."""
    
    def __init__(self, strategy: PaymentStrategy = None):
        self.strategy = strategy
    
    def set_strategy(self, strategy: PaymentStrategy) -> None:
        """Set payment strategy."""
        self.strategy = strategy
    
    def process_payment(self, amount: float) -> bool:
        """Process payment using current strategy."""
        if not self.strategy:
            raise ValueError("No payment strategy set")
        return self.strategy.pay(amount)


# Example 2: Sorting Strategy
class SortingStrategy(ABC):
    """Abstract sorting strategy."""
    
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        """Sort the data."""
        pass


class QuickSortStrategy(SortingStrategy):
    """Quick sort strategy."""
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort using quick sort."""
        if len(data) <= 1:
            return data
        
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        
        return self.sort(left) + middle + self.sort(right)


class MergeSortStrategy(SortingStrategy):
    """Merge sort strategy."""
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort using merge sort."""
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        """Merge two sorted lists."""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result


class Sorter:
    """Sorter context."""
    
    def __init__(self, strategy: SortingStrategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy: SortingStrategy) -> None:
        """Set sorting strategy."""
        self.strategy = strategy
    
    def sort_data(self, data: List[int]) -> List[int]:
        """Sort data using current strategy."""
        return self.strategy.sort(data)


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