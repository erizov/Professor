#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Authentication Pattern.

Verifies the identity of a user, process, or device. Ensures that
entities are who they claim to be before granting access.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Optional, Dict
import hashlib
import secrets

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class User:
    """User entity."""
    
    def __init__(self, user_id: str, username: str, password_hash: str):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash


class AuthenticationService:
    """Authentication service."""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, str] = {}  # session_id -> user_id
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str) -> User:
        """Register new user."""
        if username in self.users:
            raise ValueError("Username already exists")
        
        password_hash = self.hash_password(password)
        user_id = f"user_{len(self.users) + 1}"
        user = User(user_id, username, password_hash)
        self.users[username] = user
        return user
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """
        Authenticate user.
        
        Returns:
            Session ID if successful, None otherwise
        """
        if username not in self.users:
            return None
        
        user = self.users[username]
        password_hash = self.hash_password(password)
        
        if user.password_hash == password_hash:
            # Create session
            session_id = secrets.token_urlsafe(32)
            self.sessions[session_id] = user.user_id
            return session_id
        
        return None
    
    def validate_session(self, session_id: str) -> Optional[User]:
        """Validate session and return user."""
        if session_id not in self.sessions:
            return None
        
        user_id = self.sessions[session_id]
        for user in self.users.values():
            if user.user_id == user_id:
                return user
        return None
    
    def logout(self, session_id: str) -> bool:
        """Logout user."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False


# Example 2: Token-based Authentication
class TokenAuth:
    """Token-based authentication."""
    
    def __init__(self):
        self.tokens: Dict[str, str] = {}  # token -> user_id
        self.users: Dict[str, str] = {}  # user_id -> password_hash
    
    def hash_password(self, password: str) -> str:
        """Hash password."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, user_id: str, password: str) -> None:
        """Create user."""
        self.users[user_id] = self.hash_password(password)
    
    def login(self, user_id: str, password: str) -> Optional[str]:
        """Login and get token."""
        if user_id not in self.users:
            return None
        
        password_hash = self.hash_password(password)
        if self.users[user_id] == password_hash:
            token = secrets.token_urlsafe(32)
            self.tokens[token] = user_id
            return token
        return None
    
    def validate_token(self, token: str) -> Optional[str]:
        """Validate token and return user_id."""
        return self.tokens.get(token)


def main() -> None:
    """Demonstration of Authentication Pattern."""
    print("=" * 70)
    print("AUTHENTICATION PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Session-based Authentication
    print("Example 1: Session-based Authentication")
    print("-" * 70)
    
    auth_service = AuthenticationService()
    
    # Register users
    user1 = auth_service.register_user("alice", "password123")
    user2 = auth_service.register_user("bob", "secret456")
    
    print(f"Registered users: {user1.username}, {user2.username}")
    print()
    
    # Authenticate
    session1 = auth_service.authenticate("alice", "password123")
    session2 = auth_service.authenticate("bob", "wrong_password")
    
    print(f"Alice login: {'Success' if session1 else 'Failed'}")
    print(f"Bob login (wrong password): {'Success' if session2 else 'Failed'}")
    print()
    
    # Validate session
    if session1:
        user = auth_service.validate_session(session1)
        print(f"Session validated: {user.username if user else 'Invalid'}")
        auth_service.logout(session1)
        print("Logged out")
    print()
    
    # Example 2: Token-based Authentication
    print("Example 2: Token-based Authentication")
    print("-" * 70)
    
    token_auth = TokenAuth()
    token_auth.create_user("user1", "password123")
    token_auth.create_user("user2", "secret456")
    
    token = token_auth.login("user1", "password123")
    print(f"Login token: {token[:20]}..." if token else "Login failed")
    
    if token:
        user_id = token_auth.validate_token(token)
        print(f"Token validated: {user_id}")
    print()
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Authentication")
    
    def auth_operations():
        auth = AuthenticationService()
        for i in range(100):
            auth.register_user(f"user{i}", f"pass{i}")
        return len(auth.users)
    
    result, metrics = timer.measure(auth_operations)
    print(f"Time to register 100 users: {metrics['execution_time_ms']:.3f} ms")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Verify the identity of a user, process, or device.")
    print("  Ensures entities are who they claim to be.")
    print("\nKey Advantages:")
    print("  - Security and access control")
    print("  - User identification")
    print("  - Session management")
    print("  - Audit trail")
    print("\nKey Disadvantages:")
    print("  - Password management complexity")
    print("  - Security vulnerabilities if not implemented correctly")
    print("  - Session management overhead")
    print("\nWhen to Use:")
    print("  - User login systems")
    print("  - API authentication")
    print("  - Secure access control")
    print("  - Multi-user applications")
    print("\nCommon Use Cases:")
    print("  - Web applications")
    print("  - REST APIs")
    print("  - Mobile applications")
    print("  - Enterprise systems")
    print("=" * 70)


if __name__ == "__main__":
    main()
