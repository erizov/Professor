#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Masking implementation.

This file contains the implementation of the Data Masking algorithm.
"""

from typing import List, Optional, Dict, Set


def data_masking(data: str, mask_char: str = "*") -> str:
    """Mask sensitive data."""
    if len(data) <= 4:
        return mask_char * len(data)
    return data[:2] + mask_char * (len(data) - 4) + data[-2:]


class DataMasking:
    """Data masking utility."""

    def __init__(self):
        self.masking_rules: Dict[str, callable] = {}

    def add_rule(self, field_name: str, mask_func: callable) -> None:
        """Add masking rule."""
        self.masking_rules[field_name] = mask_func

    def mask_record(self, record: dict) -> dict:
        """Mask record."""
        masked = record.copy()
        for field, mask_func in self.masking_rules.items():
            if field in masked:
                masked[field] = mask_func(masked[field])
        return masked


def main() -> None:
    """Demonstrate Data Masking."""
    print("=" * 70)
    print("DATA MASKING")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Data Masking")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
