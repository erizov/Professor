#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command Design Pattern.

Encapsulates a request as an object, thereby letting you parameterize
clients with different requests, queue operations, and support undo operations.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Command Interface
class Command(ABC):
    """Abstract command interface."""
    
    @abstractmethod
    def execute(self) -> None:
        """Execute command."""
        
    
    """
    Command implementation.
    
    Args:
        *args: Variable arguments
        **kwargs: Keyword arguments
        
    Returns:
        Algorithm result
    """
    # Implementation for command
    logger.info(f"Executing command")
    return None


def main() -> None:
    """Demonstration of Command Pattern."""
    logger.info("=" * 70)
    logger.info("COMMAND DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Light Control
    logger.info("Example 1: Light Control")
    logger.info("-" * 70)
    
    living_room_light = Light("Living Room")
    kitchen_light = Light("Kitchen")
    
    remote = RemoteControl()
    
    remote.set_command(LightOnCommand(living_room_light))
    remote.press_button()
    
    remote.set_command(LightOnCommand(kitchen_light))
    remote.press_button()
    
    remote.set_command(LightOffCommand(living_room_light))
    remote.press_button()
    
    logger.info("\nUndoing last command:")
    remote.press_undo()
    logger.info()
    
    # Example 2: Text Editor
    logger.info("Example 2: Text Editor with Undo")
    logger.info("-" * 70)
    
    editor = TextEditor()
    history: List[Command] = []
    
    # Write commands
    write1 = WriteCommand(editor, "Hello ")
    write1.execute()
    history.append(write1)
    
    write2 = WriteCommand(editor, "World")
    write2.execute()
    history.append(write2)
    
    logger.info(f"Text: '{editor.get_text()}'")
    
    # Undo
    if history:
        cmd = history.pop()
        cmd.undo()
        logger.info(f"After undo: '{editor.get_text()}'")
    logger.info()
    
    # Example 3: Macro Commands
    logger.info("Example 3: Macro Commands")
    logger.info("-" * 70)
    
    bedroom_light = Light("Bedroom")
    bathroom_light = Light("Bathroom")
    
    # Create macro to turn on all lights
    party_mode = MacroCommand([
        LightOnCommand(living_room_light),
        LightOnCommand(kitchen_light),
        LightOnCommand(bedroom_light),
        LightOnCommand(bathroom_light),
    ])
    
    logger.info("Executing party mode (macro command):")
    party_mode.execute()
    
    logger.info("\nUndoing party mode:")
    party_mode.undo()
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Encapsulate a request as an object, thereby letting you")
    logger.info("  parameterize clients with different requests, queue")
    logger.info("  operations, and support undo operations.")
    logger.info("\nKey Advantages:")
    logger.info("  - Decouples invoker from receiver")
    logger.info("  - Easy to add new commands")
    logger.info("  - Supports undo/redo")
    logger.info("  - Supports macro commands")
    logger.info("  - Can queue and log requests")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Increases number of classes")
    logger.info("  - Can be overkill for simple operations")
    logger.info("\nWhen to Use:")
    logger.info("  - Need to parameterize objects with operations")
    logger.info("  - Need to queue operations")
    logger.info("  - Need undo/redo functionality")
    logger.info("  - Need to log operations")
    logger.info("  - Need macro commands")
    logger.info("\nCommon Use Cases:")
    logger.info("  - GUI buttons and menu items")
    logger.info("  - Undo/redo functionality")
    logger.info("  - Transaction systems")
    logger.info("  - Macro recording")
    logger.info("  - Job queues")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()