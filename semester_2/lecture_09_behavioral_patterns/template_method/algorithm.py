#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Template Method Design Pattern.

Defines the skeleton of an algorithm in a method, deferring some steps
to subclasses. Template Method lets subclasses redefine certain steps
of an algorithm without changing the algorithm's structure.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Abstract Class with Template Method
class DataProcessor(ABC):
    """Abstract data processor with template method."""
    
    def process(self) -> None:
        """Template method - defines algorithm skeleton."""
        self.read_data()
        self.process_data()
        self.save_data()
        self.notify_completion()
    
    @abstractmethod
    def read_data(self) -> None:
        """Read data - to be implemented by subclasses."""
        pass
    
    @abstractmethod
    def process_data(self) -> None:
        """Process data - to be implemented by subclasses."""
        pass
    
    def save_data(self) -> None:
        """Save data - default implementation."""
        print("Saving processed data...")
    
    def notify_completion(self) -> None:
        """Notify completion - default implementation."""
        print("Processing completed!")


class CSVProcessor(DataProcessor):
    """CSV data processor."""
    
    def read_data(self) -> None:
        print("Reading CSV file...")
    
    def process_data(self) -> None:
        print("Processing CSV data (parsing, validation)...")
    
    def save_data(self) -> None:
        print("Saving to database...")


class JSONProcessor(DataProcessor):
    """JSON data processor."""
    
    def read_data(self) -> None:
        print("Reading JSON file...")
    
    def process_data(self) -> None:
        print("Processing JSON data (parsing, transformation)...")
    
    def save_data(self) -> None:
        print("Saving to cloud storage...")


class XMLProcessor(DataProcessor):
    """XML data processor."""
    
    def read_data(self) -> None:
        print("Reading XML file...")
    
    def process_data(self) -> None:
        print("Processing XML data (parsing, validation, transformation)...")
    
    def notify_completion(self) -> None:
        print("XML processing completed and logged!")


# Example 2: Game Framework
class Game(ABC):
    """Abstract game with template method."""
    
    def play(self) -> None:
        """Template method for game flow."""
        self.initialize()
        self.start_play()
        self.end_play()
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize game."""
        pass
    
    @abstractmethod
    def start_play(self) -> None:
        """Start playing."""
        pass
    
    def end_play(self) -> None:
        """End game - default implementation."""
        print("Game ended!")


class Chess(Game):
    """Chess game."""
    
    def initialize(self) -> None:
        print("Setting up chess board...")
        print("Placing pieces...")
    
    def start_play(self) -> None:
        print("Starting chess game...")
        print("Players take turns...")


class Soccer(Game):
    """Soccer game."""
    
    def initialize(self) -> None:
        print("Setting up soccer field...")
        print("Teams ready...")
    
    def start_play(self) -> None:
        print("Starting soccer match...")
        print("Kickoff!")
    
    def end_play(self) -> None:
        print("Match ended!")
        print("Final score displayed")


# Example 3: Build Process
class BuildProcess(ABC):
    """Abstract build process."""
    
    def build(self) -> None:
        """Template method for build process."""
        self.fetch_dependencies()
        self.compile()
        self.test()
        self.package()
        self.deploy()
    
    @abstractmethod
    def fetch_dependencies(self) -> None:
        pass
    
    @abstractmethod
    def compile(self) -> None:
        pass
    
    def test(self) -> None:
        """Default test implementation."""
        print("Running tests...")
    
    @abstractmethod
    def package(self) -> None:
        pass
    
    def deploy(self) -> None:
        """Default deploy - can be overridden."""
        print("Deploying...")


class JavaBuildProcess(BuildProcess):
    """Java build process."""
    
    def fetch_dependencies(self) -> None:
        print("Fetching Maven dependencies...")
    
    def compile(self) -> None:
        print("Compiling Java source files...")
    
    def package(self) -> None:
        print("Creating JAR file...")


class PythonBuildProcess(BuildProcess):
    """Python build process."""
    
    def fetch_dependencies(self) -> None:
        print("Installing pip dependencies...")
    
    def compile(self) -> None:
        print("Checking Python syntax...")
    
    def package(self) -> None:
        print("Creating wheel package...")
    
    def deploy(self) -> None:
        print("Uploading to PyPI...")


def main() -> None:
    """Demonstration of Template Method Pattern."""
    print("=" * 70)
    print("TEMPLATE METHOD DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Data Processing
    print("Example 1: Data Processing")
    print("-" * 70)
    
    processors = [
        CSVProcessor(),
        JSONProcessor(),
        XMLProcessor(),
    ]
    
    for processor in processors:
        print(f"\nProcessing with {processor.__class__.__name__}:")
        processor.process()
    print()
    
    # Example 2: Games
    print("Example 2: Game Framework")
    print("-" * 70)
    
    games = [Chess(), Soccer()]
    
    for game in games:
        print(f"\nPlaying {game.__class__.__name__}:")
        game.play()
    print()
    
    # Example 3: Build Processes
    print("Example 3: Build Processes")
    print("-" * 70)
    
    builds = [JavaBuildProcess(), PythonBuildProcess()]
    
    for build in builds:
        print(f"\nBuilding with {build.__class__.__name__}:")
        build.build()
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Define the skeleton of an algorithm in a method, deferring")
    print("  some steps to subclasses. Template Method lets subclasses")
    print("  redefine certain steps without changing the algorithm's structure.")
    print("\nKey Advantages:")
    print("  - Code reuse")
    print("  - Consistent algorithm structure")
    print("  - Easy to add new variants")
    print("  - Control over algorithm flow")
    print("\nKey Disadvantages:")
    print("  - Can be rigid")
    print("  - Inheritance-based (tight coupling)")
    print("  - Can be hard to understand")
    print("\nWhen to Use:")
    print("  - Have algorithm with invariant parts")
    print("  - Want to avoid code duplication")
    print("  - Want to control algorithm structure")
    print("  - Common behavior in base class")
    print("\nCommon Use Cases:")
    print("  - Framework design")
    print("  - Build processes")
    print("  - Data processing pipelines")
    print("  - Game frameworks")
    print("  - Test frameworks")
    print("=" * 70)


if __name__ == "__main__":
    main()
