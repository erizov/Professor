#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CQRS (Command Query Responsibility Segregation) Pattern.

Separates read and write operations into different models. Commands
change state, queries read state. This allows independent scaling
and optimization of read and write operations.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


# Domain Models
@dataclass
class User:
    """User domain model."""
    user_id: int
    name: str
    email: str
    created_at: datetime


# Commands (Write Operations)
class Command(ABC):
    """Base command interface."""
    pass


@dataclass
class CreateUserCommand(Command):
    """Create user command."""
    name: str
    email: str


@dataclass
class UpdateUserCommand(Command):
    """Update user command."""
    user_id: int
    name: Optional[str] = None
    email: Optional[str] = None


@dataclass
class DeleteUserCommand(Command):
    """Delete user command."""
    user_id: int


# Command Handler
class CommandHandler:
    """Handles commands (write operations)."""
    
    def __init__(self):
        self.write_store: dict[int, User] = {}
        self.next_id = 1
    
    def handle_create_user(self, command: CreateUserCommand) -> int:
        """Handle create user command."""
        user = User(
            user_id=self.next_id,
            name=command.name,
            email=command.email,
            created_at=datetime.now()
        )
        self.next_id += 1
        self.write_store[user.user_id] = user
        print(f"[Command] Created user: {user}")
        return user.user_id
    
    def handle_update_user(self, command: UpdateUserCommand) -> bool:
        """Handle update user command."""
        if command.user_id not in self.write_store:
            return False
        
        user = self.write_store[command.user_id]
        if command.name:
            user.name = command.name
        if command.email:
            user.email = command.email
        print(f"[Command] Updated user: {user}")
        return True
    
    def handle_delete_user(self, command: DeleteUserCommand) -> bool:
        """Handle delete user command."""
        if command.user_id in self.write_store:
            del self.write_store[command.user_id]
            print(f"[Command] Deleted user: {command.user_id}")
            return True
        return False


# Queries (Read Operations)
class Query(ABC):
    """Base query interface."""
    pass


@dataclass
class GetUserQuery(Query):
    """Get user query."""
    user_id: int


@dataclass
class GetAllUsersQuery(Query):
    """Get all users query."""
    pass


@dataclass
class SearchUsersQuery(Query):
    """Search users query."""
    name_pattern: Optional[str] = None
    email_pattern: Optional[str] = None


# Query Handler (Read Model)
class QueryHandler:
    """Handles queries (read operations)."""
    
    def __init__(self, write_store: dict):
        # Read model (can be optimized/cached/denormalized)
        self.read_store = write_store  # Simplified: same store
    
    def handle_get_user(self, query: GetUserQuery) -> Optional[User]:
        """Handle get user query."""
        user = self.read_store.get(query.user_id)
        if user:
            print(f"[Query] Retrieved user: {user}")
        return user
    
    def handle_get_all_users(self, query: GetAllUsersQuery) -> List[User]:
        """Handle get all users query."""
        users = list(self.read_store.values())
        print(f"[Query] Retrieved {len(users)} users")
        return users
    
    def handle_search_users(self, query: SearchUsersQuery) -> List[User]:
        """Handle search users query."""
        results = []
        for user in self.read_store.values():
            match = True
            if query.name_pattern and query.name_pattern.lower() not in user.name.lower():
                match = False
            if query.email_pattern and query.email_pattern.lower() not in user.email.lower():
                match = False
            if match:
                results.append(user)
        print(f"[Query] Found {len(results)} users matching search")
        return results


# CQRS Service
class CQRSService:
    """CQRS service coordinating commands and queries."""
    
    def __init__(self):
        self.command_handler = CommandHandler()
        self.query_handler = QueryHandler(self.command_handler.write_store)
    
    def execute_command(self, command: Command) -> Any:
        """Execute command."""
        if isinstance(command, CreateUserCommand):
            return self.command_handler.handle_create_user(command)
        elif isinstance(command, UpdateUserCommand):
            return self.command_handler.handle_update_user(command)
        elif isinstance(command, DeleteUserCommand):
            return self.command_handler.handle_delete_user(command)
        else:
            raise ValueError(f"Unknown command: {type(command)}")
    
    def execute_query(self, query: Query) -> Any:
        """Execute query."""
        if isinstance(query, GetUserQuery):
            return self.query_handler.handle_get_user(query)
        elif isinstance(query, GetAllUsersQuery):
            return self.query_handler.handle_get_all_users(query)
        elif isinstance(query, SearchUsersQuery):
            return self.query_handler.handle_search_users(query)
        else:
            raise ValueError(f"Unknown query: {type(query)}")


# Example 2: Order CQRS
@dataclass
class Order:
    """Order domain model."""
    order_id: int
    customer_id: int
    items: List[str]
    total: float
    status: str


@dataclass
class CreateOrderCommand(Command):
    """Create order command."""
    customer_id: int
    items: List[str]
    total: float


@dataclass
class GetOrderQuery(Query):
    """Get order query."""
    order_id: int


class OrderCQRSService:
    """Order CQRS service."""
    
    def __init__(self):
        self.orders: dict[int, Order] = {}
        self.next_id = 1
    
    def create_order(self, command: CreateOrderCommand) -> int:
        """Create order (command)."""
        order = Order(
            order_id=self.next_id,
            customer_id=command.customer_id,
            items=command.items,
            total=command.total,
            status="pending"
        )
        self.next_id += 1
        self.orders[order.order_id] = order
        print(f"[Command] Created order: {order.order_id}")
        return order.order_id
    
    def get_order(self, query: GetOrderQuery) -> Optional[Order]:
        """Get order (query)."""
        order = self.orders.get(query.order_id)
        if order:
            print(f"[Query] Retrieved order: {order.order_id}")
        return order


def main() -> None:
    """Demonstration of CQRS Pattern."""
    print("=" * 70)
    print("CQRS (COMMAND QUERY RESPONSIBILITY SEGREGATION) PATTERN")
    print("=" * 70)
    print()
    
    # Example 1: User CQRS
    print("Example 1: User Management CQRS")
    print("-" * 70)
    
    service = CQRSService()
    
    # Commands (Write)
    print("Executing Commands (Write Operations):")
    user_id1 = service.execute_command(CreateUserCommand("Alice", "alice@example.com"))
    user_id2 = service.execute_command(CreateUserCommand("Bob", "bob@example.com"))
    user_id3 = service.execute_command(CreateUserCommand("Charlie", "charlie@example.com"))
    print()
    
    service.execute_command(UpdateUserCommand(user_id2, name="Robert"))
    print()
    
    # Queries (Read)
    print("Executing Queries (Read Operations):")
    user = service.execute_query(GetUserQuery(user_id1))
    print()
    
    all_users = service.execute_query(GetAllUsersQuery())
    print()
    
    search_results = service.execute_query(SearchUsersQuery(name_pattern="al"))
    print()
    
    # Example 2: Order CQRS
    print("Example 2: Order Management CQRS")
    print("-" * 70)
    
    order_service = OrderCQRSService()
    
    order_id = order_service.create_order(
        CreateOrderCommand(
            customer_id=1,
            items=["Laptop", "Mouse"],
            total=999.99
        )
    )
    print()
    
    order = order_service.get_order(GetOrderQuery(order_id))
    if order:
        print(f"Order details: {order}")
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("CQRS")
    
    def cqrs_operations():
        svc = CQRSService()
        for i in range(50):
            svc.execute_command(CreateUserCommand(f"User{i}", f"user{i}@example.com"))
        return len(svc.execute_query(GetAllUsersQuery()))
    
    result, metrics = timer.measure(cqrs_operations)
    print(f"Time to create 50 users via CQRS: {metrics['execution_time_ms']:.3f} ms")
    print(f"Users created: {result}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Separate read and write operations into different models.")
    print("  Commands change state, queries read state.")
    print("\nKey Advantages:")
    print("  - Independent scaling of read/write")
    print("  - Optimize read and write separately")
    print("  - Clear separation of concerns")
    print("  - Can use different data stores")
    print("\nKey Disadvantages:")
    print("  - Increased complexity")
    print("  - Eventual consistency challenges")
    print("  - More infrastructure needed")
    print("  - Learning curve")
    print("\nWhen to Use:")
    print("  - High read/write ratio")
    print("  - Need to scale reads independently")
    print("  - Complex domain models")
    print("  - Different read/write requirements")
    print("\nCommon Use Cases:")
    print("  - Event-driven architectures")
    print("  - Microservices")
    print("  - High-traffic applications")
    print("  - Complex reporting requirements")
    print("=" * 70)


if __name__ == "__main__":
    main()
