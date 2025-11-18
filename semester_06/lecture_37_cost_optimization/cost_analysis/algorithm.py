#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cost Analysis implementation.

This file contains the implementation of the Cost Analysis algorithm.
"""

from typing import List, Optional, Dict, Set


class CostAnalysis:
    """Cost analysis system."""
    def __init__(self):
        self.costs: List[dict] = {}
        self.categories: Dict[str, List[float]] = {}
    
    def record_cost(self, cost_id: str, amount: float, category: str,
                   description: str) -> None:
        """Record cost."""
        import time
        self.costs[cost_id] = {
            "amount": amount,
            "category": category,
            "description": description,
            "timestamp": time.time()
        }
        
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(amount)
    
    def get_total_cost(self, start_time: float = None, 
                      end_time: float = None) -> float:
        """Get total cost."""
        total = 0.0
        for cost in self.costs.values():
            if start_time and cost["timestamp"] < start_time:
                continue
            if end_time and cost["timestamp"] > end_time:
                continue
            total += cost["amount"]
        return total
    
    def get_cost_by_category(self) -> Dict[str, float]:
        """Get costs by category."""
        result = {}
        for category, amounts in self.categories.items():
            result[category] = sum(amounts)
        return result
    
    def get_average_cost(self, category: str = None) -> float:
        """Get average cost."""
        if category:
            amounts = self.categories.get(category, [])
            return sum(amounts) / len(amounts) if amounts else 0.0
        
        all_amounts = [cost["amount"] for cost in self.costs.values()]
        return sum(all_amounts) / len(all_amounts) if all_amounts else 0.0


def main() -> None:
    """Demonstrate Cost Analysis."""
    print("=" * 70)
    print("COST ANALYSIS")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Cost Analysis")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
