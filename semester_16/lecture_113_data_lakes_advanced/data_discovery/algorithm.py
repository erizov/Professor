#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Discovery implementation.

This file contains the implementation of the Data Discovery algorithm.
"""

from typing import List, Optional, Dict, Set


class DataDiscovery:
    """Data discovery system."""

    def __init__(self):
        self.data_sources: Dict[str, dict] = {}
        self.index: Dict[str, List[str]] = {}

    def register_source(
        self, source_id: str, name: str, location: str, schema: dict
    ) -> None:
        """Register data source."""
        self.data_sources[source_id] = {
            "name": name,
            "location": location,
            "schema": schema,
        }

        # Index schema fields
        for field_name in schema.keys():
            if field_name not in self.index:
                self.index[field_name] = []
            if source_id not in self.index[field_name]:
                self.index[field_name].append(source_id)

    def discover_by_field(self, field_name: str) -> List[str]:
        """Discover sources by field name."""
        return self.index.get(field_name, [])

    def discover_by_name(self, name_pattern: str) -> List[str]:
        """Discover sources by name pattern."""
        results = []
        name_lower = name_pattern.lower()
        for source_id, source in self.data_sources.items():
            if name_lower in source["name"].lower():
                results.append(source_id)
        return results

    def get_source_info(self, source_id: str) -> Optional[dict]:
        """Get source information."""
        return self.data_sources.get(source_id)


def main() -> None:
    """Demonstrate Data Discovery."""
    print("=" * 70)
    print("DATA DISCOVERY")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Data Discovery")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
