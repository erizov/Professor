#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authorization Pattern.

Determines what actions a user is allowed to perform after authentication.
Controls access to resources based on user roles and permissions.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Set, Dict, Optional
from enum import Enum

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class Permission(Enum):
    """Permission types."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"


class Role:
    """User role with permissions."""
    
    def __init__(self, name: str, permissions: Set[Permission]):
        self.name = name
        self.permissions = permissions
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if role has permission."""
        return permission in self.permissions


class User:
    """User with roles."""
    
    def __init__(self, user_id: str, username: str, roles: List[Role]):
        self.user_id = user_id
        self.username = username
        self.roles = roles
    
    def has_permission(self, permission: Permission) -> bool:
        """Check if user has permission through any role."""
        return any(role.has_permission(permission) for role in self.roles)
    
    def has_role(self, role_name: str) -> bool:
        """Check if user has role."""
        return any(role.name == role_name for role in self.roles)


class AuthorizationService:
    """Authorization service."""
    
    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
    
    def create_role(self, name: str, permissions: Set[Permission]) -> Role:
        """Create role."""
        role = Role(name, permissions)
        self.roles[name] = role
        return role
    
    def create_user(self, user_id: str, username: str, role_names: List[str]) -> User:
        """Create user with roles."""
        roles = [self.roles[name] for name in role_names if name in self.roles]
        user = User(user_id, username, roles)
        self.users[user_id] = user
        return user
    
    def authorize(self, user_id: str, permission: Permission) -> bool:
        """Authorize user action."""
        if user_id not in self.users:
            return False
        return self.users[user_id].has_permission(permission)
    
    def check_access(self, user_id: str, resource: str, action: Permission) -> bool:
        """Check if user can perform action on resource."""
        return self.authorize(user_id, action)


# Example 2: RBAC (Role-Based Access Control)
class RBAC:
    """Role-Based Access Control."""
    
    def __init__(self):
        self.roles: Dict[str, Set[str]] = {}  # role -> permissions
        self.user_roles: Dict[str, Set[str]] = {}  # user -> roles
    
    def add_role(self, role: str, permissions: List[str]) -> None:
        """Add role with permissions."""
        self.roles[role] = set(permissions)
    
    def assign_role(self, user_id: str, role: str) -> None:
        """Assign role to user."""
        if user_id not in self.user_roles:
            self.user_roles[user_id] = set()
        self.user_roles[user_id].add(role)
    
    def has_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has permission."""
        if user_id not in self.user_roles:
            return False
        
        for role in self.user_roles[user_id]:
            if role in self.roles and permission in self.roles[role]:
                return True
        return False


def main() -> None:
    """Demonstration of Authorization Pattern."""
    print("=" * 70)
    print("AUTHORIZATION PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Role-based Authorization
    print("Example 1: Role-based Authorization")
    print("-" * 70)
    
    authz = AuthorizationService()
    
    # Create roles
    admin_role = authz.create_role("admin", {
        Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN
    })
    editor_role = authz.create_role("editor", {
        Permission.READ, Permission.WRITE
    })
    viewer_role = authz.create_role("viewer", {Permission.READ})
    
    print("Created roles:")
    print(f"  Admin: {[p.value for p in admin_role.permissions]}")
    print(f"  Editor: {[p.value for p in editor_role.permissions]}")
    print(f"  Viewer: {[p.value for p in viewer_role.permissions]}")
    print()
    
    # Create users
    admin_user = authz.create_user("u1", "alice", ["admin"])
    editor_user = authz.create_user("u2", "bob", ["editor"])
    viewer_user = authz.create_user("u3", "charlie", ["viewer"])
    
    # Check permissions
    print("Permission checks:")
    print(f"Alice (admin) can delete: {authz.authorize('u1', Permission.DELETE)}")
    print(f"Bob (editor) can write: {authz.authorize('u2', Permission.WRITE)}")
    print(f"Bob (editor) can delete: {authz.authorize('u2', Permission.DELETE)}")
    print(f"Charlie (viewer) can read: {authz.authorize('u3', Permission.READ)}")
    print(f"Charlie (viewer) can write: {authz.authorize('u3', Permission.WRITE)}")
    print()
    
    # Example 2: RBAC
    print("Example 2: RBAC (Role-Based Access Control)")
    print("-" * 70)
    
    rbac = RBAC()
    
    rbac.add_role("admin", ["read", "write", "delete", "manage"])
    rbac.add_role("user", ["read", "write"])
    rbac.add_role("guest", ["read"])
    
    rbac.assign_role("user1", "admin")
    rbac.assign_role("user2", "user")
    rbac.assign_role("user3", "guest")
    
    print("Permission checks:")
    print(f"User1 (admin) can delete: {rbac.has_permission('user1', 'delete')}")
    print(f"User2 (user) can write: {rbac.has_permission('user2', 'write')}")
    print(f"User2 (user) can delete: {rbac.has_permission('user2', 'delete')}")
    print(f"User3 (guest) can read: {rbac.has_permission('user3', 'read')}")
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Authorization")
    
    def authz_operations():
        authz = AuthorizationService()
        authz.create_role("role1", {Permission.READ, Permission.WRITE})
        for i in range(100):
            authz.create_user(f"u{i}", f"user{i}", ["role1"])
        return authz.authorize("u50", Permission.READ)
    
    result, metrics = timer.measure(authz_operations)
    print(f"Time to create 100 users and check permission: "
          f"{metrics['execution_time_ms']:.3f} ms")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Determines what actions a user is allowed to perform")
    print("  after authentication. Controls access to resources.")
    print("\nKey Advantages:")
    print("  - Fine-grained access control")
    print("  - Role-based management")
    print("  - Centralized authorization")
    print("  - Scalable permissions")
    print("\nKey Disadvantages:")
    print("  - Complex permission management")
    print("  - Performance overhead")
    print("  - Can be over-engineered")
    print("\nWhen to Use:")
    print("  - Multi-user systems")
    print("  - Need fine-grained permissions")
    print("  - Role-based access")
    print("  - Enterprise applications")
    print("\nCommon Use Cases:")
    print("  - Web applications")
    print("  - Enterprise systems")
    print("  - Cloud services")
    print("  - API access control")
    print("=" * 70)


if __name__ == "__main__":
    main()
