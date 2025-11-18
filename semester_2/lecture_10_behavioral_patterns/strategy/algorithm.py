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
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Strategy Interface
class SortingStrategy(ABC):
    """Abstract sorting strategy."""
    
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        """Sort the data."""
        
    
    
    """
    Strategy pattern implementation.
    """
    def sort(self):
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
    
    # Example 1: Sorting Strategies
    logger.info("Example 1: Sorting Strategies")
    logger.info("-" * 70)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    logger.info(f"Original data: {data}")
    
    sorter = Sorter()
    
    # Use different strategies
    strategies = [
        BubbleSortStrategy(),
        QuickSortStrategy(),
        MergeSortStrategy()
    ]
    
    for strategy in strategies:
        sorter.set_strategy(strategy)
        sorted_data = sorter.sort(data)
        logger.info(f"{strategy.get_name()}: {sorted_data}")
    logger.info()
    
    # Example 2: Payment Strategies
    logger.info("Example 2: Payment Strategies")
    logger.info("-" * 70)
    
    cart = ShoppingCart()
    cart.add_item("Laptop", 999.99)
    cart.add_item("Mouse", 29.99)
    cart.add_item("Keyboard", 79.99)
    
    # Try different payment methods
    payment_methods = [
        CreditCardPayment("1234567890123456", "123"),
        PayPalPayment("user@example.com"),
        CryptocurrencyPayment("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    ]
    
    for payment in payment_methods:
        cart.set_payment_strategy(payment)
        cart.checkout()
        logger.info()
    
    # Example 3: Compression Strategies
    logger.info("Example 3: Compression Strategies")
    logger.info("-" * 70)
    
    content = "This is a test file with some content. " * 10
    logger.info(f"Original size: {len(content)} bytes")
    
    compression_strategies = [
        ZipCompression(),
        GzipCompression()
    ]
    
    for strategy in compression_strategies:
        compressor = FileCompressor(strategy)
        compressed = compressor.compress_file(content)
        decompressed = compressor.decompress_file(compressed)
        
        logger.info(f"  Compressed size: {len(compressed)} bytes")
        logger.info(f"  Compression ratio: {len(compressed)/len(content)*100:.1f}%")
        logger.info(f"  Decompressed matches original: {decompressed == content}")
        logger.info()
    
    # Example 4: Runtime Strategy Selection
    logger.info("Example 4: Runtime Strategy Selection")
    logger.info("-" * 70)
    
    def select_sorting_strategy(data_size: int) -> SortingStrategy:
        """Select strategy based on data size."""
        if data_size < 10:
            return BubbleSortStrategy()
        elif data_size < 100:
            return QuickSortStrategy()
        else:
            return MergeSortStrategy()
    
    test_data_sizes = [5, 50, 500]
    for size in test_data_sizes:
        test_data = list(range(size, 0, -1))  # Reverse order
        strategy = select_sorting_strategy(size)
        sorter.set_strategy(strategy)
        
        sorted_result = sorter.sort(test_data)
        logger.info(f"Data size: {size}, Strategy: {strategy.get_name()}")
        logger.info(f"  First 5: {sorted_result[:5]}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Define a family of algorithms, encapsulate each one,")
    logger.info("  and make them interchangeable. Strategy lets the")
    logger.info("  algorithm vary independently from clients.")
    logger.info("\nKey Advantages:")
    logger.debug("  - Algorithms can be swapped at runtime")
    logger.info("  - Eliminates conditional statements for algorithm selection")
    logger.info("  - Open/Closed Principle (easy to add new strategies)")
    logger.info("  - Single Responsibility (each strategy is independent)")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Clients must be aware of different strategies")
    logger.info("  - Increased number of classes")
    logger.info("  - Communication overhead between context and strategy")
    logger.info("\nWhen to Use:")
    logger.info("  - Multiple ways to perform a task")
    logger.info("  - Want to avoid conditional statements for algorithm selection")
    logger.info("  - Algorithms should be interchangeable")
    logger.info("  - Hide algorithm implementation from clients")
    logger.info("\nWhen NOT to Use:")
    logger.info("  - Only one way to perform task")
    logger.info("  - Algorithms are not interchangeable")
    logger.info("  - Strategy selection is compile-time only")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Sorting algorithms (as shown)")
    logger.info("  - Payment processing (credit card, PayPal, etc.)")
    logger.info("  - Compression algorithms (ZIP, GZIP, etc.)")
    logger.info("  - Validation strategies")
    logger.info("  - Caching strategies (LRU, LFU, etc.)")
    logger.info("  - Rendering strategies (HTML, PDF, etc.)")
    logger.info("\nComparison with Other Patterns:")
    logger.info("  - Strategy vs State: Strategy is about algorithms,")
    logger.info("    State is about object behavior")
    logger.info("  - Strategy vs Template Method: Strategy uses composition,")
    logger.info("    Template Method uses inheritance")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()