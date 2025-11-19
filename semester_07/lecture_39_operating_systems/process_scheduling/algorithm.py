#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Process Scheduling implementation.

This file contains the implementation of the Process Scheduling algorithm.
"""

from typing import List, Optional, Dict, Set


class ProcessScheduler:
    """Process scheduler."""

    def __init__(self, algorithm: str = "fcfs"):
        self.processes: List[dict] = []
        self.algorithm = algorithm

    def add_process(
        self, process_id: str, arrival_time: float, burst_time: float, priority: int = 0
    ) -> None:
        """Add process."""
        self.processes.append(
            {
                "id": process_id,
                "arrival": arrival_time,
                "burst": burst_time,
                "priority": priority,
                "status": "ready",
            }
        )

    def schedule(self) -> Optional[dict]:
        """Schedule next process."""
        if not self.processes:
            return None

        ready = [p for p in self.processes if p["status"] == "ready"]
        if not ready:
            return None

        if self.algorithm == "fcfs":
            return min(ready, key=lambda p: p["arrival"])
        elif self.algorithm == "sjf":
            return min(ready, key=lambda p: p["burst"])
        elif self.algorithm == "priority":
            return min(ready, key=lambda p: p["priority"])
        return ready[0]


def main() -> None:
    """Demonstrate Process Scheduling."""
    print("=" * 70)
    print("PROCESS SCHEDULING")
    print("=" * 70)

    # Example usage
    print("Algorithm implementation for Process Scheduling")
    print("See implementation above for details.")

    print("=" * 70)


if __name__ == "__main__":
    main()
