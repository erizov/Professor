#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cpu Scheduling Advanced implementation.

This file contains the implementation of the Cpu Scheduling Advanced algorithm.
"""

from typing import List, Optional, Dict, Set


class CPUSchedulerAdvanced:
    """Advanced CPU scheduling algorithms."""
    def __init__(self):
        self.processes: List[dict] = []
        self.current_time = 0
    
    def add_process(self, process_id: str, arrival_time: float,
                   burst_time: float, priority: int = 0) -> None:
        """Add process."""
        self.processes.append({
            "id": process_id,
            "arrival": arrival_time,
            "burst": burst_time,
            "priority": priority,
            "remaining": burst_time,
            "wait_time": 0.0,
            "turnaround_time": 0.0
        })
    
    def round_robin(self, time_quantum: float = 2.0) -> List[str]:
        """Round-robin scheduling."""
        queue = sorted(self.processes, key=lambda p: p["arrival"])
        result = []
        current_time = 0.0
        
        while queue:
            process = queue.pop(0)
            if process["remaining"] <= time_quantum:
                current_time += process["remaining"]
                process["turnaround_time"] = current_time - process["arrival"]
                result.append(process["id"])
            else:
                current_time += time_quantum
                process["remaining"] -= time_quantum
                queue.append(process)
                result.append(process["id"])
        
        return result
    
    def priority_scheduling(self) -> List[str]:
        """Priority scheduling."""
        sorted_processes = sorted(self.processes, 
                                 key=lambda p: (p["priority"], p["arrival"]))
        result = []
        current_time = 0.0
        
        for process in sorted_processes:
            current_time += process["burst"]
            process["turnaround_time"] = current_time - process["arrival"]
            result.append(process["id"])
        
        return result
    
    def shortest_job_first(self) -> List[str]:
        """Shortest Job First scheduling."""
        sorted_processes = sorted(self.processes, 
                                 key=lambda p: (p["arrival"], p["burst"]))
        result = []
        current_time = 0.0
        
        for process in sorted_processes:
            if current_time < process["arrival"]:
                current_time = process["arrival"]
            current_time += process["burst"]
            process["turnaround_time"] = current_time - process["arrival"]
            result.append(process["id"])
        
        return result


def main() -> None:
    """Demonstrate Cpu Scheduling Advanced."""
    print("=" * 70)
    print("CPU SCHEDULING ADVANCED")
    print("=" * 70)
    
    # Example usage
    print("Algorithm implementation for Cpu Scheduling Advanced")
    print("See implementation above for details.")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
