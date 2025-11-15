#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Q-Learning implementation."""

import time
import sys
from pathlib import Path

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from framework.performance_timer import PerformanceTimer


def q_learning():
    """
    Implement Q-Learning.
    
    Category: Reinforcement Learning
    Time Complexity: O(states*actions)
    Space Complexity: O(states*actions)
    """
    print("==" * 35)
    print("Q-Learning")
    print("==" * 35)
    print(f"Category: Reinforcement Learning")
    print(f"Time Complexity: O(states*actions)")
    print(f"Space Complexity: O(states*actions)")
    print()
    print("Resource Requirements:")
    print("  - GPU: Optional")
    print("  - Memory: Medium")
    print("==" * 35)


if __name__ == "__main__":
    timer = PerformanceTimer("Q-Learning")
    _, metrics = timer.measure(q_learning)
    print(f"\nExecution time: {metrics['execution_time_ms']:.3f} ms")
    print(f"Memory used: {metrics['memory_peak_kb']:.2f} KB")
