#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit of Work Design Pattern.

Maintains a list of objects affected by a business transaction and
coordinates writing out changes and resolving concurrency problems.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Set, Optional
from enum import Enum

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class EntityState(Enum):
    """Entity state in unit of work."""
    NEW = "new"
    MODIFIED = "modified"
    DELETED = "deleted"
    UNCHANGED = "unchanged"


# Domain Entity
class User:
    """User entity."""
    
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
    
    def __str__(self) -> str:
        return f"User(id={self.user_id}, name='{self.name}', email='{self.email}')"


# Repository Interface
class IUserRepository(ABC):
    """User repository interface."""
    
    @abstractmethod
    def add(self, user: User) -> None:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def update(self, user: User) -> None:
        pass
    
    @abstractmethod
    def delete(self, user: User) -> None:
        pass


# Unit of Work
class UnitOfWork:
    """Unit of Work - tracks changes and commits atomically."""
    
    def __init__(self, repository: IUserRepository):
        self.repository = repository
        self.new_entities: Set[User] = set()
        self.modified_entities: Set[User] = set()
        self.deleted_entities: Set[User] = set()
    
    def register_new(self, entity: User) -> None:
        """Register new entity."""
        if entity in self.deleted_entities:
            self.deleted_entities.remove(entity)
        if entity not in self.modified_entities:
            self.new_entities.add(entity)
    
    def register_modified(self, entity: User) -> None:
        """Register modified entity."""
        if entity not in self.new_entities and entity not in self.deleted_entities:
            self.modified_entities.add(entity)
    
    def register_deleted(self, entity: User) -> None:
        """Register deleted entity."""
        if entity in self.new_entities:
            self.new_entities.remove(entity)
        if entity in self.modified_entities:
            self.modified_entities.remove(entity)
        if entity not in self.deleted_entities:
            self.deleted_entities.add(entity)
    
    def commit(self) -> None:
        """Commit all changes atomically."""
        try:
            # Insert new entities
            for entity in self.new_entities:
                self.repository.add(entity)
            
            # Update modified entities
            for entity in self.modified_entities:
                self.repository.update(entity)
            
            # Delete entities
            for entity in self.deleted_entities:
                self.repository.delete(entity)
            
            # Clear tracking
            self.new_entities.clear()
            self.modified_entities.clear()
            self.deleted_entities.clear()
            
            print("Unit of Work committed successfully")
        except Exception as e:
            print(f"Error committing Unit of Work: {e}")
            raise
    
    def rollback(self) -> None:
        """Rollback all changes."""
        self.new_entities.clear()
        self.modified_entities.clear()
        self.deleted_entities.clear()
        print("Unit of Work rolled back")


# In-Memory Repository
class InMemoryUserRepository(IUserRepository):
    """In-memory user repository."""
    
    def __init__(self):
        self.users: dict[int, User] = {}
        self.next_id = 1
    
    def add(self, user: User) -> None:
        """Add user."""
        if user.user_id == 0:
            user.user_id = self.next_id
            self.next_id += 1
        self.users[user.user_id] = user
        print(f"  Added: {user}")
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)
    
    def update(self, user: User) -> None:
        """Update user."""
        if user.user_id in self.users:
            self.users[user.user_id] = user
            print(f"  Updated: {user}")
    
    def delete(self, user: User) -> None:
        """Delete user."""
        if user.user_id in self.users:
            del self.users[user.user_id]
            print(f"  Deleted: {user}")


# Service using Unit of Work
class UserService:
    """User service using Unit of Work."""
    
    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work
    
    def create_user(self, name: str, email: str) -> User:
        """Create user."""
        user = User(0, name, email)
        self.unit_of_work.register_new(user)
        return user
    
    def update_user(self, user: User, name: str = None, 
                   email: str = None) -> None:
        """Update user."""
        if name:
            user.name = name
        if email:
            user.email = email
        self.unit_of_work.register_modified(user)
    
    def delete_user(self, user: User) -> None:
        """Delete user."""
        self.unit_of_work.register_deleted(user)
    
    def commit(self) -> None:
        """Commit changes."""
        self.unit_of_work.commit()


def main() -> None:
    """Demonstration of Unit of Work Pattern."""
    print("=" * 70)
    print("UNIT OF WORK DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic Unit of Work
    print("Example 1: Basic Unit of Work")
    print("-" * 70)
    
    repository = InMemoryUserRepository()
    unit_of_work = UnitOfWork(repository)
    service = UserService(unit_of_work)
    
    # Create multiple users
    user1 = service.create_user("Alice", "alice@example.com")
    user2 = service.create_user("Bob", "bob@example.com")
    user3 = service.create_user("Charlie", "charlie@example.com")
    
    print("Changes registered (not yet committed):")
    print(f"  New entities: {len(unit_of_work.new_entities)}")
    print()
    
    # Commit all changes atomically
    print("Committing Unit of Work:")
    service.commit()
    print()
    
    # Example 2: Update and Delete
    print("Example 2: Update and Delete Operations")
    print("-" * 70)
    
    # Get existing user
    existing_user = repository.get_by_id(2)
    if existing_user:
        # Update
        service.update_user(existing_user, name="Robert")
        
        # Delete another user
        user_to_delete = repository.get_by_id(3)
        if user_to_delete:
            service.delete_user(user_to_delete)
        
        print("Changes registered:")
        print(f"  Modified: {len(unit_of_work.modified_entities)}")
        print(f"  Deleted: {len(unit_of_work.deleted_entities)}")
        print()
        
        print("Committing changes:")
        service.commit()
        print()
    
    # Example 3: Transaction Rollback
    print("Example 3: Transaction Rollback")
    print("-" * 70)
    
    # Register some changes
    user4 = service.create_user("Diana", "diana@example.com")
    user5 = service.create_user("Eve", "eve@example.com")
    
    print(f"Changes registered: {len(unit_of_work.new_entities)} new entities")
    print("Rolling back (not committing):")
    unit_of_work.rollback()
    print()
    
    # Verify nothing was committed
    all_users = [repository.get_by_id(i) for i in range(1, 10)]
    all_users = [u for u in all_users if u]
    print(f"Users in repository after rollback: {len(all_users)}")
    for user in all_users:
        print(f"  {user}")
    print()
    
    # Example 4: Performance measurement
    print("Example 4: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Unit of Work")
    
    def unit_of_work_operations():
        repo = InMemoryUserRepository()
        uow = UnitOfWork(repo)
        svc = UserService(uow)
        
        for i in range(50):
            svc.create_user(f"User{i}", f"user{i}@example.com")
        svc.commit()
        return len(repo.users)
    
    result, metrics = timer.measure(unit_of_work_operations)
    print(f"Time to create and commit 50 users: "
          f"{metrics['execution_time_ms']:.3f} ms")
    print(f"Users committed: {result}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Maintains a list of objects affected by a business")
    print("  transaction and coordinates writing out changes and")
    print("  resolving concurrency problems.")
    print("\nKey Advantages:")
    print("  - Atomic transactions")
    print("  - Tracks all changes")
    print("  - Prevents inconsistent state")
    print("  - Batch operations")
    print("\nKey Disadvantages:")
    print("  - More complex than simple repository")
    print("  - Memory overhead for tracking")
    print("  - Can be overkill for simple operations")
    print("\nWhen to Use:")
    print("  - Need atomic transactions")
    print("  - Multiple related changes")
    print("  - Complex business transactions")
    print("  - Need to track all changes")
    print("\nCommon Use Cases:")
    print("  - ORM frameworks (Entity Framework, Hibernate)")
    print("  - Domain-Driven Design")
    print("  - Complex business transactions")
    print("  - Batch operations")
    print("=" * 70)


if __name__ == "__main__":
    main()
