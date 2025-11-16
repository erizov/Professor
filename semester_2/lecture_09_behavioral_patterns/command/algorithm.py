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
        pass
    
    @abstractmethod
    def undo(self) -> None:
        """Undo command."""
        pass


# Receiver
class Light:
    """Light receiver."""
    
    def __init__(self, location: str):
        self.location = location
        self.is_on = False
    
    def on(self) -> None:
        self.is_on = True
        logger.info(f"{self.location} light is ON")
    
    def off(self) -> None:
        self.is_on = False
        logger.info(f"{self.location} light is OFF")


# Concrete Commands
class LightOnCommand(Command):
    """Command to turn light on."""
    
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self) -> None:
        self.light.on()
    
    def undo(self) -> None:
        self.light.off()


class LightOffCommand(Command):
    """Command to turn light off."""
    
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self) -> None:
        self.light.off()
    
    def undo(self) -> None:
        self.light.on()


# Invoker
class RemoteControl:
    """Remote control invoker."""
    
    def __init__(self):
        self.commands: List[Command] = []
        self.history: List[Command] = []
    
    def set_command(self, command: Command) -> None:
        """Set command to execute."""
        self.commands.append(command)
    
    def press_button(self) -> None:
        """Press button to execute command."""
        if self.commands:
            command = self.commands.pop(0)
            command.execute()
            self.history.append(command)
    
    def press_undo(self) -> None:
        """Undo last command."""
        if self.history:
            command = self.history.pop()
            command.undo()


# Example 2: Text Editor
class TextEditor:
    """Text editor receiver."""
    
    def __init__(self):
        self.text = ""
    
    def write(self, text: str) -> None:
        """Write text."""
        self.text += text
    
    def delete(self, length: int) -> None:
        """Delete text."""
        self.text = self.text[:-length] if length <= len(self.text) else ""
    
    def get_text(self) -> str:
        """Get text."""
        return self.text


class WriteCommand(Command):
    """Command to write text."""
    
    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text
    
    def execute(self) -> None:
        self.editor.write(self.text)
    
    def undo(self) -> None:
        self.editor.delete(len(self.text))


class DeleteCommand(Command):
    """Command to delete text."""
    
    def __init__(self, editor: TextEditor, length: int):
        self.editor = editor
        self.length = length
        self.deleted_text = ""
    
    def execute(self) -> None:
        if len(self.editor.text) >= self.length:
            self.deleted_text = self.editor.text[-self.length:]
        self.editor.delete(self.length)
    
    def undo(self) -> None:
        self.editor.write(self.deleted_text)


# Example 3: Macro Commands
class MacroCommand(Command):
    """Macro command - executes multiple commands."""
    
    def __init__(self, commands: List[Command]):
        self.commands = commands
    
    def execute(self) -> None:
        """Execute all commands."""
        for command in self.commands:
            command.execute()
    
    def undo(self) -> None:
        """Undo all commands in reverse order."""
        for command in reversed(self.commands):
            command.undo()


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