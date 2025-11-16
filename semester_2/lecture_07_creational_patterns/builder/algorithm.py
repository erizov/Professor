#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builder Design Pattern.

Separates the construction of a complex object from its representation,
allowing the same construction process to create different representations.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional, List
from framework.logging_utils import get_logger
logger = get_logger(__name__)

sys.path.append(str(Path(__file__).parent.parent.parent.parent))


# Product
class Computer:
    """Computer product."""
    
    def __init__(self):
        self.cpu: Optional[str] = None
        self.ram: Optional[str] = None
        self.storage: Optional[str] = None
        self.gpu: Optional[str] = None
        self.motherboard: Optional[str] = None
        self.power_supply: Optional[str] = None
    
    def __str__(self) -> str:
        parts = []
        if self.cpu:
            parts.append(f"CPU: {self.cpu}")
        if self.ram:
            parts.append(f"RAM: {self.ram}")
        if self.storage:
            parts.append(f"Storage: {self.storage}")
        if self.gpu:
            parts.append(f"GPU: {self.gpu}")
        if self.motherboard:
            parts.append(f"Motherboard: {self.motherboard}")
        if self.power_supply:
            parts.append(f"Power Supply: {self.power_supply}")
        return "Computer(" + ", ".join(parts) + ")"


# Builder Interface
class ComputerBuilder(ABC):
    """Abstract computer builder."""
    
    def __init__(self):
        self.computer = Computer()
    
    @abstractmethod
    def build_cpu(self, cpu: str) -> 'ComputerBuilder':
        """Build CPU."""
        pass
    
    @abstractmethod
    def build_ram(self, ram: str) -> 'ComputerBuilder':
        """Build RAM."""
        pass
    
    @abstractmethod
    def build_storage(self, storage: str) -> 'ComputerBuilder':
        """Build storage."""
        pass
    
    @abstractmethod
    def build_gpu(self, gpu: str) -> 'ComputerBuilder':
        """Build GPU."""
        pass
    
    def build_motherboard(self, motherboard: str) -> 'ComputerBuilder':
        """Build motherboard (optional)."""
        self.computer.motherboard = motherboard
        return self
    
    def build_power_supply(self, power_supply: str) -> 'ComputerBuilder':
        """Build power supply (optional)."""
        self.computer.power_supply = power_supply
        return self
    
    def get_computer(self) -> Computer:
        """Get built computer."""
        return self.computer


# Concrete Builder
class GamingComputerBuilder(ComputerBuilder):
    """Builder for gaming computers."""
    
    def build_cpu(self, cpu: str) -> 'ComputerBuilder':
        self.computer.cpu = cpu or "Intel i9-13900K"
        return self
    
    def build_ram(self, ram: str) -> 'ComputerBuilder':
        self.computer.ram = ram or "32GB DDR5"
        return self
    
    def build_storage(self, storage: str) -> 'ComputerBuilder':
        self.computer.storage = storage or "2TB NVMe SSD"
        return self
    
    def build_gpu(self, gpu: str) -> 'ComputerBuilder':
        self.computer.gpu = gpu or "NVIDIA RTX 4090"
        return self


class OfficeComputerBuilder(ComputerBuilder):
    """Builder for office computers."""
    
    def build_cpu(self, cpu: str) -> 'ComputerBuilder':
        self.computer.cpu = cpu or "Intel i5-13400"
        return self
    
    def build_ram(self, ram: str) -> 'ComputerBuilder':
        self.computer.ram = ram or "16GB DDR4"
        return self
    
    def build_storage(self, storage: str) -> 'ComputerBuilder':
        self.computer.storage = storage or "512GB SSD"
        return self
    
    def build_gpu(self, gpu: str) -> 'ComputerBuilder':
        self.computer.gpu = gpu or "Integrated Graphics"
        return self


# Director (optional)
class ComputerDirector:
    """Director that constructs computers using builders."""
    
    def __init__(self, builder: ComputerBuilder):
        self.builder = builder
    
    def build_gaming_pc(self) -> Computer:
        """Build a gaming PC."""
        return (self.builder
                .build_cpu("Intel i9-13900K")
                .build_ram("32GB DDR5")
                .build_storage("2TB NVMe SSD")
                .build_gpu("NVIDIA RTX 4090")
                .build_motherboard("ASUS ROG Strix Z790")
                .build_power_supply("1000W 80+ Gold")
                .get_computer())
    
    def build_office_pc(self) -> Computer:
        """Build an office PC."""
        return (self.builder
                .build_cpu("Intel i5-13400")
                .build_ram("16GB DDR4")
                .build_storage("512GB SSD")
                .build_gpu("Integrated Graphics")
                .build_motherboard("ASUS Prime B760")
                .build_power_supply("500W 80+ Bronze")
                .get_computer())


# Fluent Builder Example
class Pizza:
    """Pizza product."""
    
    def __init__(self):
        self.size: Optional[str] = None
        self.crust: Optional[str] = None
        self.cheese: bool = False
        self.pepperoni: bool = False
        self.bacon: bool = False
        self.mushrooms: bool = False
        self.onions: bool = False
        self.peppers: bool = False
    
    def __str__(self) -> str:
        toppings = []
        if self.cheese:
            toppings.append("cheese")
        if self.pepperoni:
            toppings.append("pepperoni")
        if self.bacon:
            toppings.append("bacon")
        if self.mushrooms:
            toppings.append("mushrooms")
        if self.onions:
            toppings.append("onions")
        if self.peppers:
            toppings.append("peppers")
        
        return (f"Pizza(size={self.size}, crust={self.crust}, "
                f"toppings=[{', '.join(toppings)}])")


class PizzaBuilder:
    """Fluent builder for pizza."""
    
    def __init__(self):
        self.pizza = Pizza()
    
    def size(self, size: str) -> 'PizzaBuilder':
        """Set pizza size."""
        self.pizza.size = size
        return self
    
    def crust(self, crust: str) -> 'PizzaBuilder':
        """Set crust type."""
        self.pizza.crust = crust
        return self
    
    def add_cheese(self) -> 'PizzaBuilder':
        """Add cheese."""
        self.pizza.cheese = True
        return self
    
    def add_pepperoni(self) -> 'PizzaBuilder':
        """Add pepperoni."""
        self.pizza.pepperoni = True
        return self
    
    def add_bacon(self) -> 'PizzaBuilder':
        """Add bacon."""
        self.pizza.bacon = True
        return self
    
    def add_mushrooms(self) -> 'PizzaBuilder':
        """Add mushrooms."""
        self.pizza.mushrooms = True
        return self
    
    def add_onions(self) -> 'PizzaBuilder':
        """Add onions."""
        self.pizza.onions = True
        return self
    
    def add_peppers(self) -> 'PizzaBuilder':
        """Add peppers."""
        self.pizza.peppers = True
        return self
    
    def build(self) -> Pizza:
        """Build pizza."""
        return self.pizza


# SQL Query Builder Example
class SQLQuery:
    """SQL query product."""
    
    def __init__(self):
        self.select: List[str] = []
        self.from_table: Optional[str] = None
        self.where: List[str] = []
        self.order_by: List[str] = []
        self.limit: Optional[int] = None
    
    def __str__(self) -> str:
        query = "SELECT "
        query += ", ".join(self.select) if self.select else "*"
        
        if self.from_table:
            query += f" FROM {self.from_table}"
        
        if self.where:
            query += " WHERE " + " AND ".join(self.where)
        
        if self.order_by:
            query += " ORDER BY " + ", ".join(self.order_by)
        
        if self.limit:
            query += f" LIMIT {self.limit}"
        
        return query


class SQLQueryBuilder:
    """Builder for SQL queries."""
    
    def __init__(self):
        self.query = SQLQuery()
    
    def select(self, *columns: str) -> 'SQLQueryBuilder':
        """Add SELECT columns."""
        self.query.select.extend(columns)
        return self
    
    def from_table(self, table: str) -> 'SQLQueryBuilder':
        """Set FROM table."""
        self.query.from_table = table
        return self
    
    def where(self, condition: str) -> 'SQLQueryBuilder':
        """Add WHERE condition."""
        self.query.where.append(condition)
        return self
    
    def order_by(self, *columns: str) -> 'SQLQueryBuilder':
        """Add ORDER BY columns."""
        self.query.order_by.extend(columns)
        return self
    
    def limit(self, n: int) -> 'SQLQueryBuilder':
        """Set LIMIT."""
        self.query.limit = n
        return self
    
    def build(self) -> SQLQuery:
        """Build SQL query."""
        return self.query


def main() -> None:
    """Demonstration of Builder Pattern."""
    logger.info("=" * 70)
    logger.info("BUILDER DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Computer Builder
    logger.info("Example 1: Computer Builder")
    logger.info("-" * 70)
    
    gaming_builder = GamingComputerBuilder()
    gaming_pc = (gaming_builder
                 .build_cpu("Intel i9-13900K")
                 .build_ram("32GB DDR5")
                 .build_storage("2TB NVMe SSD")
                 .build_gpu("NVIDIA RTX 4090")
                 .build_motherboard("ASUS ROG Strix Z790")
                 .get_computer())
    
    logger.info("Gaming PC:")
    logger.info(f"  {gaming_pc}")
    
    office_builder = OfficeComputerBuilder()
    office_pc = (office_builder
                 .build_cpu("Intel i5-13400")
                 .build_ram("16GB DDR4")
                 .build_storage("512GB SSD")
                 .build_gpu("Integrated Graphics")
                 .get_computer())
    
    logger.info("\nOffice PC:")
    logger.info(f"  {office_pc}")
    logger.info()
    
    # Example 2: Using Director
    logger.info("Example 2: Using Director")
    logger.info("-" * 70)
    
    director = ComputerDirector(GamingComputerBuilder())
    pc1 = director.build_gaming_pc()
    logger.info(f"Director-built Gaming PC: {pc1}")
    
    director2 = ComputerDirector(OfficeComputerBuilder())
    pc2 = director2.build_office_pc()
    logger.info(f"Director-built Office PC: {pc2}")
    logger.info()
    
    # Example 3: Fluent Pizza Builder
    logger.info("Example 3: Fluent Pizza Builder")
    logger.info("-" * 70)
    
    pizza1 = (PizzaBuilder()
              .size("Large")
              .crust("Thin")
              .add_cheese()
              .add_pepperoni()
              .add_mushrooms()
              .build())
    
    logger.info(f"Pizza 1: {pizza1}")
    
    pizza2 = (PizzaBuilder()
              .size("Medium")
              .crust("Thick")
              .add_cheese()
              .add_bacon()
              .add_onions()
              .add_peppers()
              .build())
    
    logger.info(f"Pizza 2: {pizza2}")
    logger.info()
    
    # Example 4: SQL Query Builder
    logger.info("Example 4: SQL Query Builder")
    logger.info("-" * 70)
    
    query1 = (SQLQueryBuilder()
              .select("id", "name", "email")
              .from_table("users")
              .where("age > 18")
              .where("active = 1")
              .order_by("name")
              .limit(10)
              .build())
    
    logger.info(f"Query 1: {query1}")
    
    query2 = (SQLQueryBuilder()
              .select("*")
              .from_table("products")
              .where("price < 100")
              .order_by("price", "name")
              .build())
    
    logger.info(f"Query 2: {query2}")
    logger.info()
    
    # Example 5: Step-by-step building
    logger.debug("Example 5: Step-by-step Building")
    logger.info("-" * 70)
    
    builder = PizzaBuilder()
    builder.size("Large")
    builder.crust("Pan")
    builder.add_cheese()
    builder.add_pepperoni()
    
    # Can add more later
    builder.add_bacon()
    
    pizza = builder.build()
    logger.debug(f"Step-by-step built pizza: {pizza}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Separate the construction of a complex object from its")
    logger.info("  representation, allowing the same construction process")
    logger.info("  to create different representations.")
    logger.info("\nKey Advantages:")
    logger.debug("  - Step-by-step construction")
    logger.info("  - Reusable construction code")
    logger.info("  - Isolates complex construction")
    logger.info("  - Allows different representations")
    logger.info("  - Fluent interface support")
    logger.info("\nKey Disadvantages:")
    logger.info("  - More classes to maintain")
    logger.info("  - Can be overkill for simple objects")
    logger.info("  - Requires creating builder for each product type")
    logger.info("\nWhen to Use:")
    logger.info("  - Complex object construction")
    logger.info("  - Many optional parameters")
    logger.info("  - Need different representations")
    logger.debug("  - Step-by-step construction needed")
    logger.info("  - Immutable object construction")
    logger.info("\nWhen NOT to Use:")
    logger.info("  - Simple objects with few parameters")
    logger.info("  - All parameters are required")
    logger.info("  - Construction is straightforward")
    logger.info("\nBuilder vs Factory:")
    logger.debug("  - Builder: Step-by-step, complex objects")
    logger.debug("  - Factory: Single-step, simple objects")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Configuration objects")
    logger.info("  - Query builders (SQL, MongoDB)")
    logger.info("  - HTTP request builders")
    logger.info("  - Test data builders")
    logger.info("  - Document builders (HTML, XML)")
    logger.info("\nReal-world Examples:")
    logger.info("  - Java: StringBuilder, HttpRequest.Builder")
    logger.info("  - Python: SQLAlchemy query builder")
    logger.info("  - JavaScript: jQuery, Axios request builder")
    logger.info("  - Android: AlertDialog.Builder")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()