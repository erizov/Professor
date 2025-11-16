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
from framework.logging_utils import get_logger
logger = get_logger(__name__)


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
    logger.info("=" * 70)
    logger.info("JSON WEB TOKEN (JWT) PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: Create and verify JWT
    logger.info("Example 1: Create and Verify JWT")
    logger.info("-" * 70)
    
    jwt = JWT(secret="my-secret-key")
    
    payload = {
        "user_id": 12345,
        "username": "alice",
        "role": "admin"
    }
    
    token = jwt.encode(payload, expires_in=3600)
    logger.info(f"Token: {token[:50]}...")
    logger.info()
    
    decoded = jwt.decode(token)
    if decoded:
        logger.info("Decoded payload:")
        for key, value in decoded.items():
            if key not in ["exp", "iat"]:
                logger.info(f"  {key}: {value}")
        logger.info(f"  Issued at: {datetime.fromtimestamp(decoded['iat'])}")
        logger.info(f"  Expires at: {datetime.fromtimestamp(decoded['exp'])}")
    else:
        logger.info("Token invalid or expired")
    logger.info()
    
    # Example 2: Token expiration
    logger.info("Example 2: Token Expiration")
    logger.info("-" * 70)
    
    short_token = jwt.encode({"test": "data"}, expires_in=1)
    logger.info("Created token with 1 second expiration")
    
    decoded1 = jwt.decode(short_token)
    logger.info(f"Immediate decode: {'Valid' if decoded1 else 'Invalid'}")
    
    import time
    time.sleep(1.1)
    
    decoded2 = jwt.decode(short_token)
    logger.info(f"After 1.1s: {'Valid' if decoded2 else 'Invalid (expired)'}")
    logger.info()
    
    # Example 3: Invalid token
    logger.info("Example 3: Invalid Token Detection")
    logger.info("-" * 70)
    
    invalid_token = "invalid.token.here"
    decoded = jwt.decode(invalid_token)
    logger.info(f"Invalid token decode: {'Valid' if decoded else 'Invalid (as expected)'}")
    logger.info()
    
    # Example 4: Performance measurement
    logger.info("Example 4: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("JWT")
    
    def jwt_operations():
        jwt = JWT("secret")
        token = jwt.encode({"user_id": 123, "role": "user"})
        decoded = jwt.decode(token)
        return decoded is not None
    
    result, metrics = timer.measure(jwt_operations)
    logger.info(f"Time to encode and decode JWT: {metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Compact, URL-safe token format for securely transmitting")
    logger.info("  information between parties.")
    logger.info("\nToken Structure:")
    logger.info("  - Header: Algorithm and token type")
    logger.info("  - Payload: Claims (data)")
    logger.info("  - Signature: Verification signature")
    logger.info("\nKey Advantages:")
    logger.info("  - Stateless authentication")
    logger.info("  - Compact format")
    logger.info("  - Self-contained")
    logger.info("  - Widely supported")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Cannot revoke tokens easily")
    logger.info("  - Size limitations")
    logger.info("  - Secret key management")
    logger.info("  - XSS vulnerabilities if stored in localStorage")
    logger.info("\nWhen to Use:")
    logger.info("  - Stateless authentication")
    logger.info("  - API authentication")
    logger.info("  - Microservices communication")
    logger.info("  - Single Sign-On (SSO)")
    logger.info("\nCommon Use Cases:")
    logger.info("  - REST API authentication")
    logger.info("  - OAuth 2.0")
    logger.info("  - Session management")
    logger.info("  - Information exchange")
    logger.info("\nSecurity Best Practices:")
    logger.info("  - Use strong secret keys")
    logger.info("  - Set appropriate expiration times")
    logger.info("  - Use HTTPS only")
    logger.info("  - Validate all claims")
    logger.info("  - Store tokens securely")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()