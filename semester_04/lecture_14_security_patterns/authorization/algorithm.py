#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authorization implementation.

This file contains the implementation of the Authorization algorithm.
"""

from typing import List, Optional, Dict, Set


class Authorization:
    """Authorization system (RBAC - Role-Based Access Control)."""

    def __init__(self):
        self.user_roles: Dict[str, List[str]] = {}  # user -> roles
        self.role_permissions: Dict[str, List[str]] = {}  # role -> permissions
        self.resource_permissions: Dict[str, List[str]] = (
            {}
        )  # resource -> required permissions

    def assign_role(self, user: str, role: str) -> None:
        """Assign role to user."""
        if user not in self.user_roles:
            self.user_roles[user] = []
        if role not in self.user_roles[user]:
            self.user_roles[user].append(role)

    def grant_permission(self, role: str, permission: str) -> None:
        """Grant permission to role."""
        if role not in self.role_permissions:
            self.role_permissions[role] = []
        if permission not in self.role_permissions[role]:
            self.role_permissions[role].append(permission)

    def set_resource_permissions(self, resource: str, permissions: List[str]) -> None:
        """Set required permissions for resource."""
        self.resource_permissions[resource] = permissions

    def check_access(self, user: str, resource: str) -> bool:
        """Check if user has access to resource."""
        if resource not in self.resource_permissions:
            return True  # No restrictions

        required_permissions = self.resource_permissions[resource]
        user_roles = self.user_roles.get(user, [])

        user_permissions = set()
        for role in user_roles:
            user_permissions.update(self.role_permissions.get(role, []))

        return all(perm in user_permissions for perm in required_permissions)


def main() -> None:
    """Demonstrate Authorization."""
    print("=" * 70)
    print("AUTHORIZATION")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Authorization")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
