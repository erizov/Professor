#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Mapper Design Pattern.

A layer of mappers that moves data between objects and a database
while keeping them independent of each other and the mapper itself.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional, List, Dict

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


# Domain Object (no database knowledge)
class User:
    """User domain object - no database dependencies."""
    
    def __init__(self, user_id: int = 0, name: str = "", email: str = ""):
        self.user_id = user_id
        self.name = name
        self.email = email
    
    def __str__(self) -> str:
        return f"User(id={self.user_id}, name='{self.name}', email='{self.email}')"


# Data Transfer Object (database representation)
class UserDTO:
    """User Data Transfer Object - database representation."""
    
    def __init__(self, user_id: int, name: str, email: str, 
                 created_at: str = "", updated_at: str = ""):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserDTO':
        """Create from dictionary."""
        return cls(
            user_id=data.get('user_id', 0),
            name=data.get('name', ''),
            email=data.get('email', ''),
            created_at=data.get('created_at', ''),
            updated_at=data.get('updated_at', '')
        )


# Data Mapper
class UserMapper:
    """Maps between User domain object and UserDTO."""
    
    @staticmethod
    def to_dto(user: User) -> UserDTO:
        """Convert domain object to DTO."""
        return UserDTO(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            created_at="2024-01-01",  # Simulated
            updated_at="2024-01-01"
        )
    
    @staticmethod
    def to_domain(dto: UserDTO) -> User:
        """Convert DTO to domain object."""
        return User(
            user_id=dto.user_id,
            name=dto.name,
            email=dto.email
        )


# Data Access Layer (simulated database)
class UserDataAccess:
    """Simulated database access layer."""
    
    def __init__(self):
        self.storage: Dict[int, Dict] = {}
        self.next_id = 1
    
    def insert(self, dto: UserDTO) -> int:
        """Insert DTO into database."""
        if dto.user_id == 0:
            dto.user_id = self.next_id
            self.next_id += 1
        
        self.storage[dto.user_id] = dto.to_dict()
        print(f"  Database: Inserted user {dto.user_id}")
        return dto.user_id
    
    def find_by_id(self, user_id: int) -> Optional[UserDTO]:
        """Find DTO by ID."""
        data = self.storage.get(user_id)
        if data:
            return UserDTO.from_dict(data)
        return None
    
    def find_all(self) -> List[UserDTO]:
        """Find all DTOs."""
        return [UserDTO.from_dict(data) 
                for data in self.storage.values()]
    
    def update(self, dto: UserDTO) -> bool:
        """Update DTO in database."""
        if dto.user_id in self.storage:
            self.storage[dto.user_id] = dto.to_dict()
            print(f"  Database: Updated user {dto.user_id}")
            return True
        return False
    
    def delete(self, user_id: int) -> bool:
        """Delete DTO from database."""
        if user_id in self.storage:
            del self.storage[user_id]
            print(f"  Database: Deleted user {user_id}")
            return True
        return False


# Repository using Data Mapper
class UserRepository:
    """Repository using Data Mapper pattern."""
    
    def __init__(self, data_access: UserDataAccess):
        self.data_access = data_access
        self.mapper = UserMapper()
    
    def save(self, user: User) -> User:
        """Save user (domain object)."""
        dto = self.mapper.to_dto(user)
        user_id = self.data_access.insert(dto)
        user.user_id = user_id
        return user
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find user by ID."""
        dto = self.data_access.find_by_id(user_id)
        if dto:
            return self.mapper.to_domain(dto)
        return None
    
    def find_all(self) -> List[User]:
        """Find all users."""
        dtos = self.data_access.find_all()
        return [self.mapper.to_domain(dto) for dto in dtos]
    
    def update(self, user: User) -> bool:
        """Update user."""
        dto = self.mapper.to_dto(user)
        return self.data_access.update(dto)
    
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        return self.data_access.delete(user_id)


# Example 2: Product Data Mapper
class Product:
    """Product domain object."""
    
    def __init__(self, product_id: int = 0, name: str = "", price: float = 0.0):
        self.product_id = product_id
        self.name = name
        self.price = price
    
    def __str__(self) -> str:
        return f"Product(id={self.product_id}, name='{self.name}', price=${self.price:.2f})"


class ProductDTO:
    """Product DTO."""
    
    def __init__(self, product_id: int, name: str, price: float, 
                 category: str = ""):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
    
    def to_dict(self) -> Dict:
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'category': self.category
        }


class ProductMapper:
    """Product mapper."""
    
    @staticmethod
    def to_dto(product: Product) -> ProductDTO:
        return ProductDTO(
            product_id=product.product_id,
            name=product.name,
            price=product.price,
            category="General"  # Default
        )
    
    @staticmethod
    def to_domain(dto: ProductDTO) -> Product:
        return Product(
            product_id=dto.product_id,
            name=dto.name,
            price=dto.price
        )


def main() -> None:
    """Demonstration of Data Mapper Pattern."""
    print("=" * 70)
    print("DATA MAPPER DESIGN PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: User Data Mapper
    print("Example 1: User Data Mapper")
    print("-" * 70)
    
    data_access = UserDataAccess()
    repository = UserRepository(data_access)
    
    # Create domain objects (no database knowledge)
    user1 = User(0, "Alice", "alice@example.com")
    user2 = User(0, "Bob", "bob@example.com")
    
    print("Saving domain objects:")
    saved_user1 = repository.save(user1)
    saved_user2 = repository.save(user2)
    print()
    
    # Retrieve as domain objects
    print("Retrieving domain objects:")
    found = repository.find_by_id(1)
    print(f"  Found: {found}")
    print()
    
    # Get all users
    all_users = repository.find_all()
    print("All users:")
    for user in all_users:
        print(f"  {user}")
    print()
    
    # Update domain object
    saved_user1.name = "Alice Smith"
    repository.update(saved_user1)
    print()
    
    updated = repository.find_by_id(1)
    print(f"Updated user: {updated}")
    print()
    
    # Example 2: Product Data Mapper
    print("Example 2: Product Data Mapper")
    print("-" * 70)
    
    product_data = {}
    product_next_id = 1
    
    def save_product(product: Product) -> Product:
        nonlocal product_next_id
        if product.product_id == 0:
            product.product_id = product_next_id
            product_next_id += 1
        
        dto = ProductMapper.to_dto(product)
        product_data[product.product_id] = dto.to_dict()
        return product
    
    def find_product(product_id: int) -> Optional[Product]:
        data = product_data.get(product_id)
        if data:
            dto = ProductDTO(**data)
            return ProductMapper.to_domain(dto)
        return None
    
    product1 = Product(0, "Laptop", 999.99)
    product1 = save_product(product1)
    
    product2 = Product(0, "Mouse", 29.99)
    product2 = save_product(product2)
    
    print("Products saved:")
    print(f"  {product1}")
    print(f"  {product2}")
    print()
    
    found_product = find_product(1)
    print(f"Retrieved product: {found_product}")
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Data Mapper")
    
    def mapper_operations():
        data_access = UserDataAccess()
        repo = UserRepository(data_access)
        
        for i in range(50):
            user = User(0, f"User{i}", f"user{i}@example.com")
            repo.save(user)
        
        return len(repo.find_all())
    
    result, metrics = timer.measure(mapper_operations)
    print(f"Time to save and retrieve 50 users: "
          f"{metrics['execution_time_ms']:.3f} ms")
    print(f"Users processed: {result}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  A layer of mappers that moves data between objects and")
    print("  a database while keeping them independent of each other.")
    print("\nKey Advantages:")
    print("  - Domain objects have no database dependencies")
    print("  - Database schema changes don't affect domain")
    print("  - Clear separation of concerns")
    print("  - Easy to test domain objects")
    print("\nKey Disadvantages:")
    print("  - More code to maintain")
    print("  - Additional mapping layer")
    print("  - Can be complex for simple cases")
    print("\nWhen to Use:")
    print("  - Domain objects should be database-agnostic")
    print("  - Complex domain model")
    print("  - Database schema differs from domain model")
    print("  - Need to support multiple data sources")
    print("\nCommon Use Cases:")
    print("  - ORM frameworks")
    print("  - Domain-Driven Design")
    print("  - Legacy database integration")
    print("  - Multi-database support")
    print("=" * 70)


if __name__ == "__main__":
    main()
