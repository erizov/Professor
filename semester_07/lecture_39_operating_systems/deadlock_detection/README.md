# Deadlock Detection

1. **Name of Algorithm**  
   Deadlock Detection

2. **What problem does it solve? (1 sentence)**  
   Identifies deadlock situations where multiple processes are waiting indefinitely for resources held by each other, enabling system recovery and prevention of resource starvation.

3. **Intuition (plain-language explanation)**  
   Like detecting a traffic jam where cars are blocking each other: process A holds resource 1 and waits for resource 2, while process B holds resource 2 and waits for resource 1 - they're stuck forever. Deadlock detection finds these circular wait conditions.

4. **Inputs & Outputs**  
   - Input: Resource allocation graph (processes, resources, allocation edges, request edges), system state snapshot.  
   - Output: Detection of deadlock cycles, list of processes involved in deadlock, recovery recommendations.

5. **Step-by-step description (5–10 lines max)**  
1. Build resource allocation graph: represent processes and resources as nodes, allocations and requests as edges.
2. Detect cycles: search for cycles in the graph (if process A waits for resource held by B, and B waits for resource held by A, there's a cycle).
3. Use cycle detection algorithm: depth-first search (DFS) or wait-for graph analysis to find cycles.
4. Identify deadlocked processes: all processes in a cycle are deadlocked.
5. Report deadlock: notify system or administrator about detected deadlock and involved processes.
6. Recovery options: abort one or more deadlocked processes, preempt resources, or rollback transactions.
7. Prevent recurrence: analyze deadlock to understand cause and implement prevention strategies.
8. Monitor continuously: periodically check for deadlocks in running system.

6. **Tiny example (hand-simulated)**  
   Database system: transaction T1 locks row A, waits for row B → transaction T2 locks row B, waits for row A → deadlock detection: finds cycle T1→A→T2→B→T1 → system aborts T1 (rollback) → T2 completes → deadlock resolved.

7. **Time & Space Complexity**  
   - Time: O(V + E) where V is number of processes/resources, E is number of edges (DFS for cycle detection).  
   - Space: O(V + E) for storing resource allocation graph, O(V) for DFS recursion stack.

8. **Strengths**  
- Enables recovery: detects deadlocks so system can recover.
- Prevents indefinite blocking: identifies processes that will never proceed.
- Diagnostic: helps understand resource contention issues.

9. **Weaknesses / limitations**  
- Overhead: periodic detection adds computational cost.
- Detection delay: deadlock may exist for some time before detection.
- Recovery cost: aborting processes may lose work.

10. **Compare with alternatives**  
    Alternatives: Deadlock Prevention, Deadlock Avoidance, Timeout-based Detection, No Detection (Ostrich Algorithm)

11. **30-second explanation (your own words)**  
    Identifies deadlock situations where multiple processes wait indefinitely for resources held by each other, enabling system recovery through cycle detection in resource allocation graphs.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
