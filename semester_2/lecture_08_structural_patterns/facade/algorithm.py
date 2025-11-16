#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facade Design Pattern.

Provides a unified interface to a set of interfaces in a subsystem.
Facade defines a higher-level interface that makes the subsystem easier to use.
"""

import sys
from pathlib import Path
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Complex Subsystem Classes
class CPU:
    """CPU subsystem."""
    
    def freeze(self) -> None:
        logger.info("CPU: Freezing...")
    
    def jump(self, position: int) -> None:
        logger.info(f"CPU: Jumping to position {position}")
    
    def execute(self) -> None:
        logger.info("CPU: Executing...")


class Memory:
    """Memory subsystem."""
    
    def load(self, position: int, data: str) -> None:
        logger.info(f"Memory: Loading data '{data}' at position {position}")


class HardDrive:
    """Hard drive subsystem."""
    
    def read(self, lba: int, size: int) -> str:
        logger.info(f"HardDrive: Reading {size} bytes from LBA {lba}")
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
        logger.info("Starting computer...")
        self.cpu.freeze()
        boot_data = self.hard_drive.read(self.BOOT_SECTOR, self.SECTOR_SIZE)
        self.memory.load(self.BOOT_ADDRESS, boot_data)
        self.cpu.jump(self.BOOT_ADDRESS)
        self.cpu.execute()
        logger.info("Computer started successfully!")
        logger.info()


# Example 2: Home Theater System
class Amplifier:
    """Amplifier subsystem."""
    
    def on(self) -> None:
        logger.info("Amplifier: ON")
    
    def set_volume(self, level: int) -> None:
        logger.info(f"Amplifier: Volume set to {level}")
    
    def off(self) -> None:
        logger.info("Amplifier: OFF")


class Tuner:
    """Tuner subsystem."""
    
    def on(self) -> None:
        logger.info("Tuner: ON")
    
    def set_frequency(self, freq: float) -> None:
        logger.info(f"Tuner: Frequency set to {freq} MHz")
    
    def off(self) -> None:
        logger.info("Tuner: OFF")


class DVDPlayer:
    """DVD player subsystem."""
    
    def on(self) -> None:
        logger.info("DVD Player: ON")
    
    def play(self, movie: str) -> None:
        logger.info(f"DVD Player: Playing '{movie}'")
    
    def stop(self) -> None:
        logger.info("DVD Player: STOP")
    
    def off(self) -> None:
        logger.info("DVD Player: OFF")


class Projector:
    """Projector subsystem."""
    
    def on(self) -> None:
        logger.info("Projector: ON")
    
    def wide_screen_mode(self) -> None:
        logger.info("Projector: Wide screen mode")
    
    def off(self) -> None:
        logger.info("Projector: OFF")


class HomeTheaterFacade:
    """Home theater facade."""
    
    def __init__(self):
        self.amp = Amplifier()
        self.tuner = Tuner()
        self.dvd = DVDPlayer()
        self.projector = Projector()
    
    def watch_movie(self, movie: str) -> None:
        """Watch movie - simplified interface."""
        logger.info("Get ready to watch a movie...")
        self.projector.on()
        self.projector.wide_screen_mode()
        self.amp.on()
        self.amp.set_volume(5)
        self.dvd.on()
        self.dvd.play(movie)
        logger.info()
    
    def end_movie(self) -> None:
        """End movie - simplified interface."""
        logger.info("Shutting movie theater down...")
        self.dvd.stop()
        self.dvd.off()
        self.amp.off()
        self.projector.off()
        logger.info()


# Example 3: Order Processing
class InventoryService:
    """Inventory service."""
    
    def check_availability(self, product_id: str, quantity: int) -> bool:
        logger.info(f"Inventory: Checking availability of {quantity} x {product_id}")
        return True
    
    def reserve(self, product_id: str, quantity: int) -> None:
        logger.info(f"Inventory: Reserving {quantity} x {product_id}")


class PaymentService:
    """Payment service."""
    
    def process_payment(self, amount: float, method: str) -> bool:
        logger.info(f"Payment: Processing ${amount} via {method}")
        return True


class ShippingService:
    """Shipping service."""
    
    def create_shipment(self, address: str, items: list) -> str:
        logger.info(f"Shipping: Creating shipment to {address}")
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
        logger.info("Processing order...")
        
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
        
        logger.info("Order placed successfully!")
        return shipment_id


def main() -> None:
    """Demonstration of Facade Pattern."""
    logger.info("=" * 70)
    logger.info("FACADE DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Computer Boot
    logger.info("Example 1: Computer Boot Process")
    logger.info("-" * 70)
    
    computer = ComputerFacade()
    computer.start()
    
    # Example 2: Home Theater
    logger.info("Example 2: Home Theater System")
    logger.info("-" * 70)
    
    theater = HomeTheaterFacade()
    theater.watch_movie("The Matrix")
    theater.end_movie()
    
    # Example 3: Order Processing
    logger.info("Example 3: E-commerce Order Processing")
    logger.info("-" * 70)
    
    order_system = OrderFacade()
    shipment_id = order_system.place_order(
        product_id="LAPTOP-001",
        quantity=1,
        amount=999.99,
        address="123 Main St"
    )
    logger.info(f"Shipment ID: {shipment_id}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Provide a unified interface to a set of interfaces in")
    logger.info("  a subsystem. Facade defines a higher-level interface")
    logger.info("  that makes the subsystem easier to use.")
    logger.info("\nKey Advantages:")
    logger.info("  - Simplifies complex subsystem")
    logger.info("  - Reduces coupling between clients and subsystem")
    logger.info("  - Provides convenient interface")
    logger.info("  - Hides subsystem complexity")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Can become a god object")
    logger.info("  - May limit flexibility")
    logger.info("  - Can hide important functionality")
    logger.info("\nWhen to Use:")
    logger.info("  - Want to provide simple interface to complex subsystem")
    logger.info("  - Want to decouple clients from subsystem")
    logger.info("  - Want to layer subsystems")
    logger.info("  - Need entry point to subsystem")
    logger.info("\nCommon Use Cases:")
    logger.info("  - API wrappers")
    logger.info("  - Library interfaces")
    logger.info("  - System initialization")
    logger.info("  - Complex workflows")
    logger.info("  - Legacy system integration")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()