#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test framework components."""

print("Testing Framework Components...")
print("=" * 70)

# Test 1: Performance Timer
try:
    from framework.performance_timer import PerformanceTimer

    print("✓ Performance Timer imported successfully")

    timer = PerformanceTimer("Test")
    result, metrics = timer.measure(sorted, [3, 1, 2])
    print(f"✓ Performance measurement works: {metrics['execution_time_ms']:.3f} ms")
except Exception as e:
    print(f"✗ Performance Timer error: {e}")

# Test 2: Constraint Selector
try:
    from framework.constraint_selector import (
        AlgorithmSelector,
        Constraints,
        ResourceLevel,
    )

    print("✓ Constraint Selector imported successfully")

    constraints = Constraints(memory=ResourceLevel.LOW)
    rec = AlgorithmSelector.select_sorting_algorithm(constraints)
    print(f"✓ Algorithm recommendation works: {rec['recommended']}")
except Exception as e:
    print(f"✗ Constraint Selector error: {e}")

# Test 3: Check algorithms exist
try:
    from pathlib import Path

    base_path = Path(__file__).resolve().parents[1]
    count = len(list(base_path.glob("semester_*/lecture_*/*")))
    print(f"✓ Found {count} algorithm folders")
except Exception as e:
    print(f"✗ Algorithm count error: {e}")

print("=" * 70)
print("Framework test complete!")
