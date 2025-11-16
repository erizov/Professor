#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bridge Design Pattern.

Decouples an abstraction from its implementation so that the two can
vary independently.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Implementation Interface
class DrawingAPI(ABC):
    """Drawing API interface (implementation)."""
    
    @abstractmethod
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        """Draw a circle."""
        pass


# Concrete Implementations
class DrawingAPI1(DrawingAPI):
    """First drawing API implementation."""
    
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        logger.info(f"API1.circle at ({x:.2f}, {y:.2f}) radius {radius:.2f}")


class DrawingAPI2(DrawingAPI):
    """Second drawing API implementation."""
    
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        logger.info(f"API2.circle at ({x:.2f}, {y:.2f}) radius {radius:.2f}")


# Abstraction
class Shape(ABC):
    """Shape abstraction."""
    
    def __init__(self, drawing_api: DrawingAPI):
        self.drawing_api = drawing_api
    
    @abstractmethod
    def draw(self) -> None:
        """Draw the shape."""
        pass
    
    @abstractmethod
    def resize_by_percentage(self, pct: float) -> None:
        """Resize shape by percentage."""
        pass


# Refined Abstraction
class CircleShape(Shape):
    """Circle shape."""
    
    def __init__(self, x: float, y: float, radius: float, 
                 drawing_api: DrawingAPI):
        super().__init__(drawing_api)
        self.x = x
        self.y = y
        self.radius = radius
    
    def draw(self) -> None:
        """Draw circle using drawing API."""
        self.drawing_api.draw_circle(self.x, self.y, self.radius)
    
    def resize_by_percentage(self, pct: float) -> None:
        """Resize circle."""
        self.radius *= (1 + pct / 100)


# Example 2: Device and Remote Control
class Device(ABC):
    """Device interface (implementation)."""
    
    @abstractmethod
    def turn_on(self) -> None:
        pass
    
    @abstractmethod
    def turn_off(self) -> None:
        pass
    
    @abstractmethod
    def set_volume(self, volume: int) -> None:
        pass


class TV(Device):
    """TV device."""
    
    def __init__(self):
        self.is_on = False
        self.volume = 0
    
    def turn_on(self) -> None:
        self.is_on = True
        logger.info("TV is ON")
    
    def turn_off(self) -> None:
        self.is_on = False
        logger.info("TV is OFF")
    
    def set_volume(self, volume: int) -> None:
        self.volume = max(0, min(100, volume))
        logger.info(f"TV volume set to {self.volume}")


class Radio(Device):
    """Radio device."""
    
    def __init__(self):
        self.is_on = False
        self.volume = 0
    
    def turn_on(self) -> None:
        self.is_on = True
        logger.info("Radio is ON")
    
    def turn_off(self) -> None:
        self.is_on = False
        logger.info("Radio is OFF")
    
    def set_volume(self, volume: int) -> None:
        self.volume = max(0, min(100, volume))
        logger.info(f"Radio volume set to {self.volume}")


class RemoteControl(ABC):
    """Remote control abstraction."""
    
    def __init__(self, device: Device):
        self.device = device
    
    def toggle_power(self) -> None:
        """Toggle device power."""
        if hasattr(self.device, 'is_on') and self.device.is_on:
            self.device.turn_off()
        else:
            self.device.turn_on()
    
    @abstractmethod
    def volume_up(self) -> None:
        pass
    
    @abstractmethod
    def volume_down(self) -> None:
        pass


class BasicRemote(RemoteControl):
    """Basic remote control."""
    
    def volume_up(self) -> None:
        current = getattr(self.device, 'volume', 0)
        self.device.set_volume(current + 10)
    
    def volume_down(self) -> None:
        current = getattr(self.device, 'volume', 0)
        self.device.set_volume(current - 10)


class AdvancedRemote(RemoteControl):
    """Advanced remote control with mute."""
    
    def volume_up(self) -> None:
        current = getattr(self.device, 'volume', 0)
        self.device.set_volume(current + 5)
    
    def volume_down(self) -> None:
        current = getattr(self.device, 'volume', 0)
        self.device.set_volume(current - 5)
    
    def mute(self) -> None:
        """Mute device."""
        self.device.set_volume(0)
        logger.info("Device muted")


def main() -> None:
    """Demonstration of Bridge Pattern."""
    logger.info("=" * 70)
    logger.info("BRIDGE DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Drawing Shapes
    logger.info("Example 1: Drawing Shapes with Different APIs")
    logger.info("-" * 70)
    
    shapes = [
        CircleShape(1, 2, 3, DrawingAPI1()),
        CircleShape(5, 7, 11, DrawingAPI2()),
    ]
    
    for shape in shapes:
        shape.draw()
        shape.resize_by_percentage(50)
        shape.draw()
    logger.info()
    
    # Example 2: Remote Control and Devices
    logger.info("Example 2: Remote Control and Devices")
    logger.info("-" * 70)
    
    tv = TV()
    radio = Radio()
    
    basic_tv_remote = BasicRemote(tv)
    advanced_radio_remote = AdvancedRemote(radio)
    
    logger.info("Using basic remote with TV:")
    basic_tv_remote.toggle_power()
    basic_tv_remote.volume_up()
    basic_tv_remote.volume_up()
    basic_tv_remote.volume_down()
    logger.info()
    
    logger.info("Using advanced remote with radio:")
    advanced_radio_remote.toggle_power()
    advanced_radio_remote.volume_up()
    advanced_radio_remote.volume_up()
    advanced_radio_remote.mute()
    logger.info()
    
    # Example 3: Switch device
    logger.info("Example 3: Same Remote, Different Device")
    logger.info("-" * 70)
    
    # Same remote can work with different devices
    basic_radio_remote = BasicRemote(radio)
    basic_radio_remote.toggle_power()
    basic_radio_remote.volume_up()
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Decouple an abstraction from its implementation so")
    logger.info("  that the two can vary independently.")
    logger.info("\nKey Advantages:")
    logger.info("  - Separates abstraction from implementation")
    logger.info("  - Implementation can vary independently")
    logger.info("  - Hides implementation details from clients")
    logger.info("  - Can switch implementations at runtime")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Increases complexity")
    logger.info("  - Can be overkill for simple cases")
    logger.info("  - Requires careful design")
    logger.info("\nWhen to Use:")
    logger.info("  - Want to avoid permanent binding between abstraction and implementation")
    logger.info("  - Both abstraction and implementation should be extensible")
    logger.info("  - Changes in implementation should not affect clients")
    logger.info("  - Want to share implementation among multiple objects")
    logger.info("\nBridge vs Adapter:")
    logger.info("  - Bridge: Design-time decision, separates concerns")
    logger.info("  - Adapter: Runtime decision, makes incompatible interfaces work")
    logger.info("\nCommon Use Cases:")
    logger.info("  - GUI frameworks (platform independence)")
    logger.info("  - Database drivers")
    logger.info("  - Device drivers")
    logger.info("  - Remote controls")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()