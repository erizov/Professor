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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("=" * 70)
    logger.info("REPOSITORY DESIGN PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: User Repository
    logger.info("Example 1: User Repository")
    logger.info("-" * 70)
    
    repository = InMemoryUserRepository()
    service = UserService(repository)
    
    # Create users
    user1 = service.create_user("Alice", "alice@example.com")
    user2 = service.create_user("Bob", "bob@example.com")
    user3 = service.create_user("Charlie", "charlie@example.com")
    
    logger.info(f"Created users:")
    for user in service.get_all_users():
        logger.info(f"  {user}")
    logger.info()
    
    # Get user by ID
    found = service.get_user(2)
    logger.info(f"User 2: {found}")
    logger.info()
    
    # Update user
    service.update_user_email(2, "robert@example.com")
    logger.info(f"Updated user 2: {service.get_user(2)}")
    logger.info()
    
    # Delete user
    service.delete_user(1)
    logger.info(f"After deleting user 1:")
    for user in service.get_all_users():
        logger.info(f"  {user}")
    logger.info()
    
    # Example 2: Product Repository
    logger.info("Example 2: Product Repository")
    logger.info("-" * 70)
    
    product_repo = InMemoryProductRepository()
    
    product_repo.add(Product(0, "Laptop", 999.99))
    product_repo.add(Product(0, "Mouse", 29.99))
    product_repo.add(Product(0, "Keyboard", 79.99))
    product_repo.add(Product(0, "Monitor", 299.99))
    
    # Find by name
    laptops = product_repo.find_by_name("laptop")
    logger.info("Products with 'laptop' in name:")
    for p in laptops:
        logger.info(f"  {p}")
    logger.info()
    
    # Find by price range
    affordable = product_repo.find_by_price_range(0, 100)
    logger.info("Products under $100:")
    for p in affordable:
        logger.info(f"  {p}")
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("Repository")
    
    def repository_operations():
        repo = InMemoryUserRepository()
        svc = UserService(repo)
        for i in range(100):
            svc.create_user(f"User{i}", f"user{i}@example.com")
        return len(svc.get_all_users())
    
    result, metrics = timer.measure(repository_operations)
    logger.info(f"Time to create 100 users: {metrics['execution_time_ms']:.3f} ms")
    logger.info(f"Users created: {result}")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Mediates between domain and data mapping layers, acting")
    logger.info("  like an in-memory domain object collection.")
    logger.info("\nKey Advantages:")
    logger.info("  - Abstraction over data access")
    logger.info("  - Testable (can use in-memory repository)")
    logger.info("  - Centralized data access logic")
    logger.info("  - Easy to swap implementations")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Additional abstraction layer")
    logger.info("  - Can be overkill for simple CRUD")
    logger.info("  - May hide important data access details")
    logger.info("\nWhen to Use:")
    logger.info("  - Complex data access logic")
    logger.info("  - Need to test business logic independently")
    logger.info("  - Multiple data sources")
    logger.info("  - Want to abstract data access")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Domain-Driven Design (DDD)")
    logger.info("  - ORM abstraction")
    logger.info("  - Testing with mock repositories")
    logger.info("  - Multi-database support")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()