#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decorator Design Pattern.

Allows behavior to be added to individual objects dynamically without
affecting the behavior of other objects from the same class.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Component Interface
class Coffee(ABC):
    """Abstract coffee interface."""
    
    @abstractmethod
    def get_description(self) -> str:
        """Get coffee description."""
        pass
    
    @abstractmethod
    def get_cost(self) -> float:
        """Get coffee cost."""
        pass


# Concrete Component
class SimpleCoffee(Coffee):
    """Simple coffee without any additions."""
    
    def get_description(self) -> str:
        return "Simple Coffee"
    
    def get_cost(self) -> float:
        return 2.0


# Decorator Base Class
class CoffeeDecorator(Coffee):
    """Base decorator class."""
    
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def get_description(self) -> str:
        return self._coffee.get_description()
    
    def get_cost(self) -> float:
        return self._coffee.get_cost()


# Concrete Decorators
class MilkDecorator(CoffeeDecorator):
    """Adds milk to coffee."""
    
    def get_description(self) -> str:
        return self._coffee.get_description() + ", Milk"
    
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.5


class SugarDecorator(CoffeeDecorator):
    """Adds sugar to coffee."""
    
    def get_description(self) -> str:
        return self._coffee.get_description() + ", Sugar"
    
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.2


class WhippedCreamDecorator(CoffeeDecorator):
    """Adds whipped cream to coffee."""
    
    def get_description(self) -> str:
        return self._coffee.get_description() + ", Whipped Cream"
    
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.7


class CaramelDecorator(CoffeeDecorator):
    """Adds caramel to coffee."""
    
    def get_description(self) -> str:
        return self._coffee.get_description() + ", Caramel"
    
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 0.6


# Text Processing Example
class TextProcessor(ABC):
    """Abstract text processor."""
    
    @abstractmethod
    def process(self, text: str) -> str:
        """Process text."""
        pass


class PlainText(TextProcessor):
    """Plain text processor."""
    
    def process(self, text: str) -> str:
        return text


class TextDecorator(TextProcessor):
    """Base text decorator."""
    
    def __init__(self, processor: TextProcessor):
        self._processor = processor
    
    def process(self, text: str) -> str:
        return self._processor.process(text)


class BoldDecorator(TextDecorator):
    """Makes text bold."""
    
    def process(self, text: str) -> str:
        return f"<b>{self._processor.process(text)}</b>"


class ItalicDecorator(TextDecorator):
    """Makes text italic."""
    
    def process(self, text: str) -> str:
        return f"<i>{self._processor.process(text)}</i>"


class UnderlineDecorator(TextDecorator):
    """Underlines text."""
    
    def process(self, text: str) -> str:
        return f"<u>{self._processor.process(text)}</u>"


class ColorDecorator(TextDecorator):
    """Adds color to text."""
    
    def __init__(self, processor: TextProcessor, color: str):
        super().__init__(processor)
        self.color = color
    
    def process(self, text: str) -> str:
        return f'<span style="color:{self.color}">' \
               f'{self._processor.process(text)}</span>'


# File I/O Example
class DataSource(ABC):
    """Abstract data source."""
    
    @abstractmethod
    def write_data(self, data: str) -> None:
        """Write data."""
        pass
    
    @abstractmethod
    def read_data(self) -> str:
        """Read data."""
        pass


class FileDataSource(DataSource):
    """File data source."""
    
    def __init__(self, filename: str):
        self.filename = filename
    
    def write_data(self, data: str) -> None:
        print(f"Writing to {self.filename}: {data}")
        # In real implementation: with open(self.filename, 'w') as f: f.write(data)
    
    def read_data(self) -> str:
        print(f"Reading from {self.filename}")
        return "data from file"  # In real: return open(self.filename).read()


class DataSourceDecorator(DataSource):
    """Base data source decorator."""
    
    def __init__(self, source: DataSource):
        self._source = source
    
    def write_data(self, data: str) -> None:
        self._source.write_data(data)
    
    def read_data(self) -> str:
        return self._source.read_data()


class EncryptionDecorator(DataSourceDecorator):
    """Encrypts data."""
    
    def write_data(self, data: str) -> None:
        encrypted = self._encrypt(data)
        print(f"  Encrypting data...")
        self._source.write_data(encrypted)
    
    def read_data(self) -> str:
        encrypted = self._source.read_data()
        print(f"  Decrypting data...")
        return self._decrypt(encrypted)
    
    def _encrypt(self, data: str) -> str:
        # Simple encryption (reverse + shift)
        return ''.join(chr(ord(c) + 1) for c in reversed(data))
    
    def _decrypt(self, data: str) -> str:
        # Simple decryption
        return ''.join(chr(ord(c) - 1) for c in reversed(data))


class CompressionDecorator(DataSourceDecorator):
    """Compresses data."""
    
    def write_data(self, data: str) -> None:
        compressed = self._compress(data)
        print(f"  Compressing data...")
        self._source.write_data(compressed)
    
    def read_data(self) -> str:
        compressed = self._source.read_data()
        print(f"  Decompressing data...")
        return self._decompress(compressed)
    
    def _compress(self, data: str) -> str:
        # Simple compression (simulated)
        return f"[COMPRESSED]{data[:len(data)//2]}"
    
    def _decompress(self, data: str) -> str:
        # Simple decompression (simulated)
        return data.replace("[COMPRESSED]", "").replace("", "x")[:20]


def main() -> None:
    """Demonstration of Decorator Pattern."""
    print("=" * 70)
    print("DECORATOR DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Coffee Decorator
    print("Example 1: Coffee Ordering System")
    print("-" * 70)
    
    # Simple coffee
    coffee = SimpleCoffee()
    print(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")
    
    # Coffee with milk
    coffee_with_milk = MilkDecorator(SimpleCoffee())
    print(f"{coffee_with_milk.get_description()}: "
          f"${coffee_with_milk.get_cost():.2f}")
    
    # Coffee with multiple additions
    fancy_coffee = WhippedCreamDecorator(
        CaramelDecorator(
            SugarDecorator(
                MilkDecorator(SimpleCoffee())
            )
        )
    )
    print(f"{fancy_coffee.get_description()}: "
          f"${fancy_coffee.get_cost():.2f}")
    print()
    
    # Example 2: Text Formatting
    print("Example 2: Text Formatting")
    print("-" * 70)
    
    text = "Hello, World!"
    
    plain = PlainText()
    print(f"Plain: {plain.process(text)}")
    
    bold = BoldDecorator(PlainText())
    print(f"Bold: {bold.process(text)}")
    
    bold_italic = ItalicDecorator(BoldDecorator(PlainText()))
    print(f"Bold + Italic: {bold_italic.process(text)}")
    
    formatted = ColorDecorator(
        UnderlineDecorator(
            BoldDecorator(PlainText())
        ),
        "red"
    )
    print(f"Red + Underline + Bold: {formatted.process(text)}")
    print()
    
    # Example 3: File I/O with Decorators
    print("Example 3: File I/O with Encryption and Compression")
    print("-" * 70)
    
    # Plain file
    file = FileDataSource("data.txt")
    file.write_data("Sensitive information")
    print(f"Read: {file.read_data()}")
    print()
    
    # Encrypted file
    encrypted_file = EncryptionDecorator(FileDataSource("encrypted.txt"))
    encrypted_file.write_data("Sensitive information")
    print(f"Read: {encrypted_file.read_data()}")
    print()
    
    # Compressed and encrypted file
    secure_file = CompressionDecorator(
        EncryptionDecorator(FileDataSource("secure.txt"))
    )
    secure_file.write_data("Sensitive information")
    print(f"Read: {secure_file.read_data()}")
    print()
    
    # Example 4: Dynamic Composition
    print("Example 4: Dynamic Decorator Composition")
    print("-" * 70)
    
    def create_custom_coffee(additions: list) -> Coffee:
        """Create coffee with specified additions."""
        coffee = SimpleCoffee()
        decorator_map = {
            'milk': MilkDecorator,
            'sugar': SugarDecorator,
            'cream': WhippedCreamDecorator,
            'caramel': CaramelDecorator
        }
        
        for addition in additions:
            if addition in decorator_map:
                coffee = decorator_map[addition](coffee)
        
        return coffee
    
    orders = [
        ['milk', 'sugar'],
        ['cream', 'caramel'],
        ['milk', 'sugar', 'cream', 'caramel']
    ]
    
    for order in orders:
        custom = create_custom_coffee(order)
        print(f"Order {order}: {custom.get_description()} "
              f"(${custom.get_cost():.2f})")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Attach additional responsibilities to an object dynamically.")
    print("  Decorators provide a flexible alternative to subclassing")
    print("  for extending functionality.")
    print("\nKey Advantages:")
    print("  - Add behavior without modifying existing code")
    print("  - Compose behaviors dynamically")
    print("  - Single Responsibility Principle")
    print("  - Open/Closed Principle")
    print("  - More flexible than inheritance")
    print("\nKey Disadvantages:")
    print("  - Can result in many small objects")
    print("  - Hard to debug (many layers)")
    print("  - Order of decorators matters")
    print("  - Can be overused (complexity)")
    print("\nWhen to Use:")
    print("  - Add responsibilities to objects dynamically")
    print("  - When subclassing is impractical")
    print("  - When you need to add/remove features at runtime")
    print("  - When you want to avoid feature explosion in classes")
    print("\nWhen NOT to Use:")
    print("  - Simple additions (use inheritance)")
    print("  - When decorator order doesn't matter")
    print("  - When performance is critical (overhead)")
    print("\nCommon Use Cases:")
    print("  - I/O streams (Java, Python)")
    print("  - GUI components (borders, scrollbars)")
    print("  - Web frameworks (middleware)")
    print("  - Text formatting")
    print("  - Data processing pipelines")
    print("  - Caching, logging, validation")
    print("\nComparison with Other Patterns:")
    print("  - Decorator vs Adapter: Decorator adds behavior,")
    print("    Adapter changes interface")
    print("  - Decorator vs Strategy: Decorator composes,")
    print("    Strategy replaces algorithm")
    print("  - Decorator vs Chain of Responsibility:")
    print("    Decorator composes, Chain passes request")
    print("=" * 70)


if __name__ == "__main__":
    main()
