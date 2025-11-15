#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
0/1 Knapsack Problem - Dynamic Programming.

Given items with weights and values, maximize value without exceeding
weight capacity. Each item can be taken at most once (0/1).
"""

import sys
from pathlib import Path
from typing import List, Tuple

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer


def knapsack_01(weights: List[int], values: List[int], 
                capacity: int) -> Tuple[int, List[int]]:
    """
    Solve 0/1 knapsack problem.
    
    Args:
        weights: List of item weights
        values: List of item values
        capacity: Maximum weight capacity
        
    Returns:
        Tuple of (max_value, selected_items)
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # Build DP table
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i - 1][w]
            
            # Take item i (if weight allows)
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], 
                              dp[i - 1][w - weights[i - 1]] + values[i - 1])
    
    # Reconstruct solution
    max_value = dp[n][capacity]
    selected = []
    w = capacity
    
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= weights[i - 1]
    
    selected.reverse()
    return max_value, selected


def knapsack_01_optimized(weights: List[int], values: List[int],
                          capacity: int) -> int:
    """
    Space-optimized 0/1 knapsack (only value).
    
    Args:
        weights: List of item weights
        values: List of item values
        capacity: Maximum weight capacity
        
    Returns:
        Maximum value
        
    Space Complexity: O(capacity) instead of O(n * capacity)
    """
    n = len(weights)
    dp = [0] * (capacity + 1)
    
    for i in range(n):
        # Iterate backwards to avoid using updated values
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    
    return dp[capacity]


def knapsack_fractional(weights: List[int], values: List[int],
                        capacity: int) -> float:
    """
    Fractional knapsack (greedy algorithm).
    
    Can take fractions of items. Solved optimally with greedy approach.
    
    Args:
        weights: List of item weights
        values: List of item values
        capacity: Maximum weight capacity
        
    Returns:
        Maximum value
    """
    # Calculate value per weight ratio
    items = [(values[i] / weights[i], weights[i], values[i], i)
             for i in range(len(weights))]
    items.sort(reverse=True)  # Sort by value/weight ratio
    
    total_value = 0.0
    remaining_capacity = capacity
    
    for ratio, weight, value, _ in items:
        if remaining_capacity >= weight:
            # Take entire item
            total_value += value
            remaining_capacity -= weight
        else:
            # Take fraction of item
            total_value += ratio * remaining_capacity
            break
    
    return total_value


def main() -> None:
    """Demonstration of Knapsack Problem."""
    print("=" * 70)
    print("0/1 KNAPSACK PROBLEM DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: Basic 0/1 knapsack
    print("Example 1: Basic 0/1 Knapsack")
    print("-" * 70)
    
    weights1 = [10, 20, 30]
    values1 = [60, 100, 120]
    capacity1 = 50
    
    max_value, selected = knapsack_01(weights1, values1, capacity1)
    
    print(f"Weights: {weights1}")
    print(f"Values: {values1}")
    print(f"Capacity: {capacity1}")
    print(f"Maximum value: {max_value}")
    print(f"Selected items (indices): {selected}")
    print(f"Selected weights: {[weights1[i] for i in selected]}")
    print(f"Selected values: {[values1[i] for i in selected]}")
    print(f"Total weight: {sum(weights1[i] for i in selected)}")
    print()
    
    # Example 2: Larger example
    print("Example 2: Larger Example")
    print("-" * 70)
    
    weights2 = [2, 3, 4, 5]
    values2 = [3, 4, 5, 6]
    capacity2 = 5
    
    max_value2, selected2 = knapsack_01(weights2, values2, capacity2)
    
    print(f"Weights: {weights2}")
    print(f"Values: {values2}")
    print(f"Capacity: {capacity2}")
    print(f"Maximum value: {max_value2}")
    print(f"Selected items: {selected2}")
    print()
    
    # Example 3: Space-optimized version
    print("Example 3: Space-Optimized Version")
    print("-" * 70)
    
    weights3 = [1, 3, 4, 5]
    values3 = [1, 4, 5, 7]
    capacity3 = 7
    
    value_standard = knapsack_01(weights3, values3, capacity3)[0]
    value_optimized = knapsack_01_optimized(weights3, values3, capacity3)
    
    print(f"Weights: {weights3}")
    print(f"Values: {values3}")
    print(f"Capacity: {capacity3}")
    print(f"Max value (standard): {value_standard}")
    print(f"Max value (optimized): {value_optimized}")
    print("Note: Optimized uses O(capacity) space instead of O(n*capacity)")
    print()
    
    # Example 4: 0/1 vs Fractional
    print("Example 4: 0/1 Knapsack vs Fractional Knapsack")
    print("-" * 70)
    
    weights4 = [10, 20, 30]
    values4 = [60, 100, 120]
    capacity4 = 50
    
    value_01 = knapsack_01(weights4, values4, capacity4)[0]
    value_fractional = knapsack_fractional(weights4, values4, capacity4)
    
    print(f"Weights: {weights4}")
    print(f"Values: {values4}")
    print(f"Capacity: {capacity4}")
    print(f"0/1 Knapsack (DP): {value_01}")
    print(f"Fractional Knapsack (Greedy): {value_fractional}")
    print("Note: Fractional allows taking parts of items (higher value)")
    print()
    
    # Example 5: Real-world scenario
    print("Example 5: Real-world Scenario - Resource Allocation")
    print("-" * 70)
    
    # Projects with costs and profits
    project_costs = [5, 10, 15, 20, 25]  # Budget required
    project_profits = [10, 20, 30, 40, 50]  # Expected profit
    budget = 40
    
    max_profit, selected_projects = knapsack_01(project_costs, 
                                                project_profits, 
                                                budget)
    
    print("Projects:")
    for i in range(len(project_costs)):
        print(f"  Project {i}: Cost={project_costs[i]}, "
              f"Profit={project_profits[i]}")
    print(f"\nBudget: {budget}")
    print(f"Maximum profit: {max_profit}")
    print(f"Selected projects: {selected_projects}")
    print(f"Total cost: {sum(project_costs[i] for i in selected_projects)}")
    print()
    
    # Example 6: Performance measurement
    print("Example 6: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("Knapsack")
    
    def test_knapsack(n, capacity):
        weights = list(range(1, n + 1))
        values = [w * 2 for w in weights]  # Value = 2 * weight
        return knapsack_01_optimized(weights, values, capacity)
    
    test_cases = [
        (10, 30),
        (20, 50),
        (50, 100),
    ]
    
    for n, cap in test_cases:
        _, metrics = timer.measure(test_knapsack, n, cap)
        print(f"n={n}, capacity={cap}:")
        print(f"  Time: {metrics['execution_time_ms']:.3f} ms")
    
    print()
    print("=" * 70)
    print("\nComplexity Summary:")
    print("  Time:  O(n * capacity)")
    print("  Space: O(n * capacity) - standard")
    print("        O(capacity) - optimized")
    print("\nKey Advantages:")
    print("  - Optimal solution")
    print("  - Can be space-optimized")
    print("  - Handles integer weights/values")
    print("  - Can reconstruct solution")
    print("\nKey Disadvantages:")
    print("  - Pseudo-polynomial (depends on capacity)")
    print("  - Not efficient for large capacities")
    print("  - Only works for integer weights")
    print("\nWhen to Use:")
    print("  - Resource allocation")
    print("  - Budget optimization")
    print("  - Portfolio selection")
    print("  - Cutting stock problem")
    print("  - Project selection")
    print("\nVariations:")
    print("  - Unbounded Knapsack (unlimited items)")
    print("  - Multiple Knapsack")
    print("  - Fractional Knapsack (greedy)")
    print("  - Subset Sum (special case)")
    print("\nCommon Use Cases:")
    print("  - Resource allocation")
    print("  - Budget planning")
    print("  - Investment portfolio")
    print("  - Project selection")
    print("  - Cutting stock problem")
    print("=" * 70)


if __name__ == "__main__":
    main()

