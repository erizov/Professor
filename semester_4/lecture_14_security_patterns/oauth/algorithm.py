#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OAuth 2.0 Pattern.

Authorization framework that enables applications to obtain limited access
to user accounts. Uses authorization codes, access tokens, and refresh tokens.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import secrets
import hashlib

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


@dataclass
class Client:
    """OAuth client."""
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: list = None
    
    def __post_init__(self):
        if self.scopes is None:
            self.scopes = []


@dataclass
class AuthorizationCode:
    """Authorization code."""
    code: str
    client_id: str
    user_id: str
    redirect_uri: str
    scopes: list
    expires_at: datetime


@dataclass
class AccessToken:
    """Access token."""
    token: str
    client_id: str
    user_id: str
    scopes: list
    expires_at: datetime
    refresh_token: Optional[str] = None


class AuthorizationServer:
    """OAuth 2.0 Authorization Server."""
    
    def __init__(self):
        self.clients: Dict[str, Client] = {}
        self.authorization_codes: Dict[str, AuthorizationCode] = {}
        self.access_tokens: Dict[str, AccessToken] = {}
        self.refresh_tokens: Dict[str, AccessToken] = {}
    
    def register_client(self, client: Client) -> None:
        """Register OAuth client."""
        self.clients[client.client_id] = client
    
    def generate_authorization_code(self, client_id: str, user_id: str, 
                                   redirect_uri: str, scopes: list) -> str:
        """Generate authorization code."""
        code = secrets.token_urlsafe(32)
        
        auth_code = AuthorizationCode(
            code=code,
            client_id=client_id,
            user_id=user_id,
            redirect_uri=redirect_uri,
            scopes=scopes,
            expires_at=datetime.now() + timedelta(minutes=10)
        )
        
        self.authorization_codes[code] = auth_code
        return code
    
    def exchange_code_for_token(self, code: str, client_id: str, 
                               client_secret: str) -> Optional[AccessToken]:
        """Exchange authorization code for access token."""
        # Verify code exists
        if code not in self.authorization_codes:
            return None
        
        auth_code = self.authorization_codes[code]
        
        # Verify client
        if auth_code.client_id != client_id:
            return None
        
        if client_id not in self.clients:
            return None
        
        client = self.clients[client_id]
        if client.client_secret != client_secret:
            return None
        
        # Check expiration
        if datetime.now() > auth_code.expires_at:
            del self.authorization_codes[code]
            return None
        
        # Generate access token
        access_token = AccessToken(
            token=secrets.token_urlsafe(32),
            client_id=client_id,
            user_id=auth_code.user_id,
            scopes=auth_code.scopes,
            expires_at=datetime.now() + timedelta(hours=1),
            refresh_token=secrets.token_urlsafe(32)
        )
        
        self.access_tokens[access_token.token] = access_token
        self.refresh_tokens[access_token.refresh_token] = access_token
        
        # Remove used authorization code
        del self.authorization_codes[code]
        
        return access_token
    
    def refresh_access_token(self, refresh_token: str) -> Optional[AccessToken]:
        """Refresh access token using refresh token."""
        if refresh_token not in self.refresh_tokens:
            return None
        
        old_token = self.refresh_tokens[refresh_token]
        
        # Generate new access token
        new_token = AccessToken(
            token=secrets.token_urlsafe(32),
            client_id=old_token.client_id,
            user_id=old_token.user_id,
            scopes=old_token.scopes,
            expires_at=datetime.now() + timedelta(hours=1),
            refresh_token=secrets.token_urlsafe(32)
        )
        
        # Update tokens
        del self.access_tokens[old_token.token]
        del self.refresh_tokens[refresh_token]
        
        self.access_tokens[new_token.token] = new_token
        self.refresh_tokens[new_token.refresh_token] = new_token
        
        return new_token
    
    def validate_token(self, token: str) -> Optional[AccessToken]:
        """Validate access token."""
        if token not in self.access_tokens:
            return None
        
        access_token = self.access_tokens[token]
        
        # Check expiration
        if datetime.now() > access_token.expires_at:
            del self.access_tokens[token]
            return None
        
        return access_token


class ResourceServer:
    """OAuth 2.0 Resource Server."""
    
    def __init__(self, auth_server: AuthorizationServer):
        self.auth_server = auth_server
    
    def get_resource(self, token: str, resource_path: str) -> Optional[Dict]:
        """Get protected resource."""
        access_token = self.auth_server.validate_token(token)
        
        if not access_token:
            return None
        
        # Check scopes
        if "read" not in access_token.scopes:
            return None
        
        # Return resource
        return {
            "user_id": access_token.user_id,
            "resource": resource_path,
            "data": f"Protected data for {resource_path}"
        }


def main() -> None:
    """Demonstration of OAuth 2.0 Pattern."""
    print("=" * 70)
    print("OAUTH 2.0 PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: OAuth 2.0 Flow
    print("Example 1: OAuth 2.0 Authorization Code Flow")
    print("-" * 70)
    
    # Setup
    auth_server = AuthorizationServer()
    
    client = Client(
        client_id="my-app",
        client_secret="my-secret",
        redirect_uri="https://my-app.com/callback",
        scopes=["read", "write"]
    )
    auth_server.register_client(client)
    
    # Step 1: User authorizes, get authorization code
    print("Step 1: User authorizes application")
    auth_code = auth_server.generate_authorization_code(
        client_id="my-app",
        user_id="user123",
        redirect_uri="https://my-app.com/callback",
        scopes=["read", "write"]
    )
    print(f"Authorization code generated: {auth_code[:20]}...")
    print()
    
    # Step 2: Exchange code for access token
    print("Step 2: Exchange authorization code for access token")
    access_token = auth_server.exchange_code_for_token(
        code=auth_code,
        client_id="my-app",
        client_secret="my-secret"
    )
    
    if access_token:
        print(f"Access token: {access_token.token[:30]}...")
        print(f"Refresh token: {access_token.refresh_token[:30]}...")
        print(f"Expires at: {access_token.expires_at}")
        print(f"Scopes: {access_token.scopes}")
    print()
    
    # Step 3: Use access token to access resource
    print("Step 3: Use access token to access protected resource")
    resource_server = ResourceServer(auth_server)
    
    if access_token:
        resource = resource_server.get_resource(
            token=access_token.token,
            resource_path="/api/user/profile"
        )
        
        if resource:
            print(f"Resource accessed: {resource}")
        else:
            print("Access denied")
    print()
    
    # Example 2: Token Refresh
    print("Example 2: Refresh Access Token")
    print("-" * 70)
    
    if access_token and access_token.refresh_token:
        new_token = auth_server.refresh_access_token(access_token.refresh_token)
        if new_token:
            print(f"New access token: {new_token.token[:30]}...")
            print(f"New refresh token: {new_token.refresh_token[:30]}...")
    print()
    
    # Example 3: Invalid token
    print("Example 3: Invalid Token Handling")
    print("-" * 70)
    
    invalid_resource = resource_server.get_resource("invalid-token", "/api/data")
    print(f"Invalid token result: {invalid_resource}")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Authorization framework that enables applications to obtain")
    print("  limited access to user accounts.")
    print("\nOAuth 2.0 Flow:")
    print("  1. Client requests authorization")
    print("  2. User authorizes")
    print("  3. Authorization code returned")
    print("  4. Code exchanged for access token")
    print("  5. Access token used for API calls")
    print("  6. Refresh token used to get new access token")
    print("\nKey Advantages:")
    print("  - Delegated authorization")
    print("  - Limited scope access")
    print("  - No password sharing")
    print("  - Revocable access")
    print("\nKey Disadvantages:")
    print("  - Complex implementation")
    print("  - Security vulnerabilities if misconfigured")
    print("  - Token management complexity")
    print("\nWhen to Use:")
    print("  - Third-party application access")
    print("  - API authorization")
    print("  - Single Sign-On (SSO)")
    print("  - Mobile app authentication")
    print("\nCommon Use Cases:")
    print("  - Social login (Google, Facebook)")
    print("  - API access delegation")
    print("  - Microservices authentication")
    print("  - Mobile app authentication")
    print("\nGrant Types:")
    print("  - Authorization Code: Web applications")
    print("  - Implicit: Mobile/SPA (deprecated)")
    print("  - Client Credentials: Server-to-server")
    print("  - Password: Trusted applications")
    print("=" * 70)


if __name__ == "__main__":
    main()
