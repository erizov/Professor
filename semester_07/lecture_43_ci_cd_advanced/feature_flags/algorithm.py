#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feature Flags implementation.

This file contains the implementation of the Feature Flags algorithm.
"""

from typing import List, Optional, Dict, Set


class FeatureFlags:
    """Feature flags system."""

    def __init__(self):
        self.flags: Dict[str, dict] = {}

    def create_flag(self, flag_name: str, default_value: bool = False) -> None:
        """Create feature flag."""
        self.flags[flag_name] = {
            "enabled": default_value,
            "users": set(),
            "percentage": 0.0,
        }

    def enable_flag(self, flag_name: str) -> None:
        """Enable feature flag."""
        if flag_name in self.flags:
            self.flags[flag_name]["enabled"] = True

    def disable_flag(self, flag_name: str) -> None:
        """Disable feature flag."""
        if flag_name in self.flags:
            self.flags[flag_name]["enabled"] = False

    def enable_for_user(self, flag_name: str, user_id: str) -> None:
        """Enable flag for specific user."""
        if flag_name in self.flags:
            self.flags[flag_name]["users"].add(user_id)

    def set_percentage(self, flag_name: str, percentage: float) -> None:
        """Set rollout percentage."""
        if flag_name in self.flags:
            self.flags[flag_name]["percentage"] = percentage

    def is_enabled(self, flag_name: str, user_id: Optional[str] = None) -> bool:
        """Check if flag is enabled."""
        if flag_name not in self.flags:
            return False

        flag = self.flags[flag_name]

        # Check user-specific enablement
        if user_id and user_id in flag["users"]:
            return True

        # Check percentage rollout
        if flag["percentage"] > 0.0 and user_id:
            import hashlib

            hash_val = int(hashlib.md5((flag_name + user_id).encode()).hexdigest(), 16)
            if (hash_val % 100) < (flag["percentage"] * 100):
                return True

        return flag["enabled"]


def main() -> None:
    """Demonstrate Feature Flags."""
    print("=" * 70)
    print("FEATURE FLAGS")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Feature Flags")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
