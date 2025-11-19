#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Downsampling implementation.

This file contains the implementation of the Downsampling algorithm.
"""

from typing import List, Optional, Dict, Set


def downsampling(data: List[float], factor: int) -> List[float]:
    """Downsample data."""
    return [data[i] for i in range(0, len(data), factor)]


def upsampling(data: List[float], factor: int) -> List[float]:
    """Upsample data."""
    result = []
    for i in range(len(data)):
        result.append(data[i])
        for _ in range(factor - 1):
            result.append(data[i])
    return result


class TimeSeriesDownsampling:
    """Time series downsampling."""

    def __init__(self):
        self.methods = {
            "mean": lambda chunk: sum(chunk) / len(chunk),
            "max": max,
            "min": min,
        }

    def downsample(
        self, data: List[float], window: int, method: str = "mean"
    ) -> List[float]:
        """Downsample with aggregation."""
        agg_func = self.methods.get(method, self.methods["mean"])
        result = []
        for i in range(0, len(data), window):
            chunk = data[i : i + window]
            if chunk:
                result.append(agg_func(chunk))
        return result


def main() -> None:
    """Demonstrate Downsampling."""
    print("=" * 70)
    print("DOWNSAMPLING")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Downsampling")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
