#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Joins implementation.

This file contains the implementation of the Joins algorithm.
"""

from typing import List, Optional, Dict, Set


class JoinOperations:
    """Database join operations."""

    def __init__(self):
        self.tables: Dict[str, List[dict]] = {}

    def create_table(self, table_name: str, data: List[dict]) -> None:
        """Create table."""
        self.tables[table_name] = data

    def inner_join(self, table1: str, table2: str, on: str) -> List[dict]:
        """Inner join."""
        if table1 not in self.tables or table2 not in self.tables:
            return []

        result = []
        for row1 in self.tables[table1]:
            for row2 in self.tables[table2]:
                if row1.get(on) == row2.get(on):
                    merged = {**row1, **row2}
                    result.append(merged)
        return result

    def left_join(self, table1: str, table2: str, on: str) -> List[dict]:
        """Left join."""
        if table1 not in self.tables or table2 not in self.tables:
            return []

        result = []
        for row1 in self.tables[table1]:
            matched = False
            for row2 in self.tables[table2]:
                if row1.get(on) == row2.get(on):
                    merged = {**row1, **row2}
                    result.append(merged)
                    matched = True
            if not matched:
                result.append(row1)
        return result


def main() -> None:
    """Demonstrate Joins."""
    print("=" * 70)
    print("JOINS")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Joins")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
