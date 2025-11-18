#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cost Optimization implementation.

This file contains the implementation of the Cost Optimization algorithm.
"""

from typing import List, Optional, Dict, Set


class CostOptimizer:
    """Cost optimization system."""
    def __init__(self):
        self.resources: Dict[str, dict] = {}
        self.cost_history: List[dict] = []
    
    def register_resource(self, resource_id: str, resource_type: str, 
                         cost_per_hour: float) -> None:
        """Register resource."""
        self.resources[resource_id] = {
            "type": resource_type,
            "cost_per_hour": cost_per_hour,
            "usage_hours": 0.0
        }
    
    def record_usage(self, resource_id: str, hours: float) -> None:
        """Record resource usage."""
        if resource_id in self.resources:
            self.resources[resource_id]["usage_hours"] += hours
            import time
            self.cost_history.append({
                "resource_id": resource_id,
                "hours": hours,
                "cost": hours * self.resources[resource_id]["cost_per_hour"],
                "timestamp": time.time()
            })
    
    def calculate_total_cost(self, start_time: Optional[float] = None, 
                           end_time: Optional[float] = None) -> float:
        """Calculate total cost."""
        costs = self.cost_history
        if start_time:
            costs = [c for c in costs if c["timestamp"] >= start_time]
        if end_time:
            costs = [c for c in costs if c["timestamp"] <= end_time]
        
        return sum(c["cost"] for c in costs)
    
    def get_cost_recommendations(self) -> List[str]:
        """Get cost optimization recommendations."""
        recommendations = []
        
        # Find underutilized resources
        for resource_id, resource in self.resources.items():
            if resource["usage_hours"] < 10:  # Less than 10 hours
                recommendations.append(f"Consider removing underutilized resource: {resource_id}")
        
        return recommendations


def main() -> None:
    """Demonstrate Cost Optimization."""
    print("=" * 70)
    print("COST OPTIMIZATION")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Cost Optimization")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
