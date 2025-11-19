#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Single Responsibility implementation.

This file contains the implementation of the Single Responsibility algorithm.
"""

from typing import List, Optional, Dict, Set


class SingleResponsibility:
    """Single Responsibility Principle example."""

    class UserRepository:
        """Handles user data."""

        def get_user(self, user_id: str) -> dict:
            return {"id": user_id, "name": "User"}

    class UserValidator:
        """Validates user data."""

        def validate(self, user: dict) -> bool:
            return "name" in user and user["name"]

    class UserService:
        """Orchestrates user operations."""

        def __init__(self):
            self.repository = SingleResponsibility.UserRepository()
            self.validator = SingleResponsibility.UserValidator()

        def get_validated_user(self, user_id: str) -> Optional[dict]:
            user = self.repository.get_user(user_id)
            if self.validator.validate(user):
                return user
            return None


def main() -> None:
    """Demonstrate Single Responsibility."""
    print("=" * 70)
    print("SINGLE RESPONSIBILITY")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Single Responsibility")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
