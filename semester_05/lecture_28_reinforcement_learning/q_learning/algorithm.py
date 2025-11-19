#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Q Learning implementation.

This file contains the implementation of the Q Learning algorithm.
"""

from typing import List, Optional, Dict, Set


class QLearning:
    """Q-Learning algorithm."""

    def __init__(
        self,
        state_size: int,
        action_size: int,
        lr: float = 0.1,
        gamma: float = 0.99,
        epsilon: float = 0.1,
    ):
        self.state_size = state_size
        self.action_size = action_size
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table: Dict[tuple, List[float]] = {}

    def get_state_key(self, state: List[float]) -> tuple:
        """Convert state to key."""
        return tuple(round(s, 2) for s in state)

    def get_q_values(self, state: List[float]) -> List[float]:
        """Get Q-values for state."""
        key = self.get_state_key(state)
        if key not in self.q_table:
            self.q_table[key] = [0.0] * self.action_size
        return self.q_table[key]

    def choose_action(self, state: List[float]) -> int:
        """Choose action using epsilon-greedy."""
        import random

        if random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)

        q_values = self.get_q_values(state)
        return q_values.index(max(q_values))

    def update(
        self,
        state: List[float],
        action: int,
        reward: float,
        next_state: List[float],
        done: bool,
    ) -> None:
        """Update Q-value."""
        q_values = self.get_q_values(state)
        next_q_values = self.get_q_values(next_state)

        max_next_q = max(next_q_values) if not done else 0.0
        target = reward + self.gamma * max_next_q

        q_values[action] = q_values[action] + self.lr * (target - q_values[action])
        self.q_table[self.get_state_key(state)] = q_values


def main() -> None:
    """Demonstrate Q Learning."""
    print("=" * 70)
    print("Q LEARNING")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Q Learning")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
