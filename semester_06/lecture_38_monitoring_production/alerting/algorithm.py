#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alerting implementation.

This file contains the implementation of the Alerting algorithm.
"""

from typing import List, Optional, Dict, Set


class Alerting:
    """Alerting system implementation."""

    def __init__(self):
        self.alerts: List[dict] = []
        self.rules: List[dict] = []
        self.notification_channels: List[callable] = []

    def add_rule(
        self, name: str, condition: callable, severity: str = "warning"
    ) -> None:
        """Add alerting rule."""
        self.rules.append({"name": name, "condition": condition, "severity": severity})

    def add_notification_channel(self, channel: callable) -> None:
        """Add notification channel."""
        self.notification_channels.append(channel)

    def check_metrics(self, metrics: dict) -> List[dict]:
        """Check metrics against rules."""
        triggered_alerts = []

        for rule in self.rules:
            if rule["condition"](metrics):
                alert = {
                    "rule": rule["name"],
                    "severity": rule["severity"],
                    "metrics": metrics,
                    "timestamp": None,
                }
                import time

                alert["timestamp"] = time.time()
                self.alerts.append(alert)
                triggered_alerts.append(alert)

                # Send notifications
                for channel in self.notification_channels:
                    channel(alert)

        return triggered_alerts

    def get_recent_alerts(self, limit: int = 10) -> List[dict]:
        """Get recent alerts."""
        return sorted(self.alerts, key=lambda x: x["timestamp"], reverse=True)[:limit]


def main() -> None:
    """Demonstrate Alerting."""
    print("=" * 70)
    print("ALERTING")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Alerting")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
