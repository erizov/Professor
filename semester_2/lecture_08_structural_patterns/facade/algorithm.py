#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facade Design Pattern.

Provides a unified interface to a set of interfaces in a subsystem.
Facade defines a higher-level interface that makes the subsystem easier to use.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Complex Subsystem Classes
class CPU:
    """CPU subsystem."""
    
    def freeze(self) -> None:
        print("CPU: Freezing...")
    
    def jump(self, position: int) -> None:
        print(f"CPU: Jumping to position {position}")
    
    def execute(self) -> None:
        print("CPU: Executing...")


class Memory:
    """Memory subsystem."""
    
    def load(self, position: int, data: str) -> None:
        print(f"Memory: Loading data '{data}' at position {position}")


class HardDrive:
    """Hard drive subsystem."""
    
    def read(self, lba: int, size: int) -> str:
        print(f"HardDrive: Reading {size} bytes from LBA {lba}")
        return f"Data from LBA {lba}"


# Facade
class ComputerFacade:
    """Computer facade - simplifies subsystem interaction."""
    
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()
        self.BOOT_ADDRESS = 0x7C00
        self.BOOT_SECTOR = 0
        self.SECTOR_SIZE = 512
    
    def start(self) -> None:
        """Start computer - simplified interface."""
        print("Starting computer...")
        self.cpu.freeze()
        boot_data = self.hard_drive.read(self.BOOT_SECTOR, self.SECTOR_SIZE)
        self.memory.load(self.BOOT_ADDRESS, boot_data)
        self.cpu.jump(self.BOOT_ADDRESS)
        self.cpu.execute()
        print("Computer started successfully!")
        print()


# Example 2: Home Theater System
class Amplifier:
    """Amplifier subsystem."""
    
    def on(self) -> None:
        print("Amplifier: ON")
    
    def set_volume(self, level: int) -> None:
        print(f"Amplifier: Volume set to {level}")
    
    def off(self) -> None:
        print("Amplifier: OFF")


class Tuner:
    """Tuner subsystem."""
    
    def on(self) -> None:
        print("Tuner: ON")
    
    def set_frequency(self, freq: float) -> None:
        print(f"Tuner: Frequency set to {freq} MHz")
    
    def off(self) -> None:
        print("Tuner: OFF")


class DVDPlayer:
    """DVD player subsystem."""
    
    def on(self) -> None:
        print("DVD Player: ON")
    
    def play(self, movie: str) -> None:
        print(f"DVD Player: Playing '{movie}'")
    
    def stop(self) -> None:
        print("DVD Player: STOP")
    
    def off(self) -> None:
        print("DVD Player: OFF")


class Projector:
    """Projector subsystem."""
    
    def on(self) -> None:
        print("Projector: ON")
    
    def wide_screen_mode(self) -> None:
        print("Projector: Wide screen mode")
    
    def off(self) -> None:
        print("Projector: OFF")


class HomeTheaterFacade:
    """Home theater facade."""
    
    def __init__(self):
        self.amp = Amplifier()
        self.tuner = Tuner()
        self.dvd = DVDPlayer()
        self.projector = Projector()
    
    def watch_movie(self, movie: str) -> None:
        """Watch movie - simplified interface."""
        print("Get ready to watch a movie...")
        self.projector.on()
        self.projector.wide_screen_mode()
        self.amp.on()
        self.amp.set_volume(5)
        self.dvd.on()
        self.dvd.play(movie)
        print()
    
    def end_movie(self) -> None:
        """End movie - simplified interface."""
        print("Shutting movie theater down...")
        self.dvd.stop()
        self.dvd.off()
        self.amp.off()
        self.projector.off()
        print()


# Example 3: Order Processing
class InventoryService:
    """Inventory service."""
    
    def check_availability(self, product_id: str, quantity: int) -> bool:
        print(f"Inventory: Checking availability of {quantity} x {product_id}")
        return True
    
    def reserve(self, product_id: str, quantity: int) -> None:
        print(f"Inventory: Reserving {quantity} x {product_id}")


class PaymentService:
    """Payment service."""
    
    def process_payment(self, amount: float, method: str) -> bool:
        print(f"Payment: Processing ${amount} via {method}")
        return True


class ShippingService:
    """Shipping service."""
    
    def create_shipment(self, address: str, items: list) -> str:
        print(f"Shipping: Creating shipment to {address}")
        return "SHIP-12345"


class OrderFacade:
    """Order processing facade."""
    
    def __init__(self):
        self.inventory = InventoryService()
        self.payment = PaymentService()
        self.shipping = ShippingService()
    
    def place_order(self, product_id: str, quantity: int, 
                   amount: float, address: str) -> str:
        """Place order - simplified interface."""
        print("Processing order...")
        
        # Check inventory
        if not self.inventory.check_availability(product_id, quantity):
            return None
        
        # Reserve items
        self.inventory.reserve(product_id, quantity)
        
        # Process payment
        if not self.payment.process_payment(amount, "credit_card"):
            return None
        
        # Create shipment
        shipment_id = self.shipping.create_shipment(
            address, 
            [{"product": product_id, "quantity": quantity}]
        )
        
        print("Order placed successfully!")
        return shipment_id


def main() -> None:
    """Demonstration of Facade Pattern."""
    print("=" * 70)
    print("FACADE DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Computer Boot
    print("Example 1: Computer Boot Process")
    print("-" * 70)
    
    computer = ComputerFacade()
    computer.start()
    
    # Example 2: Home Theater
    print("Example 2: Home Theater System")
    print("-" * 70)
    
    theater = HomeTheaterFacade()
    theater.watch_movie("The Matrix")
    theater.end_movie()
    
    # Example 3: Order Processing
    print("Example 3: E-commerce Order Processing")
    print("-" * 70)
    
    order_system = OrderFacade()
    shipment_id = order_system.place_order(
        product_id="LAPTOP-001",
        quantity=1,
        amount=999.99,
        address="123 Main St"
    )
    print(f"Shipment ID: {shipment_id}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Provide a unified interface to a set of interfaces in")
    print("  a subsystem. Facade defines a higher-level interface")
    print("  that makes the subsystem easier to use.")
    print("\nKey Advantages:")
    print("  - Simplifies complex subsystem")
    print("  - Reduces coupling between clients and subsystem")
    print("  - Provides convenient interface")
    print("  - Hides subsystem complexity")
    print("\nKey Disadvantages:")
    print("  - Can become a god object")
    print("  - May limit flexibility")
    print("  - Can hide important functionality")
    print("\nWhen to Use:")
    print("  - Want to provide simple interface to complex subsystem")
    print("  - Want to decouple clients from subsystem")
    print("  - Want to layer subsystems")
    print("  - Need entry point to subsystem")
    print("\nCommon Use Cases:")
    print("  - API wrappers")
    print("  - Library interfaces")
    print("  - System initialization")
    print("  - Complex workflows")
    print("  - Legacy system integration")
    print("=" * 70)


if __name__ == "__main__":
    main()
