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
        
    """
    Builder implementation.
    
    Args:
        *args: Variable arguments
        **kwargs: Keyword arguments
        
    Returns:
        Algorithm result
    """
    # Implementation for builder
    logger.info(f"Executing builder")
    return None


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