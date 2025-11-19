#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canary Analysis implementation.

This file contains the implementation of the Canary Analysis algorithm.
"""

from typing import List, Optional, Dict, Set


class CanaryAnalysis:
    """Canary deployment analysis."""

    def __init__(self):
        self.canary_metrics: Dict[str, List[float]] = {}
        self.stable_metrics: Dict[str, List[float]] = {}

    def add_metric(self, version: str, metric_name: str, value: float) -> None:
        """Add metric."""
        metrics = self.canary_metrics if version == "canary" else self.stable_metrics
        if metric_name not in metrics:
            metrics[metric_name] = []
        metrics[metric_name].append(value)

    def compare_metrics(self) -> dict:
        """Compare canary vs stable metrics."""
        comparison = {}

        all_metrics = set(self.canary_metrics.keys()) | set(self.stable_metrics.keys())

        for metric_name in all_metrics:
            canary_vals = self.canary_metrics.get(metric_name, [])
            stable_vals = self.stable_metrics.get(metric_name, [])

            if canary_vals and stable_vals:
                canary_avg = sum(canary_vals) / len(canary_vals)
                stable_avg = sum(stable_vals) / len(stable_vals)

                diff = canary_avg - stable_avg
                diff_percent = (diff / stable_avg * 100) if stable_avg > 0 else 0.0

                comparison[metric_name] = {
                    "canary_avg": canary_avg,
                    "stable_avg": stable_avg,
                    "difference": diff,
                    "difference_percent": diff_percent,
                }

        return comparison

    def should_rollback(self, threshold: float = 0.1) -> bool:
        """Check if should rollback."""
        comparison = self.compare_metrics()

        for metric_name, comp in comparison.items():
            # If canary performs significantly worse
            if comp["difference_percent"] < -threshold * 100:
                return True

        return False


def main() -> None:
    """Demonstrate Canary Analysis."""
    print("=" * 70)
    print("CANARY ANALYSIS")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Canary Analysis")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
