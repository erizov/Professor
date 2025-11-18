#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rate Limiting implementation.

This file contains the implementation of the Rate Limiting algorithm.
"""

from typing import List, Optional, Dict, Set


class RateLimiting:
    """Rate limiting."""
    def __init__(self, max_requests: int = 100, 
                time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[str, List[float]] = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed."""
        import time
        current_time = time.time()
        if identifier not in self.requests:
            self.requests[identifier] = []
        # Remove old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if current_time - req_time < self.time_window
        ]
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        self.requests[identifier].append(current_time)
        return True


def main() -> None:
    """Demonstrate Rate Limiting."""
    print("=" * 70)
    print("RATE LIMITING")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Rate Limiting")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
