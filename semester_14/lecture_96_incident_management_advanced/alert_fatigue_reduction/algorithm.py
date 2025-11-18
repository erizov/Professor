#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alert Fatigue Reduction implementation.

This file contains the implementation of the Alert Fatigue Reduction algorithm.
"""

from typing import List, Optional, Dict, Set


class AlertFatigueReduction:
    """Alert fatigue reduction system."""
    def __init__(self):
        self.alerts: List[dict] = []
        self.alert_groups: Dict[str, List[dict]] = {}
        self.suppressed_alerts: Set[str] = set()
    
    def add_alert(self, alert_id: str, severity: str, 
                 message: str, source: str) -> None:
        """Add alert."""
        import time
        alert = {
            "id": alert_id,
            "severity": severity,
            "message": message,
            "source": source,
            "timestamp": time.time(),
            "count": 1
        }
        self.alerts.append(alert)
    
    def group_similar_alerts(self, time_window: float = 300.0) -> List[dict]:
        """Group similar alerts."""
        import time
        current_time = time.time()
        
        # Group by source and message
        groups = {}
        for alert in self.alerts:
            if current_time - alert["timestamp"] <= time_window:
                key = f"{alert['source']}:{alert['message']}"
                if key not in groups:
                    groups[key] = []
                groups[key].append(alert)
        
        # Create grouped alerts
        grouped = []
        for key, alerts in groups.items():
            if len(alerts) > 1:
                grouped.append({
                    "group_key": key,
                    "count": len(alerts),
                    "severity": max(a["severity"] for a in alerts),
                    "first_seen": min(a["timestamp"] for a in alerts),
                    "last_seen": max(a["timestamp"] for a in alerts),
                    "alerts": alerts
                })
        
        return grouped
    
    def should_suppress(self, alert_id: str) -> bool:
        """Check if alert should be suppressed."""
        return alert_id in self.suppressed_alerts
    
    def suppress_alert(self, alert_id: str) -> None:
        """Suppress alert."""
        self.suppressed_alerts.add(alert_id)


def main() -> None:
    """Demonstrate Alert Fatigue Reduction."""
    print("=" * 70)
    print("ALERT FATIGUE REDUCTION")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Alert Fatigue Reduction")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
