# Readers-Writers Problem

1. **Name of Algorithm**  
   Readers-Writers Problem

2. **What problem does it solve? (1 sentence)**  
   Manages concurrent access to shared resources allowing many readers or one writer at a time.

3. **Intuition (plain-language explanation)**  
   Multiple readers can read simultaneously, but writers require exclusive access.

4. **Inputs & Outputs**  
   - Input: Shared resource, read-write lock or semaphore, reader and writer threads.  
   - Output: Safe concurrent operations without stale reads or write conflicts.

5. **Step-by-step description (5–10 lines max)**  
1. Maintain counters for active readers and waiting writers.
2. Readers acquire shared lock if no writer active.
3. Writers wait until readers finish, then acquire exclusive lock.
4. After operation, release lock and signal waiting threads.
5. Optionally prioritize writers to prevent starvation.

6. **Tiny example (hand-simulated)**  
   Database cache accessed by many read queries but occasionally updated by writers.

7. **Time & Space Complexity**  
   - Time: Lock acquisition typically O(1); throughput depends on contention.  
   - Space: O(1) for counters and lock state.

8. **Strengths**  
- Improves read-heavy workloads by allowing parallel reads.
- Prevents race conditions on shared resources.

9. **Weaknesses / limitations**  
- Complex to implement starvation-free policies.
- Still serialized for write-heavy workloads.

10. **Compare with alternatives**  
    Alternatives: Optimistic Concurrency Control, Stamped Locks, Copy-on-Write

11. **30-second explanation (your own words)**  
    Use read-write synchronization primitives so multiple readers can proceed concurrently while writers get exclusive access.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
