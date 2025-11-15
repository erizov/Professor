#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Event Sourcing Pattern.

Store all changes to application state as a sequence of events.
The current state can be reconstructed by replaying events.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


# Event Base
class Event(ABC):
    """Base event interface."""
    
    @property
    @abstractmethod
    def event_type(self) -> str:
        """Get event type."""
        pass
    
    @property
    @abstractmethod
    def timestamp(self) -> datetime:
        """Get event timestamp."""
        pass


# Domain Events
@dataclass
class UserCreatedEvent(Event):
    """User created event."""
    user_id: int
    name: str
    email: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def event_type(self) -> str:
        return "UserCreated"


@dataclass
class UserUpdatedEvent(Event):
    """User updated event."""
    user_id: int
    name: Optional[str] = None
    email: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def event_type(self) -> str:
        return "UserUpdated"


@dataclass
class UserDeletedEvent(Event):
    """User deleted event."""
    user_id: int
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def event_type(self) -> str:
        return "UserDeleted"


# Aggregate Root
@dataclass
class User:
    """User aggregate root."""
    user_id: int
    name: str
    email: str
    created_at: datetime
    deleted: bool = False
    
    def apply_event(self, event: Event) -> None:
        """Apply event to aggregate."""
        if isinstance(event, UserCreatedEvent):
            self.user_id = event.user_id
            self.name = event.name
            self.email = event.email
            self.created_at = event.timestamp
        elif isinstance(event, UserUpdatedEvent):
            if event.name:
                self.name = event.name
            if event.email:
                self.email = event.email
        elif isinstance(event, UserDeletedEvent):
            self.deleted = True
    
    def __str__(self) -> str:
        status = "deleted" if self.deleted else "active"
        return f"User(id={self.user_id}, name='{self.name}', email='{self.email}', status={status})"


# Event Store
class EventStore:
    """Stores events."""
    
    def __init__(self):
        self.events: List[Event] = []
        self.aggregate_events: dict[int, List[Event]] = {}
    
    def append(self, aggregate_id: int, event: Event) -> None:
        """Append event to store."""
        self.events.append(event)
        if aggregate_id not in self.aggregate_events:
            self.aggregate_events[aggregate_id] = []
        self.aggregate_events[aggregate_id].append(event)
        print(f"[EventStore] Stored event: {event.event_type} for aggregate {aggregate_id}")
    
    def get_events(self, aggregate_id: int) -> List[Event]:
        """Get all events for aggregate."""
        return self.aggregate_events.get(aggregate_id, [])
    
    def get_all_events(self) -> List[Event]:
        """Get all events."""
        return self.events.copy()


# Event Sourced Repository
class EventSourcedRepository:
    """Repository that uses event sourcing."""
    
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
        self.snapshots: dict[int, User] = {}  # Optional: for performance
    
    def save(self, aggregate: User, events: List[Event]) -> None:
        """Save aggregate and events."""
        for event in events:
            self.event_store.append(aggregate.user_id, event)
            aggregate.apply_event(event)
        # Optional: save snapshot
        self.snapshots[aggregate.user_id] = aggregate
    
    def load(self, aggregate_id: int) -> Optional[User]:
        """Load aggregate by replaying events."""
        # Check snapshot first
        if aggregate_id in self.snapshots:
            snapshot = self.snapshots[aggregate_id]
            events = self.event_store.get_events(aggregate_id)
            # Replay events after snapshot
            snapshot_events = [e for e in events if e.timestamp > snapshot.created_at]
            aggregate = snapshot
        else:
            # Replay all events
            events = self.event_store.get_events(aggregate_id)
            if not events:
                return None
            aggregate = User(0, "", "", datetime.now())
        
        # Replay events
        for event in events:
            aggregate.apply_event(event)
        
        return aggregate


# Service using Event Sourcing
class UserService:
    """User service with event sourcing."""
    
    def __init__(self, repository: EventSourcedRepository):
        self.repository = repository
        self.next_id = 1
    
    def create_user(self, name: str, email: str) -> User:
        """Create user."""
        user_id = self.next_id
        self.next_id += 1
        
        event = UserCreatedEvent(user_id, name, email)
        user = User(0, "", "", datetime.now())
        
        self.repository.save(user, [event])
        return self.repository.load(user_id)
    
    def update_user(self, user_id: int, name: Optional[str] = None,
                   email: Optional[str] = None) -> Optional[User]:
        """Update user."""
        user = self.repository.load(user_id)
        if not user or user.deleted:
            return None
        
        event = UserUpdatedEvent(user_id, name, email)
        self.repository.save(user, [event])
        return self.repository.load(user_id)
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        user = self.repository.load(user_id)
        if not user or user.deleted:
            return False
        
        event = UserDeletedEvent(user_id)
        self.repository.save(user, [event])
        return True
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user."""
        return self.repository.load(user_id)


# Example 2: Account Event Sourcing
@dataclass
class AccountCreatedEvent(Event):
    """Account created event."""
    account_id: int
    owner: str
    initial_balance: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def event_type(self) -> str:
        return "AccountCreated"


@dataclass
class MoneyDepositedEvent(Event):
    """Money deposited event."""
    account_id: int
    amount: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def event_type(self) -> str:
        return "MoneyDeposited"


@dataclass
class MoneyWithdrawnEvent(Event):
    """Money withdrawn event."""
    account_id: int
    amount: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def event_type(self) -> str:
        return "MoneyWithdrawn"


@dataclass
class Account:
    """Account aggregate."""
    account_id: int
    owner: str
    balance: float = 0.0
    
    def apply_event(self, event: Event) -> None:
        """Apply event."""
        if isinstance(event, AccountCreatedEvent):
            self.account_id = event.account_id
            self.owner = event.owner
            self.balance = event.initial_balance
        elif isinstance(event, MoneyDepositedEvent):
            self.balance += event.amount
        elif isinstance(event, MoneyWithdrawnEvent):
            self.balance -= event.amount


def main() -> None:
    """Demonstration of Event Sourcing Pattern."""
    print("=" * 70)
    print("EVENT SOURCING PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: User Event Sourcing
    print("Example 1: User Event Sourcing")
    print("-" * 70)
    
    event_store = EventStore()
    repository = EventSourcedRepository(event_store)
    service = UserService(repository)
    
    # Create user
    user1 = service.create_user("Alice", "alice@example.com")
    print(f"Created: {user1}")
    print()
    
    # Update user
    user1 = service.update_user(user1.user_id, name="Alice Smith")
    print(f"Updated: {user1}")
    print()
    
    # Get user (reconstructed from events)
    retrieved = service.get_user(user1.user_id)
    print(f"Retrieved (from events): {retrieved}")
    print()
    
    # Show event history
    events = event_store.get_events(user1.user_id)
    print(f"Event history for user {user1.user_id}:")
    for event in events:
        print(f"  - {event.event_type} at {event.timestamp}")
    print()
    
    # Delete user
    service.delete_user(user1.user_id)
    deleted_user = service.get_user(user1.user_id)
    print(f"After deletion: {deleted_user}")
    print()
    
    # Example 2: Account Event Sourcing
    print("Example 2: Account Event Sourcing")
    print("-" * 70)
    
    account_store = EventStore()
    account_repo = EventSourcedRepository(account_store)
    
    # Create account
    account = Account(0, "")
    account_id = 1
    account_repo.save(account, [AccountCreatedEvent(account_id, "Bob", 100.0)])
    account = account_repo.load(account_id)
    print(f"Account created: {account}")
    
    # Deposit
    account_repo.save(account, [MoneyDepositedEvent(account_id, 50.0)])
    account = account_repo.load(account_id)
    print(f"After deposit: {account}")
    
    # Withdraw
    account_repo.save(account, [MoneyWithdrawnEvent(account_id, 30.0)])
    account = account_repo.load(account_id)
    print(f"After withdrawal: {account}")
    print()
    
    # Show event history
    events = account_store.get_events(account_id)
    print("Account event history:")
    for event in events:
        print(f"  - {event.event_type} at {event.timestamp}")
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Event Sourcing")
    
    def event_sourcing_operations():
        store = EventStore()
        repo = EventSourcedRepository(store)
        svc = UserService(repo)
        
        user = svc.create_user("Test", "test@example.com")
        svc.update_user(user.user_id, name="Test Updated")
        return len(store.get_events(user.user_id))
    
    result, metrics = timer.measure(event_sourcing_operations)
    print(f"Time to create and update user via event sourcing: "
          f"{metrics['execution_time_ms']:.3f} ms")
    print(f"Events created: {result}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Store all changes to application state as a sequence")
    print("  of events. The current state can be reconstructed by")
    print("  replaying events.")
    print("\nKey Advantages:")
    print("  - Complete audit trail")
    print("  - Time travel (reconstruct any point in time)")
    print("  - Event replay for debugging")
    print("  - Natural fit for event-driven architecture")
    print("\nKey Disadvantages:")
    print("  - Eventual consistency")
    print("  - Event versioning complexity")
    print("  - Storage overhead")
    print("  - Performance for large event streams")
    print("\nWhen to Use:")
    print("  - Need complete audit trail")
    print("  - Complex business logic")
    print("  - Event-driven architecture")
    print("  - Need to replay events")
    print("\nCommon Use Cases:")
    print("  - Financial systems")
    print("  - Domain-Driven Design")
    print("  - Audit requirements")
    print("  - Event-driven microservices")
    print("=" * 70)


if __name__ == "__main__":
    main()
