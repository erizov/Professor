#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Allreduce implementation.

This file contains the implementation of the Allreduce algorithm.
"""

from typing import List, Optional, Dict, Set


def allreduce(data: List[float], operation: str = "sum") -> List[float]:
    """AllReduce operation for distributed computing."""
    # Simplified AllReduce - in practice would use MPI or similar
    n = len(data)
    
    if operation == "sum":
        total = sum(data)
        return [total / n] * n
    elif operation == "max":
        max_val = max(data)
        return [max_val] * n
    elif operation == "min":
        min_val = min(data)
        return [min_val] * n
    elif operation == "avg":
        avg_val = sum(data) / n
        return [avg_val] * n
    
    return data

class AllReduce:
    """AllReduce implementation for distributed training."""
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.gradients: List[List[float]] = []
    
    def reduce(self, gradients: List[float], operation: str = "sum") -> List[float]:
        """Reduce gradients across workers."""
        self.gradients.append(gradients)
        
        if len(self.gradients) == self.num_workers:
            # Aggregate
            aggregated = []
            for i in range(len(gradients)):
                values = [g[i] for g in self.gradients]
                if operation == "sum":
                    aggregated.append(sum(values))
                elif operation == "avg":
                    aggregated.append(sum(values) / len(values))
                else:
                    aggregated.append(values[0])
            
            self.gradients = []
            return aggregated
        
        return gradients


def main() -> None:
    """Demonstrate Allreduce."""
    print("=" * 70)
    print("ALLREDUCE")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Allreduce")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
