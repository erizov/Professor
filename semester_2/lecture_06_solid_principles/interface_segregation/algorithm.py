#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interface Segregation Principle (ISP).

Clients should not be forced to depend on interfaces they do not use.
Many client-specific interfaces are better than one general-purpose interface.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# ❌ BAD: Violates ISP - forces clients to implement unused methods
class BadWorker(ABC):
    """Worker interface that violates ISP."""
    
    @abstractmethod
    def work(self) -> None:
        """Work."""
        pass
    
    @abstractmethod
    def eat(self) -> None:
        """Eat."""
        pass
    
    @abstractmethod
    def sleep(self) -> None:
        """Sleep."""
        pass


class BadHumanWorker(BadWorker):
    """Human worker - implements all methods."""
    
    def work(self) -> None:
        print("Human working...")
    
    def eat(self) -> None:
        print("Human eating...")
    
    def sleep(self) -> None:
        print("Human sleeping...")


class BadRobotWorker(BadWorker):
    """Robot worker - forced to implement unused methods!"""
    
    def work(self) -> None:
        print("Robot working...")
    
    def eat(self) -> None:
        raise NotImplementedError("Robots don't eat!")  # Forced!
    
    def sleep(self) -> None:
        raise NotImplementedError("Robots don't sleep!")  # Forced!


# ✅ GOOD: Follows ISP - segregated interfaces
class Workable(ABC):
    """Interface for workable entities."""
    
    @abstractmethod
    def work(self) -> None:
        """Work."""
        pass


class Eatable(ABC):
    """Interface for eatable entities."""
    
    @abstractmethod
    def eat(self) -> None:
        """Eat."""
        pass


class Sleepable(ABC):
    """Interface for sleepable entities."""
    
    @abstractmethod
    def sleep(self) -> None:
        """Sleep."""
        pass


class HumanWorker(Workable, Eatable, Sleepable):
    """Human worker - implements all relevant interfaces."""
    
    def work(self) -> None:
        print("Human working...")
    
    def eat(self) -> None:
        print("Human eating...")
    
    def sleep(self) -> None:
        print("Human sleeping...")


class RobotWorker(Workable):
    """Robot worker - only implements work interface."""
    
    def work(self) -> None:
        print("Robot working...")


# Example 2: Document Operations
# ❌ BAD: Fat interface
class BadPrinter(ABC):
    """Printer interface that violates ISP."""
    
    @abstractmethod
    def print_document(self, document: str) -> None:
        pass
    
    @abstractmethod
    def scan_document(self) -> str:
        pass
    
    @abstractmethod
    def fax_document(self, document: str) -> None:
        pass


class BadSimplePrinter(BadPrinter):
    """Simple printer - forced to implement unused methods."""
    
    def print_document(self, document: str) -> None:
        print(f"Printing: {document}")
    
    def scan_document(self) -> str:
        raise NotImplementedError("Simple printer cannot scan!")
    
    def fax_document(self, document: str) -> None:
        raise NotImplementedError("Simple printer cannot fax!")


# ✅ GOOD: Segregated interfaces
class Printer(ABC):
    """Printer interface."""
    
    @abstractmethod
    def print_document(self, document: str) -> None:
        pass


class Scanner(ABC):
    """Scanner interface."""
    
    @abstractmethod
    def scan_document(self) -> str:
        pass


class Fax(ABC):
    """Fax interface."""
    
    @abstractmethod
    def fax_document(self, document: str) -> None:
        pass


class SimplePrinter(Printer):
    """Simple printer - only prints."""
    
    def print_document(self, document: str) -> None:
        print(f"Printing: {document}")


class MultiFunctionPrinter(Printer, Scanner, Fax):
    """Multi-function printer - implements all interfaces."""
    
    def print_document(self, document: str) -> None:
        print(f"Printing: {document}")
    
    def scan_document(self) -> str:
        return "Scanned document"
    
    def fax_document(self, document: str) -> None:
        print(f"Faxing: {document}")


# Example 3: Repository Pattern
# ❌ BAD: Fat repository interface
class BadRepository(ABC):
    """Repository that violates ISP."""
    
    @abstractmethod
    def create(self, entity: any) -> None:
        pass
    
    @abstractmethod
    def read(self, id: int) -> any:
        pass
    
    @abstractmethod
    def update(self, entity: any) -> None:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> None:
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> list:
        pass
    
    @abstractmethod
    def find_by_date(self, date: str) -> list:
        pass


# ✅ GOOD: Segregated interfaces
class Readable(ABC):
    """Read interface."""
    
    @abstractmethod
    def read(self, id: int) -> any:
        pass


class Writable(ABC):
    """Write interface."""
    
    @abstractmethod
    def create(self, entity: any) -> None:
        pass
    
    @abstractmethod
    def update(self, entity: any) -> None:
        pass


class Deletable(ABC):
    """Delete interface."""
    
    @abstractmethod
    def delete(self, id: int) -> None:
        pass


class Searchable(ABC):
    """Search interface."""
    
    @abstractmethod
    def find_by_name(self, name: str) -> list:
        pass


class ReadOnlyRepository(Readable):
    """Read-only repository."""
    
    def read(self, id: int) -> any:
        print(f"Reading entity {id}")
        return f"Entity {id}"


class FullRepository(Readable, Writable, Deletable, Searchable):
    """Full repository with all operations."""
    
    def read(self, id: int) -> any:
        print(f"Reading entity {id}")
        return f"Entity {id}"
    
    def create(self, entity: any) -> None:
        print(f"Creating {entity}")
    
    def update(self, entity: any) -> None:
        print(f"Updating {entity}")
    
    def delete(self, id: int) -> None:
        print(f"Deleting entity {id}")
    
    def find_by_name(self, name: str) -> list:
        print(f"Finding entities with name: {name}")
        return []


def main() -> None:
    """Demonstration of Interface Segregation Principle."""
    print("=" * 70)
    print("INTERFACE SEGREGATION PRINCIPLE (ISP) DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Workers
    print("Example 1: Worker Interfaces")
    print("-" * 70)
    
    print("❌ BAD: Robot forced to implement unused methods")
    try:
        robot = BadRobotWorker()
        robot.work()
        robot.eat()  # This will fail!
    except NotImplementedError as e:
        print(f"Error: {e}")
    print()
    
    print("✅ GOOD: Segregated interfaces")
    human = HumanWorker()
    robot = RobotWorker()
    
    human.work()
    human.eat()
    robot.work()
    # robot.eat()  # Not available - correct!
    print()
    
    # Example 2: Printers
    print("Example 2: Printer Interfaces")
    print("-" * 70)
    
    simple = SimplePrinter()
    simple.print_document("Document 1")
    
    multi = MultiFunctionPrinter()
    multi.print_document("Document 2")
    multi.scan_document()
    multi.fax_document("Document 3")
    print()
    
    # Example 3: Repositories
    print("Example 3: Repository Interfaces")
    print("-" * 70)
    
    read_only = ReadOnlyRepository()
    read_only.read(1)
    
    full = FullRepository()
    full.create("New Entity")
    full.read(1)
    full.update("Updated Entity")
    full.find_by_name("Test")
    full.delete(1)
    print()
    
    print("=" * 70)
    print("\nPrinciple Summary:")
    print("\nDefinition:")
    print("  Clients should not be forced to depend on interfaces")
    print("  they do not use. Many client-specific interfaces are")
    print("  better than one general-purpose interface.")
    print("\nKey Benefits:")
    print("  - Clients only depend on what they use")
    print("  - No forced implementation of unused methods")
    print("  - Better code organization")
    print("  - Easier to maintain and extend")
    print("\nCommon Violations:")
    print("  - Fat interfaces (too many methods)")
    print("  - Clients implementing unused methods")
    print("  - Throwing NotImplementedError")
    print("  - Empty method implementations")
    print("\nHow to Apply:")
    print("  1. Split large interfaces into smaller ones")
    print("  2. Group related methods together")
    print("  3. Use composition of interfaces")
    print("  4. Keep interfaces focused and cohesive")
    print("\nSigns of Violation:")
    print("  - Classes implementing unused methods")
    print("  - NotImplementedError exceptions")
    print("  - Empty method implementations")
    print("  - Clients depending on unused functionality")
    print("=" * 70)


if __name__ == "__main__":
    main()
