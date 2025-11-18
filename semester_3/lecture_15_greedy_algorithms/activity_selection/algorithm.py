#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Activity Selection implementation.

This file contains the implementation of the Activity Selection algorithm.
"""

from typing import List, Optional, Dict, Set


def activity_selection(start: List[int], finish: List[int]) -> List[int]:
    """Activity selection problem using greedy approach."""
    n = len(finish)
    activities = list(zip(start, finish, range(n)))
    activities.sort(key=lambda x: x[1])  # Sort by finish time
    
    selected = [activities[0][2]]
    last_finish = activities[0][1]
    
    for i in range(1, n):
        if activities[i][0] >= last_finish:
            selected.append(activities[i][2])
            last_finish = activities[i][1]
    
    return selected


def main() -> None:
    """Demonstrate Activity Selection."""
    print("=" * 70)
    print("ACTIVITY SELECTION")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Activity Selection")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
