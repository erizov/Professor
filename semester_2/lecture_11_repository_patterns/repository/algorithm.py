#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repository Design Pattern.

Mediates between the domain and data mapping layers, acting like an
in-memory domain object collection. Provides abstraction over data access.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Optional

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


# Domain Entity
class User:
    """User domain entity."""
    
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
        """Add user."""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[User]:
        """Get all users."""
        pass
    
    @abstractmethod
    def update(self, user: User) -> bool:
        """Update user."""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        pass


# In-Memory Repository Implementation
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
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.users.get(user_id)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        for user in self.users.values():
            if user.email == email:
                return user
        return None
    
    def get_all(self) -> List[User]:
        """Get all users."""
        return list(self.users.values())
    
    def update(self, user: User) -> bool:
        """Update user."""
        if user.user_id in self.users:
            self.users[user.user_id] = user
            return True
        return False
    
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False


# Service Layer (uses repository)
class UserService:
    """User service - business logic."""
    
    def __init__(self, repository: IUserRepository):
        self.repository = repository
    
    def create_user(self, name: str, email: str) -> User:
        """Create user with validation."""
        # Check if email already exists
        existing = self.repository.get_by_email(email)
        if existing:
            raise ValueError(f"User with email {email} already exists")
        
        user = User(0, name, email)
        self.repository.add(user)
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.repository.get_by_id(user_id)
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        return self.repository.get_all()
    
    def update_user_email(self, user_id: int, new_email: str) -> bool:
        """Update user email."""
        user = self.repository.get_by_id(user_id)
        if not user:
            return False
        
        # Check if new email is already taken
        existing = self.repository.get_by_email(new_email)
        if existing and existing.user_id != user_id:
            raise ValueError(f"Email {new_email} already in use")
        
        user.email = new_email
        return self.repository.update(user)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        return self.repository.delete(user_id)


# Example 2: Product Repository
class Product:
    """Product entity."""
    
    def __init__(self, product_id: int, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price
    
    def __str__(self) -> str:
        return f"Product(id={self.product_id}, name='{self.name}', price=${self.price:.2f})"


class IProductRepository(ABC):
    """Product repository interface."""
    
    @abstractmethod
    def add(self, product: Product) -> None:
        pass
    
    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> List[Product]:
        pass
    
    @abstractmethod
    def find_by_price_range(self, min_price: float, 
                           max_price: float) -> List[Product]:
        pass


class InMemoryProductRepository(IProductRepository):
    """In-memory product repository."""
    
    def __init__(self):
        self.products: dict[int, Product] = {}
        self.next_id = 1
    
    def add(self, product: Product) -> None:
        if product.product_id == 0:
            product.product_id = self.next_id
            self.next_id += 1
        self.products[product.product_id] = product
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.products.get(product_id)
    
    def find_by_name(self, name: str) -> List[Product]:
        return [p for p in self.products.values() 
                if name.lower() in p.name.lower()]
    
    def find_by_price_range(self, min_price: float, 
                           max_price: float) -> List[Product]:
        return [p for p in self.products.values() 
                if min_price <= p.price <= max_price]


def main() -> None:
    """Demonstration of Repository Pattern."""
    print("=" * 70)
    print("REPOSITORY DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: User Repository
    print("Example 1: User Repository")
    print("-" * 70)
    
    repository = InMemoryUserRepository()
    service = UserService(repository)
    
    # Create users
    user1 = service.create_user("Alice", "alice@example.com")
    user2 = service.create_user("Bob", "bob@example.com")
    user3 = service.create_user("Charlie", "charlie@example.com")
    
    print(f"Created users:")
    for user in service.get_all_users():
        print(f"  {user}")
    print()
    
    # Get user by ID
    found = service.get_user(2)
    print(f"User 2: {found}")
    print()
    
    # Update user
    service.update_user_email(2, "robert@example.com")
    print(f"Updated user 2: {service.get_user(2)}")
    print()
    
    # Delete user
    service.delete_user(1)
    print(f"After deleting user 1:")
    for user in service.get_all_users():
        print(f"  {user}")
    print()
    
    # Example 2: Product Repository
    print("Example 2: Product Repository")
    print("-" * 70)
    
    product_repo = InMemoryProductRepository()
    
    product_repo.add(Product(0, "Laptop", 999.99))
    product_repo.add(Product(0, "Mouse", 29.99))
    product_repo.add(Product(0, "Keyboard", 79.99))
    product_repo.add(Product(0, "Monitor", 299.99))
    
    # Find by name
    laptops = product_repo.find_by_name("laptop")
    print("Products with 'laptop' in name:")
    for p in laptops:
        print(f"  {p}")
    print()
    
    # Find by price range
    affordable = product_repo.find_by_price_range(0, 100)
    print("Products under $100:")
    for p in affordable:
        print(f"  {p}")
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Repository")
    
    def repository_operations():
        repo = InMemoryUserRepository()
        svc = UserService(repo)
        for i in range(100):
            svc.create_user(f"User{i}", f"user{i}@example.com")
        return len(svc.get_all_users())
    
    result, metrics = timer.measure(repository_operations)
    print(f"Time to create 100 users: {metrics['execution_time_ms']:.3f} ms")
    print(f"Users created: {result}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Mediates between domain and data mapping layers, acting")
    print("  like an in-memory domain object collection.")
    print("\nKey Advantages:")
    print("  - Abstraction over data access")
    print("  - Testable (can use in-memory repository)")
    print("  - Centralized data access logic")
    print("  - Easy to swap implementations")
    print("\nKey Disadvantages:")
    print("  - Additional abstraction layer")
    print("  - Can be overkill for simple CRUD")
    print("  - May hide important data access details")
    print("\nWhen to Use:")
    print("  - Complex data access logic")
    print("  - Need to test business logic independently")
    print("  - Multiple data sources")
    print("  - Want to abstract data access")
    print("\nCommon Use Cases:")
    print("  - Domain-Driven Design (DDD)")
    print("  - ORM abstraction")
    print("  - Testing with mock repositories")
    print("  - Multi-database support")
    print("=" * 70)


if __name__ == "__main__":
    main()
