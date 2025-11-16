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
from framework.logging_utils import get_logger
logger = get_logger(__name__)

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
        logger.info(f"Writing to {self.filename}: {data}")
        # In real implementation: with open(self.filename, 'w') as f: f.write(data)
    
    def read_data(self) -> str:
        logger.info(f"Reading from {self.filename}")
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
        logger.info(f"  Encrypting data...")
        self._source.write_data(encrypted)
    
    def read_data(self) -> str:
        encrypted = self._source.read_data()
        logger.info(f"  Decrypting data...")
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
        logger.info(f"  Compressing data...")
        self._source.write_data(compressed)
    
    def read_data(self) -> str:
        compressed = self._source.read_data()
        logger.info(f"  Decompressing data...")
        return self._decompress(compressed)
    
    def _compress(self, data: str) -> str:
        # Simple compression (simulated)
        return f"[COMPRESSED]{data[:len(data)//2]}"
    
    def _decompress(self, data: str) -> str:
        # Simple decompression (simulated)
        return data.replace("[COMPRESSED]", "").replace("", "x")[:20]


def main() -> None:
    """Demonstration of Decorator Pattern."""
    logger.info("=" * 70)
    logger.info("DECORATOR DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Coffee Decorator
    logger.info("Example 1: Coffee Ordering System")
    logger.info("-" * 70)
    
    # Simple coffee
    coffee = SimpleCoffee()
    logger.info(f"{coffee.get_description()}: ${coffee.get_cost():.2f}")
    
    # Coffee with milk
    coffee_with_milk = MilkDecorator(SimpleCoffee())
    logger.info(f"{coffee_with_milk.get_description()}: "
          f"${coffee_with_milk.get_cost():.2f}")
    
    # Coffee with multiple additions
    fancy_coffee = WhippedCreamDecorator(
        CaramelDecorator(
            SugarDecorator(
                MilkDecorator(SimpleCoffee())
            )
        )
    )
    logger.info(f"{fancy_coffee.get_description()}: "
          f"${fancy_coffee.get_cost():.2f}")
    logger.info()
    
    # Example 2: Text Formatting
    logger.info("Example 2: Text Formatting")
    logger.info("-" * 70)
    
    text = "Hello, World!"
    
    plain = PlainText()
    logger.info(f"Plain: {plain.process(text)}")
    
    bold = BoldDecorator(PlainText())
    logger.info(f"Bold: {bold.process(text)}")
    
    bold_italic = ItalicDecorator(BoldDecorator(PlainText()))
    logger.info(f"Bold + Italic: {bold_italic.process(text)}")
    
    formatted = ColorDecorator(
        UnderlineDecorator(
            BoldDecorator(PlainText())
        ),
        "red"
    )
    logger.info(f"Red + Underline + Bold: {formatted.process(text)}")
    logger.info()
    
    # Example 3: File I/O with Decorators
    logger.info("Example 3: File I/O with Encryption and Compression")
    logger.info("-" * 70)
    
    # Plain file
    file = FileDataSource("data.txt")
    file.write_data("Sensitive information")
    logger.info(f"Read: {file.read_data()}")
    logger.info()
    
    # Encrypted file
    encrypted_file = EncryptionDecorator(FileDataSource("encrypted.txt"))
    encrypted_file.write_data("Sensitive information")
    logger.info(f"Read: {encrypted_file.read_data()}")
    logger.info()
    
    # Compressed and encrypted file
    secure_file = CompressionDecorator(
        EncryptionDecorator(FileDataSource("secure.txt"))
    )
    secure_file.write_data("Sensitive information")
    logger.info(f"Read: {secure_file.read_data()}")
    logger.info()
    
    # Example 4: Dynamic Composition
    logger.info("Example 4: Dynamic Decorator Composition")
    logger.info("-" * 70)
    
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
        logger.info(f"Order {order}: {custom.get_description()} "
              f"(${custom.get_cost():.2f})")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Attach additional responsibilities to an object dynamically.")
    logger.info("  Decorators provide a flexible alternative to subclassing")
    logger.info("  for extending functionality.")
    logger.info("\nKey Advantages:")
    logger.info("  - Add behavior without modifying existing code")
    logger.info("  - Compose behaviors dynamically")
    logger.info("  - Single Responsibility Principle")
    logger.info("  - Open/Closed Principle")
    logger.info("  - More flexible than inheritance")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Can result in many small objects")
    logger.info("  - Hard to debug (many layers)")
    logger.info("  - Order of decorators matters")
    logger.info("  - Can be overused (complexity)")
    logger.info("\nWhen to Use:")
    logger.info("  - Add responsibilities to objects dynamically")
    logger.info("  - When subclassing is impractical")
    logger.info("  - When you need to add/remove features at runtime")
    logger.info("  - When you want to avoid feature explosion in classes")
    logger.info("\nWhen NOT to Use:")
    logger.info("  - Simple additions (use inheritance)")
    logger.info("  - When decorator order doesn't matter")
    logger.info("  - When performance is critical (overhead)")
    logger.info("\nCommon Use Cases:")
    logger.info("  - I/O streams (Java, Python)")
    logger.info("  - GUI components (borders, scrollbars)")
    logger.info("  - Web frameworks (middleware)")
    logger.info("  - Text formatting")
    logger.info("  - Data processing pipelines")
    logger.info("  - Caching, logging, validation")
    logger.info("\nComparison with Other Patterns:")
    logger.info("  - Decorator vs Adapter: Decorator adds behavior,")
    logger.info("    Adapter changes interface")
    logger.info("  - Decorator vs Strategy: Decorator composes,")
    logger.info("    Strategy replaces algorithm")
    logger.info("  - Decorator vs Chain of Responsibility:")
    logger.info("    Decorator composes, Chain passes request")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()