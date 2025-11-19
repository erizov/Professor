#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi Armed Bandit implementation.

This file contains the implementation of the Multi Armed Bandit algorithm.
"""

from typing import List, Optional, Dict, Set


class MultiArmedBandit:
    """Multi-armed bandit algorithm."""

    def __init__(self, num_arms: int = 10):
        self.num_arms = num_arms
        self.counts: List[int] = [0] * num_arms
        self.values: List[float] = [0.0] * num_arms

    def select_arm(self, epsilon: float = 0.1) -> int:
        """Select arm using epsilon-greedy."""
        import random

        if random.random() < epsilon:
            return random.randint(0, self.num_arms - 1)
        return self.values.index(max(self.values))

    def update(self, arm: int, reward: float) -> None:
        """Update arm value."""
        self.counts[arm] += 1
        n = self.counts[arm]
        self.values[arm] = ((n - 1) * self.values[arm] + reward) / n

    def ucb(self, c: float = 2.0) -> int:
        """Upper Confidence Bound selection."""
        import math

        total_counts = sum(self.counts)
        if total_counts == 0:
            return 0

        ucb_values = []
        for i in range(self.num_arms):
            if self.counts[i] == 0:
                ucb_values.append(float("inf"))
            else:
                confidence = c * math.sqrt(math.log(total_counts) / self.counts[i])
                ucb_values.append(self.values[i] + confidence)

        return ucb_values.index(max(ucb_values))


def main() -> None:
    """Demonstrate Multi Armed Bandit."""
    print("=" * 70)
    print("MULTI ARMED BANDIT")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Multi Armed Bandit")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
