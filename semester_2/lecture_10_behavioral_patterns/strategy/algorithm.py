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


# Strategy Interface
class SortingStrategy(ABC):
    """Abstract sorting strategy."""
    
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        """Sort the data."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get strategy name."""
        pass


# Concrete Strategies
class BubbleSortStrategy(SortingStrategy):
    """Bubble sort strategy."""
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort using bubble sort."""
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    def get_name(self) -> str:
        return "Bubble Sort"


class QuickSortStrategy(SortingStrategy):
    """Quick sort strategy."""
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort using quick sort."""
        if len(data) <= 1:
            return data.copy()
        
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        
        return (self.sort(left) + middle + self.sort(right))
    
    def get_name(self) -> str:
        return "Quick Sort"


class MergeSortStrategy(SortingStrategy):
    """Merge sort strategy."""
    
    def sort(self, data: List[int]) -> List[int]:
        """Sort using merge sort."""
        if len(data) <= 1:
            return data.copy()
        
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
    
    def get_name(self) -> str:
        return "Merge Sort"


# Context
class Sorter:
    """Context that uses a sorting strategy."""
    
    def __init__(self, strategy: SortingStrategy = None):
        """
        Initialize sorter with optional strategy.
        
        Args:
            strategy: Sorting strategy to use
        """
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortingStrategy) -> None:
        """Set the sorting strategy."""
        self._strategy = strategy
    
    def sort(self, data: List[int]) -> List[int]:
        """
        Sort data using current strategy.
        
        Args:
            data: List to sort
            
        Returns:
            Sorted list
        """
        if self._strategy is None:
            raise ValueError("No sorting strategy set")
        return self._strategy.sort(data)


# Payment Strategy Example
class PaymentStrategy(ABC):
    """Abstract payment strategy."""
    
    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Process payment."""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Get payment method name."""
        pass


class CreditCardPayment(PaymentStrategy):
    """Credit card payment strategy."""
    
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv
    
    def pay(self, amount: float) -> bool:
        """Process credit card payment."""
        print(f"Processing ${amount:.2f} payment via Credit Card")
        print(f"Card: ****{self.card_number[-4:]}")
        # Simulate payment processing
        return True
    
    def get_name(self) -> str:
        return "Credit Card"


class PayPalPayment(PaymentStrategy):
    """PayPal payment strategy."""
    
    def __init__(self, email: str):
        self.email = email
    
    def pay(self, amount: float) -> bool:
        """Process PayPal payment."""
        print(f"Processing ${amount:.2f} payment via PayPal")
        print(f"Email: {self.email}")
        # Simulate payment processing
        return True
    
    def get_name(self) -> str:
        return "PayPal"


class CryptocurrencyPayment(PaymentStrategy):
    """Cryptocurrency payment strategy."""
    
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
    
    def pay(self, amount: float) -> bool:
        """Process cryptocurrency payment."""
        print(f"Processing ${amount:.2f} payment via Cryptocurrency")
        print(f"Wallet: {self.wallet_address[:10]}...")
        # Simulate payment processing
        return True
    
    def get_name(self) -> str:
        return "Cryptocurrency"


class ShoppingCart:
    """Shopping cart that uses payment strategy."""
    
    def __init__(self):
        self.items: List[tuple] = []  # (name, price)
        self.payment_strategy: PaymentStrategy = None
    
    def add_item(self, name: str, price: float) -> None:
        """Add item to cart."""
        self.items.append((name, price))
    
    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        """Set payment strategy."""
        self.payment_strategy = strategy
    
    def checkout(self) -> bool:
        """Checkout using payment strategy."""
        if not self.items:
            print("Cart is empty!")
            return False
        
        if self.payment_strategy is None:
            print("No payment method selected!")
            return False
        
        total = sum(price for _, price in self.items)
        print(f"\nTotal: ${total:.2f}")
        print(f"Payment method: {self.payment_strategy.get_name()}")
        
        return self.payment_strategy.pay(total)


# Compression Strategy Example
class CompressionStrategy(ABC):
    """Abstract compression strategy."""
    
    @abstractmethod
    def compress(self, data: str) -> bytes:
        """Compress data."""
        pass
    
    @abstractmethod
    def decompress(self, data: bytes) -> str:
        """Decompress data."""
        pass


class ZipCompression(CompressionStrategy):
    """ZIP compression strategy."""
    
    def compress(self, data: str) -> bytes:
        """Compress using ZIP."""
        import zlib
        return zlib.compress(data.encode())
    
    def decompress(self, data: bytes) -> str:
        """Decompress ZIP data."""
        import zlib
        return zlib.decompress(data).decode()
    
    def __str__(self) -> str:
        return "ZIP"


class GzipCompression(CompressionStrategy):
    """GZIP compression strategy."""
    
    def compress(self, data: str) -> bytes:
        """Compress using GZIP."""
        import gzip
        return gzip.compress(data.encode())
    
    def decompress(self, data: bytes) -> str:
        """Decompress GZIP data."""
        import gzip
        return gzip.decompress(data).decode()
    
    def __str__(self) -> str:
        return "GZIP"


class FileCompressor:
    """File compressor using compression strategy."""
    
    def __init__(self, strategy: CompressionStrategy):
        self.strategy = strategy
    
    def compress_file(self, content: str) -> bytes:
        """Compress file content."""
        print(f"Compressing using {self.strategy}...")
        return self.strategy.compress(content)
    
    def decompress_file(self, data: bytes) -> str:
        """Decompress file data."""
        print(f"Decompressing using {self.strategy}...")
        return self.strategy.decompress(data)


def main() -> None:
    """Demonstration of Strategy Pattern."""
    print("=" * 70)
    print("STRATEGY DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Sorting Strategies
    print("Example 1: Sorting Strategies")
    print("-" * 70)
    
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original data: {data}")
    
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
        print(f"{strategy.get_name()}: {sorted_data}")
    print()
    
    # Example 2: Payment Strategies
    print("Example 2: Payment Strategies")
    print("-" * 70)
    
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
        print()
    
    # Example 3: Compression Strategies
    print("Example 3: Compression Strategies")
    print("-" * 70)
    
    content = "This is a test file with some content. " * 10
    print(f"Original size: {len(content)} bytes")
    
    compression_strategies = [
        ZipCompression(),
        GzipCompression()
    ]
    
    for strategy in compression_strategies:
        compressor = FileCompressor(strategy)
        compressed = compressor.compress_file(content)
        decompressed = compressor.decompress_file(compressed)
        
        print(f"  Compressed size: {len(compressed)} bytes")
        print(f"  Compression ratio: {len(compressed)/len(content)*100:.1f}%")
        print(f"  Decompressed matches original: {decompressed == content}")
        print()
    
    # Example 4: Runtime Strategy Selection
    print("Example 4: Runtime Strategy Selection")
    print("-" * 70)
    
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
        print(f"Data size: {size}, Strategy: {strategy.get_name()}")
        print(f"  First 5: {sorted_result[:5]}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Define a family of algorithms, encapsulate each one,")
    print("  and make them interchangeable. Strategy lets the")
    print("  algorithm vary independently from clients.")
    print("\nKey Advantages:")
    print("  - Algorithms can be swapped at runtime")
    print("  - Eliminates conditional statements for algorithm selection")
    print("  - Open/Closed Principle (easy to add new strategies)")
    print("  - Single Responsibility (each strategy is independent)")
    print("\nKey Disadvantages:")
    print("  - Clients must be aware of different strategies")
    print("  - Increased number of classes")
    print("  - Communication overhead between context and strategy")
    print("\nWhen to Use:")
    print("  - Multiple ways to perform a task")
    print("  - Want to avoid conditional statements for algorithm selection")
    print("  - Algorithms should be interchangeable")
    print("  - Hide algorithm implementation from clients")
    print("\nWhen NOT to Use:")
    print("  - Only one way to perform task")
    print("  - Algorithms are not interchangeable")
    print("  - Strategy selection is compile-time only")
    print("\nCommon Use Cases:")
    print("  - Sorting algorithms (as shown)")
    print("  - Payment processing (credit card, PayPal, etc.)")
    print("  - Compression algorithms (ZIP, GZIP, etc.)")
    print("  - Validation strategies")
    print("  - Caching strategies (LRU, LFU, etc.)")
    print("  - Rendering strategies (HTML, PDF, etc.)")
    print("\nComparison with Other Patterns:")
    print("  - Strategy vs State: Strategy is about algorithms,")
    print("    State is about object behavior")
    print("  - Strategy vs Template Method: Strategy uses composition,")
    print("    Template Method uses inheritance")
    print("=" * 70)


if __name__ == "__main__":
    main()

