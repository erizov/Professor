import types
import json
import builtins
import io
from pathlib import Path
from typing import Any, Dict

import pytest

from framework.performance_timer import PerformanceTimer, benchmark, ResourceAnalyzer, compare_algorithms


# ----------------------------
# Helpers / Fakes for testing
# ----------------------------
class FakeTracemalloc:
    def __init__(self):
        self._started = False
        self.snapshots = []
        self.current = 10 * 1024
        self.peak = 20 * 1024

    def start(self):
        self._started = True

    def get_traced_memory(self):
        assert self._started, "tracemalloc must be started before reading memory"
        # Return fixed current and peak for determinism
        return self.current, self.peak

    def stop(self):
        self._started = False


class FakeTimer:
    def __init__(self, increments):
        self.increments = iter(increments)
        self.now = 0.0

    def perf_counter(self):
        try:
            inc = next(self.increments)
        except StopIteration:
            inc = 0.0
        self.now += inc
        return self.now


# ----------------------------
# Behaviors
# ----------------------------
# 1) PerformanceTimer.measure returns function result and records deterministic metrics
# 2) PerformanceTimer.get_summary aggregates min/avg/max correctly across runs
# 3) benchmark decorator generates datasets and prints summary while returning original result
# 4) ResourceAnalyzer.analyze_constraints sets suitability levels and recommendations based on metrics/complexities
# 5) compare_algorithms prints a single-line summary per algorithm and uses PerformanceTimer internally


@pytest.fixture
def fake_env(monkeypatch):
    # Patch time.perf_counter deterministically
    ft = FakeTimer([0.1, 0.2, 0.3, 0.4, 0.5])
    monkeypatch.setattr('framework.performance_timer.time', types.SimpleNamespace(perf_counter=ft.perf_counter))

    # Patch tracemalloc
    fake_tm = FakeTracemalloc()
    monkeypatch.setattr('framework.performance_timer.tracemalloc', fake_tm)

    return ft, fake_tm


def test_measure_returns_result_and_metrics(fake_env):
    timer = PerformanceTimer("adder")

    def add(a, b):
        return a + b

    result, metrics = timer.measure(add, 2, 3)

    # Result is correct
    assert result == 5
    # Metrics contain expected keys
    assert set(metrics.keys()) == {"execution_time_ms", "memory_current_kb", "memory_peak_kb", "input_size"}
    # Memory figures reflect fake tracemalloc
    assert metrics["memory_current_kb"] == pytest.approx(10.0, rel=1e-6)
    assert metrics["memory_peak_kb"] == pytest.approx(20.0, rel=1e-6)
    # Input size sums only sized args (ints have no __len__)
    assert metrics["input_size"] == 0


def test_summary_aggregates_min_avg_max(fake_env):
    timer = PerformanceTimer("noop")

    def noop(x):
        return x

    # Execute measure multiple times with different time deltas
    timer.measure(noop, [1])  # 0.1 ms-equivalent step (scaled to ms later)
    timer.measure(noop, [1, 2])
    timer.measure(noop, [1, 2, 3])

    summary = timer.get_summary()
    assert summary["algorithm"] == "noop"
    assert summary["runs"] == 3

    times = summary["time"]
    assert times["min_ms"] <= times["avg_ms"] <= times["max_ms"]

    mem = summary["memory"]
    assert mem["min_kb"] == pytest.approx(20.0) or mem["min_kb"] == pytest.approx(20.0)
    assert mem["max_kb"] == pytest.approx(20.0)


def test_benchmark_decorator_prints_and_returns(fake_env, capsys):
    # Define a simple sort function to trigger dataset generation path
    @benchmark(dataset_sizes=[3, 5])
    def demo_sort(arr):
        return sorted(arr)

    # Call wrapped function with a concrete list (return value should be preserved)
    out = demo_sort([3, 2, 1])
    assert out == [1, 2, 3]

    captured = capsys.readouterr().out
    # Should contain header and lines for both sizes
    assert "Benchmarking demo_sort" in captured
    assert "n=     3:" in captured
    assert "n=     5:" in captured
    assert "Performance Summary: demo_sort" in captured


def test_resource_analyzer_analyze_and_print(capsys):
    metrics = {
        'time': {'avg_ms': 5.0},
        'memory': {'avg_kb': 50.0}
    }
    analysis = ResourceAnalyzer.analyze_constraints(
        algorithm_name='AlgoX',
        time_complexity='O(n log n)',
        space_complexity='O(1)',
        metrics=metrics,
    )

    # Check key fields
    assert analysis['algorithm'] == 'AlgoX'
    assert analysis['constraints']['low_memory'] == 'EXCELLENT'
    assert analysis['constraints']['low_cpu'] == 'GOOD'
    assert analysis['constraints']['distributed'] == 'GOOD'
    assert analysis['constraints']['edge'] == 'EXCELLENT'
    assert any('Suitable for memory-constrained' in r for r in analysis['recommendations'])

    # Validate print output
    ResourceAnalyzer.print_analysis(analysis)
    out = capsys.readouterr().out
    assert 'Resource Constraint Analysis: AlgoX' in out
    assert 'Time:  O(n log n)' in out
    assert 'Space: O(1)' in out


def test_compare_algorithms_uses_timer_and_prints(fake_env, capsys):
    # Two trivial algorithms
    def f1(arr):
        return arr

    def f2(arr):
        return list(reversed(arr))

    compare_algorithms([
        ("noop", f1),
        ("reverse", f2),
    ], dataset_size=10)

    out = capsys.readouterr().out
    # Header and two lines for the algorithms
    assert 'Algorithm Comparison (n=10)' in out
    assert 'noop' in out
    assert 'reverse' in out
