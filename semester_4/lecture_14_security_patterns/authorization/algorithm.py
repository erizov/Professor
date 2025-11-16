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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("=" * 70)
    logger.info("AUTHORIZATION PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Role-based Authorization
    logger.info("Example 1: Role-based Authorization")
    logger.info("-" * 70)
    
    authz = AuthorizationService()
    
    # Create roles
    admin_role = authz.create_role("admin", {
        Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN
    })
    editor_role = authz.create_role("editor", {
        Permission.READ, Permission.WRITE
    })
    viewer_role = authz.create_role("viewer", {Permission.READ})
    
    logger.info("Created roles:")
    logger.info(f"  Admin: {[p.value for p in admin_role.permissions]}")
    logger.info(f"  Editor: {[p.value for p in editor_role.permissions]}")
    logger.info(f"  Viewer: {[p.value for p in viewer_role.permissions]}")
    logger.info()
    
    # Create users
    admin_user = authz.create_user("u1", "alice", ["admin"])
    editor_user = authz.create_user("u2", "bob", ["editor"])
    viewer_user = authz.create_user("u3", "charlie", ["viewer"])
    
    # Check permissions
    logger.info("Permission checks:")
    logger.info(f"Alice (admin) can delete: {authz.authorize('u1', Permission.DELETE)}")
    logger.info(f"Bob (editor) can write: {authz.authorize('u2', Permission.WRITE)}")
    logger.info(f"Bob (editor) can delete: {authz.authorize('u2', Permission.DELETE)}")
    logger.info(f"Charlie (viewer) can read: {authz.authorize('u3', Permission.READ)}")
    logger.info(f"Charlie (viewer) can write: {authz.authorize('u3', Permission.WRITE)}")
    logger.info()
    
    # Example 2: RBAC
    logger.info("Example 2: RBAC (Role-Based Access Control)")
    logger.info("-" * 70)
    
    rbac = RBAC()
    
    rbac.add_role("admin", ["read", "write", "delete", "manage"])
    rbac.add_role("user", ["read", "write"])
    rbac.add_role("guest", ["read"])
    
    rbac.assign_role("user1", "admin")
    rbac.assign_role("user2", "user")
    rbac.assign_role("user3", "guest")
    
    logger.info("Permission checks:")
    logger.info(f"User1 (admin) can delete: {rbac.has_permission('user1', 'delete')}")
    logger.info(f"User2 (user) can write: {rbac.has_permission('user2', 'write')}")
    logger.info(f"User2 (user) can delete: {rbac.has_permission('user2', 'delete')}")
    logger.info(f"User3 (guest) can read: {rbac.has_permission('user3', 'read')}")
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Authorization")
    
    def authz_operations():
        authz = AuthorizationService()
        authz.create_role("role1", {Permission.READ, Permission.WRITE})
        for i in range(100):
            authz.create_user(f"u{i}", f"user{i}", ["role1"])
        return authz.authorize("u50", Permission.READ)
    
    result, metrics = timer.measure(authz_operations)
    logger.info(f"Time to create 100 users and check permission: "
          f"{metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Determines what actions a user is allowed to perform")
    logger.info("  after authentication. Controls access to resources.")
    logger.info("\nKey Advantages:")
    logger.info("  - Fine-grained access control")
    logger.info("  - Role-based management")
    logger.info("  - Centralized authorization")
    logger.info("  - Scalable permissions")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Complex permission management")
    logger.info("  - Performance overhead")
    logger.info("  - Can be over-engineered")
    logger.info("\nWhen to Use:")
    logger.info("  - Multi-user systems")
    logger.info("  - Need fine-grained permissions")
    logger.info("  - Role-based access")
    logger.info("  - Enterprise applications")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Web applications")
    logger.info("  - Enterprise systems")
    logger.info("  - Cloud services")
    logger.info("  - API access control")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()