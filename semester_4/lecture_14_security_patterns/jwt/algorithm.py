#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON Web Token (JWT) Pattern.

Compact, URL-safe token format for securely transmitting information
between parties. Consists of header, payload, and signature.
"""

import sys
from pathlib import Path
import json
import base64
import hmac
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


class JWT:
    """JSON Web Token implementation."""
    
    def __init__(self, secret: str):
        """
        Initialize JWT.
        
        Args:
            secret: Secret key for signing
        """
        self.secret = secret
    
    def encode(self, payload: Dict[str, Any], expires_in: int = 3600) -> str:
        """
        Encode JWT token.
        
        Args:
            payload: Token payload
            expires_in: Expiration time in seconds
            
        Returns:
            Encoded JWT token
        """
        # Header
        header = {
            "alg": "HS256",
            "typ": "JWT"
        }
        
        # Add expiration
        payload = payload.copy()
        payload["exp"] = int((datetime.now() + timedelta(seconds=expires_in)).timestamp())
        payload["iat"] = int(datetime.now().timestamp())
        
        # Encode header and payload
        header_encoded = self._base64_url_encode(json.dumps(header).encode())
        payload_encoded = self._base64_url_encode(json.dumps(payload).encode())
        
        # Create signature
        message = f"{header_encoded}.{payload_encoded}"
        signature = self._sign(message)
        signature_encoded = self._base64_url_encode(signature)
        
        return f"{message}.{signature_encoded}"
    
    def decode(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Decode and verify JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            Decoded payload or None if invalid
        """
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            header_encoded, payload_encoded, signature_encoded = parts
            
            # Verify signature
            message = f"{header_encoded}.{payload_encoded}"
            expected_signature = self._base64_url_encode(self._sign(message))
            
            if signature_encoded != expected_signature:
                return None
            
            # Decode payload
            payload_json = self._base64_url_decode(payload_encoded)
            payload = json.loads(payload_json)
            
            # Check expiration
            if "exp" in payload:
                exp_timestamp = payload["exp"]
                if datetime.now().timestamp() > exp_timestamp:
                    return None
            
            return payload
        except Exception:
            return None
    
    def _sign(self, message: str) -> bytes:
        """Sign message using HMAC-SHA256."""
        return hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
    
    def _base64_url_encode(self, data: bytes) -> str:
        """Base64 URL-safe encode."""
        return base64.urlsafe_b64encode(data).decode().rstrip('=')
    
    def _base64_url_decode(self, data: str) -> bytes:
        """Base64 URL-safe decode."""
        padding = 4 - len(data) % 4
        data += '=' * padding
        return base64.urlsafe_b64decode(data)


def main() -> None:
    """Demonstration of JWT Pattern."""
    print("=" * 70)
    print("JSON WEB TOKEN (JWT) PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Create and verify JWT
    print("Example 1: Create and Verify JWT")
    print("-" * 70)
    
    jwt = JWT(secret="my-secret-key")
    
    payload = {
        "user_id": 12345,
        "username": "alice",
        "role": "admin"
    }
    
    token = jwt.encode(payload, expires_in=3600)
    print(f"Token: {token[:50]}...")
    print()
    
    decoded = jwt.decode(token)
    if decoded:
        print("Decoded payload:")
        for key, value in decoded.items():
            if key not in ["exp", "iat"]:
                print(f"  {key}: {value}")
        print(f"  Issued at: {datetime.fromtimestamp(decoded['iat'])}")
        print(f"  Expires at: {datetime.fromtimestamp(decoded['exp'])}")
    else:
        print("Token invalid or expired")
    print()
    
    # Example 2: Token expiration
    print("Example 2: Token Expiration")
    print("-" * 70)
    
    short_token = jwt.encode({"test": "data"}, expires_in=1)
    print("Created token with 1 second expiration")
    
    decoded1 = jwt.decode(short_token)
    print(f"Immediate decode: {'Valid' if decoded1 else 'Invalid'}")
    
    import time
    time.sleep(1.1)
    
    decoded2 = jwt.decode(short_token)
    print(f"After 1.1s: {'Valid' if decoded2 else 'Invalid (expired)'}")
    print()
    
    # Example 3: Invalid token
    print("Example 3: Invalid Token Detection")
    print("-" * 70)
    
    invalid_token = "invalid.token.here"
    decoded = jwt.decode(invalid_token)
    print(f"Invalid token decode: {'Valid' if decoded else 'Invalid (as expected)'}")
    print()
    
    # Example 4: Performance measurement
    print("Example 4: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("JWT")
    
    def jwt_operations():
        jwt = JWT("secret")
        token = jwt.encode({"user_id": 123, "role": "user"})
        decoded = jwt.decode(token)
        return decoded is not None
    
    result, metrics = timer.measure(jwt_operations)
    print(f"Time to encode and decode JWT: {metrics['execution_time_ms']:.3f} ms")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Compact, URL-safe token format for securely transmitting")
    print("  information between parties.")
    print("\nToken Structure:")
    print("  - Header: Algorithm and token type")
    print("  - Payload: Claims (data)")
    print("  - Signature: Verification signature")
    print("\nKey Advantages:")
    print("  - Stateless authentication")
    print("  - Compact format")
    print("  - Self-contained")
    print("  - Widely supported")
    print("\nKey Disadvantages:")
    print("  - Cannot revoke tokens easily")
    print("  - Size limitations")
    print("  - Secret key management")
    print("  - XSS vulnerabilities if stored in localStorage")
    print("\nWhen to Use:")
    print("  - Stateless authentication")
    print("  - API authentication")
    print("  - Microservices communication")
    print("  - Single Sign-On (SSO)")
    print("\nCommon Use Cases:")
    print("  - REST API authentication")
    print("  - OAuth 2.0")
    print("  - Session management")
    print("  - Information exchange")
    print("\nSecurity Best Practices:")
    print("  - Use strong secret keys")
    print("  - Set appropriate expiration times")
    print("  - Use HTTPS only")
    print("  - Validate all claims")
    print("  - Store tokens securely")
    print("=" * 70)


if __name__ == "__main__":
    main()
