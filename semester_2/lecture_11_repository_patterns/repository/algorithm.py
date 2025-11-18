#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repository implementation.

This file contains the implementation of the Repository algorithm.
"""

from typing import List, Optional, Dict, Set


class Entity:
    """Entity class."""
    def __init__(self, id: int, data: str):
        self.id = id
        self.data = data

class Repository:
    """Repository pattern implementation."""
    def __init__(self):
        self.entities: Dict[int, Entity] = {}
    
    def add(self, entity: Entity) -> None:
        """Add entity."""
        self.entities[entity.id] = entity
    
    def get_by_id(self, id: int) -> Optional[Entity]:
        """Get entity by ID."""
        return self.entities.get(id)
    
    def get_all(self) -> List[Entity]:
        """Get all entities."""
        return list(self.entities.values())
    
    def remove(self, id: int) -> bool:
        """Remove entity."""
        if id in self.entities:
            del self.entities[id]
            return True
        return False


def main() -> None:
    """Demonstrate Repository."""
    print("=" * 70)
    print("REPOSITORY")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Repository")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
