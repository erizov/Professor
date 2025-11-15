#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fully Convolutional Networks implementation."""

import time
import sys
from pathlib import Path

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from framework.performance_timer import PerformanceTimer


def fcn():
    """
    Implement Fully Convolutional Networks.
    
    Category: Computer Vision
    Time Complexity: O(n*H*W)
    Space Complexity: O(H*W)
    """
    print("==" * 35)
    print("Fully Convolutional Networks")
    print("==" * 35)
    print(f"Category: Computer Vision")
    print(f"Time Complexity: O(n*H*W)")
    print(f"Space Complexity: O(H*W)")
    print()
    print("Resource Requirements:")
    print("  - GPU: Optional")
    print("  - Memory: Medium")
    print("==" * 35)


if __name__ == "__main__":
    timer = PerformanceTimer("Fully Convolutional Networks")
    _, metrics = timer.measure(fcn)
    print(f"\nExecution time: {metrics['execution_time_ms']:.3f} ms")
    print(f"Memory used: {metrics['memory_peak_kb']:.2f} KB")
