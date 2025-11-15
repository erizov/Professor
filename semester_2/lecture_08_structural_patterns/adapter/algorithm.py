#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adapter Design Pattern.

Allows incompatible interfaces to work together by wrapping an object
with an adapter that translates between the two interfaces.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Target Interface (what client expects)
class MediaPlayer(ABC):
    """Target interface for media players."""
    
    @abstractmethod
    def play(self, audio_type: str, filename: str) -> None:
        """Play audio file."""
        pass


# Adaptee (existing incompatible interface)
class AdvancedMediaPlayer(ABC):
    """Advanced media player interface."""
    
    @abstractmethod
    def play_vlc(self, filename: str) -> None:
        """Play VLC file."""
        pass
    
    @abstractmethod
    def play_mp4(self, filename: str) -> None:
        """Play MP4 file."""
        pass


# Concrete Adaptees
class VlcPlayer(AdvancedMediaPlayer):
    """VLC player implementation."""
    
    def play_vlc(self, filename: str) -> None:
        print(f"Playing VLC file: {filename}")
    
    def play_mp4(self, filename: str) -> None:
        pass  # Not supported


class Mp4Player(AdvancedMediaPlayer):
    """MP4 player implementation."""
    
    def play_vlc(self, filename: str) -> None:
        pass  # Not supported
    
    def play_mp4(self, filename: str) -> None:
        print(f"Playing MP4 file: {filename}")


# Adapter (translates between interfaces)
class MediaAdapter(MediaPlayer):
    """Adapter that makes AdvancedMediaPlayer compatible with MediaPlayer."""
    
    def __init__(self, audio_type: str):
        """
        Initialize adapter with appropriate player.
        
        Args:
            audio_type: Type of audio (vlc or mp4)
        """
        if audio_type == "vlc":
            self.advanced_player = VlcPlayer()
        elif audio_type == "mp4":
            self.advanced_player = Mp4Player()
        else:
            raise ValueError(f"Unsupported audio type: {audio_type}")
    
    def play(self, audio_type: str, filename: str) -> None:
        """Play file using advanced player."""
        if audio_type == "vlc":
            self.advanced_player.play_vlc(filename)
        elif audio_type == "mp4":
            self.advanced_player.play_mp4(filename)


# Client (uses target interface)
class AudioPlayer(MediaPlayer):
    """Audio player that uses adapter for advanced formats."""
    
    def play(self, audio_type: str, filename: str) -> None:
        """Play audio file, using adapter for advanced formats."""
        if audio_type == "mp3":
            print(f"Playing MP3 file: {filename}")
        elif audio_type in ["vlc", "mp4"]:
            adapter = MediaAdapter(audio_type)
            adapter.play(audio_type, filename)
        else:
            print(f"Invalid media type: {audio_type}")


# Object Adapter Example (using composition)
class Square:
    """Square class (adaptee)."""
    
    def __init__(self, side: float):
        self.side = side
    
    def get_side(self) -> float:
        return self.side


class Rectangle:
    """Rectangle interface (target)."""
    
    def get_width(self) -> float:
        raise NotImplementedError
    
    def get_height(self) -> float:
        raise NotImplementedError
    
    def get_area(self) -> float:
        return self.get_width() * self.get_height()


class SquareToRectangleAdapter(Rectangle):
    """Adapter that makes Square compatible with Rectangle."""
    
    def __init__(self, square: Square):
        self.square = square
    
    def get_width(self) -> float:
        return self.square.get_side()
    
    def get_height(self) -> float:
        return self.square.get_side()


# Class Adapter Example (using inheritance)
class LegacyPrinter:
    """Legacy printer (adaptee)."""
    
    def print_legacy(self, text: str) -> None:
        print(f"[LEGACY] {text}")


class ModernPrinter:
    """Modern printer interface (target)."""
    
    def print_document(self, content: str) -> None:
        raise NotImplementedError


class PrinterAdapter(ModernPrinter, LegacyPrinter):
    """Class adapter using multiple inheritance."""
    
    def print_document(self, content: str) -> None:
        # Adapt modern interface to legacy
        self.print_legacy(content)


# Third-party API Adapter Example
class ThirdPartyPaymentGateway:
    """Third-party payment gateway (adaptee)."""
    
    def process_payment_third_party(self, amount: float, 
                                    currency: str) -> bool:
        """Process payment using third-party format."""
        print(f"Processing {currency} {amount} via third-party gateway")
        return True


class PaymentProcessor:
    """Our payment processor interface (target)."""
    
    def pay(self, amount: float, currency_code: str) -> bool:
        """Process payment."""
        raise NotImplementedError


class PaymentGatewayAdapter(PaymentProcessor):
    """Adapter for third-party payment gateway."""
    
    def __init__(self):
        self.gateway = ThirdPartyPaymentGateway()
    
    def pay(self, amount: float, currency_code: str) -> bool:
        """Adapt our interface to third-party interface."""
        # Convert currency code to currency name
        currency_map = {
            "USD": "US Dollar",
            "EUR": "Euro",
            "GBP": "British Pound"
        }
        currency = currency_map.get(currency_code, currency_code)
        
        return self.gateway.process_payment_third_party(amount, currency)


def main() -> None:
    """Demonstration of Adapter Pattern."""
    print("=" * 70)
    print("ADAPTER DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Media Player Adapter
    print("Example 1: Media Player Adapter")
    print("-" * 70)
    
    player = AudioPlayer()
    player.play("mp3", "song.mp3")
    player.play("mp4", "video.mp4")
    player.play("vlc", "movie.vlc")
    print()
    
    # Example 2: Object Adapter (Square to Rectangle)
    print("Example 2: Object Adapter (Square to Rectangle)")
    print("-" * 70)
    
    square = Square(5.0)
    rectangle_adapter = SquareToRectangleAdapter(square)
    
    print(f"Square side: {square.get_side()}")
    print(f"Rectangle width: {rectangle_adapter.get_width()}")
    print(f"Rectangle height: {rectangle_adapter.get_height()}")
    print(f"Rectangle area: {rectangle_adapter.get_area()}")
    print()
    
    # Example 3: Class Adapter (Printer)
    print("Example 3: Class Adapter (Printer)")
    print("-" * 70)
    
    modern_printer = PrinterAdapter()
    modern_printer.print_document("Hello, World!")
    print()
    
    # Example 4: Third-party API Adapter
    print("Example 4: Third-party Payment Gateway Adapter")
    print("-" * 70)
    
    payment_processor = PaymentGatewayAdapter()
    payment_processor.pay(100.0, "USD")
    payment_processor.pay(85.0, "EUR")
    payment_processor.pay(75.0, "GBP")
    print()
    
    # Example 5: Multiple adapters
    print("Example 5: Using Multiple Adapters")
    print("-" * 70)
    
    # Different media types
    media_files = [
        ("mp3", "audio1.mp3"),
        ("mp4", "video1.mp4"),
        ("vlc", "movie1.vlc"),
        ("mp3", "audio2.mp3")
    ]
    
    for media_type, filename in media_files:
        player.play(media_type, filename)
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Convert the interface of a class into another interface")
    print("  clients expect. Adapter lets classes work together that")
    print("  couldn't otherwise because of incompatible interfaces.")
    print("\nKey Advantages:")
    print("  - Allows incompatible interfaces to work together")
    print("  - Reuses existing classes without modification")
    print("  - Single Responsibility (separation of concerns)")
    print("  - Open/Closed Principle (can add new adapters)")
    print("\nKey Disadvantages:")
    print("  - Adds complexity (extra layer)")
    print("  - Can make code harder to understand")
    print("  - Performance overhead (indirection)")
    print("\nWhen to Use:")
    print("  - Integrating third-party libraries")
    print("  - Working with legacy code")
    print("  - Making incompatible interfaces compatible")
    print("  - Wrapping APIs for consistent interface")
    print("\nWhen NOT to Use:")
    print("  - Can modify source code directly")
    print("  - Interfaces are already compatible")
    print("  - Performance is critical")
    print("\nAdapter Types:")
    print("  - Object Adapter: Uses composition (preferred)")
    print("  - Class Adapter: Uses multiple inheritance")
    print("\nCommon Use Cases:")
    print("  - Integrating third-party libraries")
    print("  - Legacy code integration")
    print("  - API wrappers")
    print("  - Data format conversion")
    print("  - Database adapters (ODBC, JDBC)")
    print("  - UI framework adapters")
    print("\nReal-world Examples:")
    print("  - Java: Arrays.asList() adapts array to List")
    print("  - Python: io.TextIOWrapper adapts bytes to text")
    print("  - Database: JDBC adapters for different databases")
    print("  - Payment: Payment gateway adapters")
    print("=" * 70)


if __name__ == "__main__":
    main()
