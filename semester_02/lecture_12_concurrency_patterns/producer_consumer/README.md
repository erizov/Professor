# Producer-Consumer Pattern

1. **Name of Algorithm**  
   Producer-Consumer Pattern

2. **What problem does it solve? (1 sentence)**  
   Coordinates multiple producers generating work items and consumers processing them while preventing race conditions.

3. **Intuition (plain-language explanation)**  
   Use a thread-safe queue or buffer; producers enqueue tasks, consumers dequeue and handle them.

4. **Inputs & Outputs**  
   - Input: Set of producer threads, consumer threads, shared buffer, synchronization primitives.  
   - Output: Processed tasks with controlled throughput.

5. **Step-by-step description (5–10 lines max)**  
1. Create bounded/unbounded thread-safe queue.
2. Producers acquire lock (or use concurrent queue) and push items.
3. If queue full, producers block or drop depending on policy.
4. Consumers wait for items, then dequeue and process.
5. Use condition variables/semaphores to signal availability.

6. **Tiny example (hand-simulated)**  
   Web server thread pool: accept requests (producer), worker threads handle responses (consumers).

7. **Time & Space Complexity**  
   - Time: Each enqueue/dequeue typically O(1).  
   - Space: O(capacity) for buffer.

8. **Strengths**  
- Smooths load differences between producers and consumers.
- Simplifies synchronization via shared queue.

9. **Weaknesses / limitations**  
- Requires careful tuning of buffer size.
- Potential for deadlock if signaling is incorrect.

10. **Compare with alternatives**  
    Alternatives: Actor Model, Pipeline Pattern, Reactive Streams

11. **30-second explanation (your own words)**  
    Buffer work items in a synchronized queue so producers and consumers operate independently without data races.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
