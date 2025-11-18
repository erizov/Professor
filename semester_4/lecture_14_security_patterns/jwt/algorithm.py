#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jwt implementation.

This file contains the implementation of the Jwt algorithm.
"""

from typing import List, Optional, Dict, Set


class JWT:
    """JSON Web Token implementation."""
    def __init__(self, secret: str):
        self.secret = secret
        import time
        self.current_time = time.time
    
    def encode(self, payload: dict, expires_in: int = 3600) -> str:
        """Encode JWT."""
        import time
        import json
        import base64
        import hmac
        import hashlib
        
        header = {'alg': 'HS256', 'typ': 'JWT'}
        payload['exp'] = int(time.time()) + expires_in
        
        header_b64 = base64.urlsafe_b64encode(
            json.dumps(header).encode()
        ).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(
            json.dumps(payload).encode()
        ).decode().rstrip('=')
        
        message = f"{header_b64}.{payload_b64}"
        signature = hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
        
        return f"{message}.{signature_b64}"
    
    def decode(self, token: str) -> Optional[dict]:
        """Decode JWT."""
        import json
        import base64
        import hmac
        import hashlib
        import time
        
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            header_b64, payload_b64, signature_b64 = parts
            
            # Verify signature
            message = f"{header_b64}.{payload_b64}"
            expected_sig = hmac.new(
                self.secret.encode(),
                message.encode(),
                hashlib.sha256
            ).digest()
            expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode().rstrip('=')
            
            if signature_b64 != expected_sig_b64:
                return None
            
            # Decode payload
            payload_json = base64.urlsafe_b64decode(
                payload_b64 + '=='
            ).decode()
            payload = json.loads(payload_json)
            
            # Check expiration
            if 'exp' in payload and payload['exp'] < int(time.time()):
                return None
            
            return payload
        except:
            return None


def main() -> None:
    """Demonstrate Jwt."""
    print("=" * 70)
    print("JWT")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Jwt")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
