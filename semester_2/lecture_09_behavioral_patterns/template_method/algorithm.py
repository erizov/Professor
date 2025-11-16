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
from framework.logging_utils import get_logger
logger = get_logger(__name__)

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
        logger.info("Saving processed data...")
    
    def notify_completion(self) -> None:
        """Notify completion - default implementation."""
        logger.info("Processing completed!")


class CSVProcessor(DataProcessor):
    """CSV data processor."""
    
    def read_data(self) -> None:
        logger.info("Reading CSV file...")
    
    def process_data(self) -> None:
        logger.info("Processing CSV data (parsing, validation)...")
    
    def save_data(self) -> None:
        logger.info("Saving to database...")


class JSONProcessor(DataProcessor):
    """JSON data processor."""
    
    def read_data(self) -> None:
        logger.info("Reading JSON file...")
    
    def process_data(self) -> None:
        logger.info("Processing JSON data (parsing, transformation)...")
    
    def save_data(self) -> None:
        logger.info("Saving to cloud storage...")


class XMLProcessor(DataProcessor):
    """XML data processor."""
    
    def read_data(self) -> None:
        logger.info("Reading XML file...")
    
    def process_data(self) -> None:
        logger.info("Processing XML data (parsing, validation, transformation)...")
    
    def notify_completion(self) -> None:
        logger.info("XML processing completed and logged!")


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
        logger.info("Game ended!")


class Chess(Game):
    """Chess game."""
    
    def initialize(self) -> None:
        logger.info("Setting up chess board...")
        logger.info("Placing pieces...")
    
    def start_play(self) -> None:
        logger.info("Starting chess game...")
        logger.info("Players take turns...")


class Soccer(Game):
    """Soccer game."""
    
    def initialize(self) -> None:
        logger.info("Setting up soccer field...")
        logger.info("Teams ready...")
    
    def start_play(self) -> None:
        logger.info("Starting soccer match...")
        logger.info("Kickoff!")
    
    def end_play(self) -> None:
        logger.info("Match ended!")
        logger.info("Final score displayed")


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
        logger.info("Running tests...")
    
    @abstractmethod
    def package(self) -> None:
        pass
    
    def deploy(self) -> None:
        """Default deploy - can be overridden."""
        logger.info("Deploying...")


class JavaBuildProcess(BuildProcess):
    """Java build process."""
    
    def fetch_dependencies(self) -> None:
        logger.info("Fetching Maven dependencies...")
    
    def compile(self) -> None:
        logger.info("Compiling Java source files...")
    
    def package(self) -> None:
        logger.info("Creating JAR file...")


class PythonBuildProcess(BuildProcess):
    """Python build process."""
    
    def fetch_dependencies(self) -> None:
        logger.info("Installing pip dependencies...")
    
    def compile(self) -> None:
        logger.info("Checking Python syntax...")
    
    def package(self) -> None:
        logger.info("Creating wheel package...")
    
    def deploy(self) -> None:
        logger.info("Uploading to PyPI...")


def main() -> None:
    """Demonstration of Template Method Pattern."""
    logger.info("=" * 70)
    logger.info("TEMPLATE METHOD DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Data Processing
    logger.info("Example 1: Data Processing")
    logger.info("-" * 70)
    
    processors = [
        CSVProcessor(),
        JSONProcessor(),
        XMLProcessor(),
    ]
    
    for processor in processors:
        logger.info(f"\nProcessing with {processor.__class__.__name__}:")
        processor.process()
    logger.info()
    
    # Example 2: Games
    logger.info("Example 2: Game Framework")
    logger.info("-" * 70)
    
    games = [Chess(), Soccer()]
    
    for game in games:
        logger.info(f"\nPlaying {game.__class__.__name__}:")
        game.play()
    logger.info()
    
    # Example 3: Build Processes
    logger.info("Example 3: Build Processes")
    logger.info("-" * 70)
    
    builds = [JavaBuildProcess(), PythonBuildProcess()]
    
    for build in builds:
        logger.info(f"\nBuilding with {build.__class__.__name__}:")
        build.build()
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Define the skeleton of an algorithm in a method, deferring")
    logger.info("  some steps to subclasses. Template Method lets subclasses")
    logger.info("  redefine certain steps without changing the algorithm's structure.")
    logger.info("\nKey Advantages:")
    logger.info("  - Code reuse")
    logger.info("  - Consistent algorithm structure")
    logger.info("  - Easy to add new variants")
    logger.info("  - Control over algorithm flow")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Can be rigid")
    logger.info("  - Inheritance-based (tight coupling)")
    logger.info("  - Can be hard to understand")
    logger.info("\nWhen to Use:")
    logger.info("  - Have algorithm with invariant parts")
    logger.info("  - Want to avoid code duplication")
    logger.info("  - Want to control algorithm structure")
    logger.info("  - Common behavior in base class")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Framework design")
    logger.info("  - Build processes")
    logger.info("  - Data processing pipelines")
    logger.info("  - Game frameworks")
    logger.info("  - Test frameworks")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()