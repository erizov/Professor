#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R-CNN implementation."""

import time
import sys
from pathlib import Path

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from framework.performance_timer import PerformanceTimer


def rcnn():
    """
    Implement R-CNN.
    
    Category: Computer Vision
    Time Complexity: O(n*proposals)
    Space Complexity: O(proposals)
    """
    print("==" * 35)
    print("R-CNN")
    print("==" * 35)
    print(f"Category: Computer Vision")
    print(f"Time Complexity: O(n*proposals)")
    print(f"Space Complexity: O(proposals)")
    print()
    print("Resource Requirements:")
    print("  - GPU: Optional")
    print("  - Memory: Medium")
    print("==" * 35)


if __name__ == "__main__":
    timer = PerformanceTimer("R-CNN")
    _, metrics = timer.measure(rcnn)
    print(f"\nExecution time: {metrics['execution_time_ms']:.3f} ms")
    print(f"Memory used: {metrics['memory_peak_kb']:.2f} KB")
