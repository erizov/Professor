#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Abstract Factory Design Pattern.

Provides an interface for creating families of related or dependent
objects without specifying their concrete classes.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


# Abstract Products
class Button(ABC):
    """Abstract button product."""
    
    @abstractmethod
    def render(self) -> str:
        """Render button."""
        pass


class Dialog(ABC):
    """Abstract dialog product."""
    
    @abstractmethod
    def render(self) -> str:
        """Render dialog."""
        pass


# Concrete Products - Windows
class WindowsButton(Button):
    """Windows button."""
    
    def render(self) -> str:
        return "Windows Button rendered"


class WindowsDialog(Dialog):
    """Windows dialog."""
    
    def render(self) -> str:
        return "Windows Dialog rendered"


# Concrete Products - Mac
class MacButton(Button):
    """Mac button."""
    
    def render(self) -> str:
        return "Mac Button rendered"


class MacDialog(Dialog):
    """Mac dialog."""
    
    def render(self) -> str:
        return "Mac Dialog rendered"


# Abstract Factory
class GUIFactory(ABC):
    """Abstract factory for GUI components."""
    
    @abstractmethod
    def create_button(self) -> Button:
        """Create button."""
        pass
    
    @abstractmethod
    def create_dialog(self) -> Dialog:
        """Create dialog."""
        pass


# Concrete Factories
class WindowsFactory(GUIFactory):
    """Windows GUI factory."""
    
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_dialog(self) -> Dialog:
        return WindowsDialog()


class MacFactory(GUIFactory):
    """Mac GUI factory."""
    
    def create_button(self) -> Button:
        return MacButton()
    
    def create_dialog(self) -> Dialog:
        return MacDialog()


# Client Code
class Application:
    """Application using abstract factory."""
    
    def __init__(self, factory: GUIFactory):
        self.factory = factory
        self.button = None
        self.dialog = None
    
    def create_ui(self) -> None:
        """Create UI components."""
        self.button = self.factory.create_button()
        self.dialog = self.factory.create_dialog()
    
    def render_ui(self) -> None:
        """Render UI."""
        if self.button and self.dialog:
            logger.info(self.button.render())
            logger.info(self.dialog.render())


# Example 2: Database Factory
class DatabaseConnection(ABC):
    """Abstract database connection."""
    
    @abstractmethod
    def connect(self) -> str:
        pass


class DatabaseQuery(ABC):
    """Abstract database query."""
    
    @abstractmethod
    def execute(self, sql: str) -> str:
        pass


class MySQLConnection(DatabaseConnection):
    """MySQL connection."""
    
    def connect(self) -> str:
        return "Connected to MySQL"


class MySQLQuery(DatabaseQuery):
    """MySQL query."""
    
    def execute(self, sql: str) -> str:
        return f"MySQL: Executed {sql}"


class PostgreSQLConnection(DatabaseConnection):
    """PostgreSQL connection."""
    
    def connect(self) -> str:
        return "Connected to PostgreSQL"


class PostgreSQLQuery(DatabaseQuery):
    """PostgreSQL query."""
    
    def execute(self, sql: str) -> str:
        return f"PostgreSQL: Executed {sql}"


class DatabaseFactory(ABC):
    """Abstract database factory."""
    
    @abstractmethod
    def create_connection(self) -> DatabaseConnection:
        pass
    
    @abstractmethod
    def create_query(self) -> DatabaseQuery:
        pass


class MySQLFactory(DatabaseFactory):
    """MySQL factory."""
    
    def create_connection(self) -> DatabaseConnection:
        return MySQLConnection()
    
    def create_query(self) -> DatabaseQuery:
        return MySQLQuery()


class PostgreSQLFactory(DatabaseFactory):
    """PostgreSQL factory."""
    
    def create_connection(self) -> DatabaseConnection:
        return PostgreSQLConnection()
    
    def create_query(self) -> DatabaseQuery:
        return PostgreSQLQuery()


def main() -> None:
    """Demonstration of Abstract Factory Pattern."""
    logger.info("=" * 70)
    logger.info("ABSTRACT FACTORY DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: GUI Factory
    logger.info("Example 1: GUI Factory")
    logger.info("-" * 70)
    
    # Windows application
    windows_factory = WindowsFactory()
    windows_app = Application(windows_factory)
    windows_app.create_ui()
    logger.info("Windows UI:")
    windows_app.render_ui()
    logger.info()
    
    # Mac application
    mac_factory = MacFactory()
    mac_app = Application(mac_factory)
    mac_app.create_ui()
    logger.info("Mac UI:")
    mac_app.render_ui()
    logger.info()
    
    # Example 2: Database Factory
    logger.info("Example 2: Database Factory")
    logger.info("-" * 70)
    
    # MySQL
    mysql_factory = MySQLFactory()
    mysql_conn = mysql_factory.create_connection()
    mysql_query = mysql_factory.create_query()
    
    logger.info(mysql_conn.connect())
    logger.info(mysql_query.execute("SELECT * FROM users"))
    logger.info()
    
    # PostgreSQL
    postgres_factory = PostgreSQLFactory()
    postgres_conn = postgres_factory.create_connection()
    postgres_query = postgres_factory.create_query()
    
    logger.info(postgres_conn.connect())
    logger.info(postgres_query.execute("SELECT * FROM users"))
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Abstract Factory")
    
    def create_windows_ui():
        factory = WindowsFactory()
        app = Application(factory)
        app.create_ui()
        return app
    
    result, metrics = timer.measure(create_windows_ui)
    logger.info(f"Time to create Windows UI: {metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Provide an interface for creating families of related")
    logger.info("  or dependent objects without specifying their concrete classes.")
    logger.info("\nKey Advantages:")
    logger.info("  - Ensures products from one family are used together")
    logger.info("  - Isolates concrete classes from client")
    logger.info("  - Easy to add new product families")
    logger.info("  - Promotes consistency among products")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Complex to implement")
    logger.info("  - Hard to extend with new product types")
    logger.info("  - Can be overkill for simple cases")
    logger.info("\nWhen to Use:")
    logger.info("  - System should be independent of product creation")
    logger.info("  - System configured with multiple product families")
    logger.info("  - Products from same family must be used together")
    logger.info("  - Want to provide product class library")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Cross-platform GUI toolkits")
    logger.info("  - Database abstraction layers")
    logger.info("  - Theme systems")
    logger.info("  - Plugin architectures")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()