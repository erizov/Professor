# Thread Pool

1. **Name of Algorithm**  
   Thread Pool

2. **What problem does it solve? (1 sentence)**  
   Manages a reusable set of worker threads to execute many short-lived tasks without spawning new threads each time.

3. **Intuition (plain-language explanation)**  
   Keep a pool of threads waiting on a work queue; dispatch tasks to idle threads for execution.

4. **Inputs & Outputs**  
   - Input: Task queue, pool size, worker threads, synchronization primitives.  
   - Output: Completed tasks with controlled concurrency level.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize pool with N worker threads.
2. Workers wait for tasks on a blocking queue.
3. Clients submit tasks to the queue.
4. Worker picks up task, executes it, then waits for next task.
5. Pool manages scaling, timeouts, and graceful shutdown.

6. **Tiny example (hand-simulated)**  
   Java ExecutorService processes HTTP requests using a fixed thread pool.

7. **Time & Space Complexity**  
   - Time: Task dispatch O(1) amortized.  
   - Space: O(N + queue_size) for threads and pending tasks.

8. **Strengths**  
- Reduces overhead of thread creation/destruction.
- Controls resource usage by limiting concurrent threads.

9. **Weaknesses / limitations**  
- Improper sizing can cause latency or resource waste.
- Tasks must be well-behaved (no blocking forever).

10. **Compare with alternatives**  
    Alternatives: Event Loop, Reactive Streams, Fork/Join Framework

11. **30-second explanation (your own words)**  
    Pre-create a set of worker threads that repeatedly fetch tasks from a queue, improving throughput and resource control.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
