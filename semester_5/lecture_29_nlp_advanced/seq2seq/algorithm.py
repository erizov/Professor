#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sequence-to-Sequence implementation."""

import time
import sys
from pathlib import Path

# Add framework to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from framework.performance_timer import PerformanceTimer


def seq2seq():
    """
    Implement Sequence-to-Sequence.
    
    Category: NLP
    Time Complexity: O(n*m*d)
    Space Complexity: O(n*d)
    """
    print("==" * 35)
    print("Sequence-to-Sequence")
    print("==" * 35)
    print(f"Category: NLP")
    print(f"Time Complexity: O(n*m*d)")
    print(f"Space Complexity: O(n*d)")
    print()
    print("Resource Requirements:")
    print("  - GPU: Optional")
    print("  - Memory: Medium")
    print("==" * 35)


if __name__ == "__main__":
    timer = PerformanceTimer("Sequence-to-Sequence")
    _, metrics = timer.measure(seq2seq)
    print(f"\nExecution time: {metrics['execution_time_ms']:.3f} ms")
    print(f"Memory used: {metrics['memory_peak_kb']:.2f} KB")
