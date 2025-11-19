# Process Scheduling

1. **Name of Algorithm**  
   Process Scheduling

2. **What problem does it solve? (1 sentence)**  
   Determines which process runs on CPU at any given time, managing process execution order to maximize CPU utilization, ensure fairness, and meet real-time constraints.

3. **Intuition (plain-language explanation)**  
   Like a traffic controller managing cars at an intersection: the scheduler decides which process (car) gets to use the CPU (intersection) next, considering priorities (emergency vehicles first), fairness (everyone gets a turn), and efficiency (keep traffic flowing).

4. **Inputs & Outputs**  
   - Input: Ready processes, process priorities, scheduling algorithm, CPU time quantum, process states.  
   - Output: Process execution order, CPU allocation decisions, process state transitions (running, ready, waiting).

5. **Step-by-step description (5–10 lines max)**  
1. Maintain ready queue: keep list of processes ready to execute, ordered by scheduling algorithm.
2. Select process: choose next process to run based on scheduling algorithm (FCFS, Round-Robin, Priority, etc.).
3. Context switch: save current process state (registers, program counter), load selected process state.
4. Dispatch process: give CPU to selected process, change process state to running.
5. Monitor execution: track process execution time, check for I/O requests or time quantum expiration.
6. Preempt process: if time quantum expires or higher-priority process arrives, interrupt current process.
7. Update statistics: record process execution time, waiting time, turnaround time.
8. Reschedule: when process blocks (I/O) or time quantum expires, return to step 2 to select next process.

6. **Tiny example (hand-simulated)**  
   Round-Robin scheduling: 3 processes (P1, P2, P3), time quantum 10ms → P1 runs 10ms → preempt → P2 runs 10ms → preempt → P3 runs 10ms → preempt → back to P1 → cycle repeats → all processes get fair CPU time.

7. **Time & Space Complexity**  
   - Time: O(1) for simple algorithms (FCFS, Round-Robin), O(log n) for priority queues, O(n) for some algorithms where n is number of processes.  
   - Space: O(n) for storing n processes in ready queue, O(1) per process for process control block (PCB).

8. **Strengths**  
- Maximizes utilization: keeps CPU busy by switching between processes.
- Fairness: ensures all processes get CPU time (depending on algorithm).
- Responsive: enables multitasking and interactive applications.

9. **Weaknesses / limitations**  
- Overhead: context switching consumes CPU time.
- Complexity: scheduling algorithms must balance multiple objectives.
- Starvation: some algorithms may starve low-priority processes.

10. **Compare with alternatives**  
    Alternatives: Cooperative Multitasking, Single-tasking, Gang Scheduling, Real-time Scheduling

11. **30-second explanation (your own words)**  
    Determines which process runs on CPU at any given time, managing process execution order to maximize CPU utilization, ensure fairness, and meet real-time constraints through various scheduling algorithms.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
