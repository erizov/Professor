#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Apm implementation.

This file contains the implementation of the Apm algorithm.
"""

from typing import List, Optional, Dict, Set


class APM:
    """Application Performance Monitoring."""

    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        self.traces: List[dict] = []
        self.spans: List[dict] = []

    def record_metric(self, name: str, value: float) -> None:
        """Record metric."""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)

        # Keep only recent metrics
        if len(self.metrics[name]) > 1000:
            self.metrics[name] = self.metrics[name][-1000:]

    def start_trace(self, trace_id: str, operation: str) -> None:
        """Start trace."""
        import time

        trace = {
            "id": trace_id,
            "operation": operation,
            "start_time": time.time(),
            "spans": [],
        }
        self.traces.append(trace)

    def start_span(self, trace_id: str, span_name: str) -> str:
        """Start span."""
        import time
        import uuid

        span_id = str(uuid.uuid4())
        span = {
            "id": span_id,
            "trace_id": trace_id,
            "name": span_name,
            "start_time": time.time(),
        }
        self.spans.append(span)
        return span_id

    def end_span(self, span_id: str) -> None:
        """End span."""
        import time

        for span in self.spans:
            if span["id"] == span_id and "end_time" not in span:
                span["end_time"] = time.time()
                span["duration"] = span["end_time"] - span["start_time"]
                break

    def get_metric_stats(self, name: str) -> dict:
        """Get metric statistics."""
        if name not in self.metrics or not self.metrics[name]:
            return {}

        values = self.metrics[name]
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "p95": sorted(values)[int(len(values) * 0.95)] if values else 0.0,
            "p99": sorted(values)[int(len(values) * 0.99)] if values else 0.0,
        }


def main() -> None:
    """Demonstrate Apm."""
    print("=" * 70)
    print("APM")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Apm")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
