#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Capacity Planning implementation.

This file contains the implementation of the Capacity Planning algorithm.
"""

from typing import List, Optional, Dict, Set


class CapacityPlanning:
    """Capacity planning system."""

    def __init__(self):
        self.historical_usage: List[float] = []
        self.current_capacity: float = 100.0
        self.growth_rate: float = 0.1

    def record_usage(self, usage: float) -> None:
        """Record usage."""
        self.historical_usage.append(usage)

        # Keep recent history
        if len(self.historical_usage) > 365:  # 1 year
            self.historical_usage.pop(0)

    def predict_future_usage(self, days: int = 30) -> List[float]:
        """Predict future usage."""
        if len(self.historical_usage) < 2:
            return [self.current_capacity] * days

        # Simple linear growth prediction
        recent_avg = sum(self.historical_usage[-30:]) / min(
            30, len(self.historical_usage)
        )
        growth = self.growth_rate / 365  # Daily growth

        predictions = []
        for i in range(days):
            predictions.append(recent_avg * (1 + growth) ** i)

        return predictions

    def recommend_capacity(self, target_utilization: float = 0.8) -> float:
        """Recommend capacity."""
        if not self.historical_usage:
            return self.current_capacity

        predicted_usage = self.predict_future_usage(30)
        max_predicted = (
            max(predicted_usage) if predicted_usage else self.current_capacity
        )

        recommended = max_predicted / target_utilization
        return recommended

    def calculate_growth_rate(self) -> float:
        """Calculate growth rate from historical data."""
        if len(self.historical_usage) < 2:
            return 0.0

        # Simple growth rate calculation
        old_avg = sum(self.historical_usage[: len(self.historical_usage) // 2]) / (
            len(self.historical_usage) // 2
        )
        new_avg = sum(self.historical_usage[len(self.historical_usage) // 2 :]) / (
            len(self.historical_usage) - len(self.historical_usage) // 2
        )

        if old_avg > 0:
            self.growth_rate = (new_avg - old_avg) / old_avg
        else:
            self.growth_rate = 0.0

        return self.growth_rate


def main() -> None:
    """Demonstrate Capacity Planning."""
    print("=" * 70)
    print("CAPACITY PLANNING")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Capacity Planning")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
