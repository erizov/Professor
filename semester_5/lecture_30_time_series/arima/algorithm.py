#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ARIMA implementation."""

import time
import sys
from pathlib import Path

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from framework.performance_timer import PerformanceTimer


def arima():
    """
    Implement ARIMA.
    
    Category: Time Series
    Time Complexity: O(n*p*d*q)
    Space Complexity: O(n)
    """
    print("==" * 35)
    print("ARIMA")
    print("==" * 35)
    print(f"Category: Time Series")
    print(f"Time Complexity: O(n*p*d*q)")
    print(f"Space Complexity: O(n)")
    print()
    print("Resource Requirements:")
    print("  - GPU: Optional")
    print("  - Memory: Medium")
    print("==" * 35)


if __name__ == "__main__":
    timer = PerformanceTimer("ARIMA")
    _, metrics = timer.measure(arima)
    print(f"\nExecution time: {metrics['execution_time_ms']:.3f} ms")
    print(f"Memory used: {metrics['memory_peak_kb']:.2f} KB")
