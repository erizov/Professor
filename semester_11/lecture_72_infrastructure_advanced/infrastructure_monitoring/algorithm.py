#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Infrastructure Monitoring implementation.

This file contains the implementation of the Infrastructure Monitoring algorithm.
"""

from typing import List, Optional, Dict, Set


class InfrastructureMonitoring:
    """Infrastructure monitoring system."""
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        self.alerts: List[dict] = {}
    
    def collect_metric(self, metric_name: str, value: float, 
                      tags: dict = None) -> None:
        """Collect metric."""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(value)
    
    def check_health(self) -> dict:
        """Check infrastructure health."""
        health_status = {}
        for metric, values in self.metrics.items():
            if values:
                avg = sum(values) / len(values)
                health_status[metric] = 'healthy' if avg < 80 else 'warning'
        return health_status
    
    def create_alert(self, alert_name: str, condition: callable) -> None:
        """Create alert rule."""
        self.alerts[alert_name] = condition
    
    def evaluate_alerts(self) -> List[str]:
        """Evaluate all alerts."""
        triggered = []
        for alert_name, condition in self.alerts.items():
            if condition(self.metrics):
                triggered.append(alert_name)
        return triggered


def main() -> None:
    """Demonstrate Infrastructure Monitoring."""
    print("=" * 70)
    print("INFRASTRUCTURE MONITORING")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Infrastructure Monitoring")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
