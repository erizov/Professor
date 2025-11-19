# Priority Queue

1. **Name of Algorithm**  
   Priority Queue

2. **What problem does it solve? (1 sentence)**  
   Manages elements where highest (or lowest) priority item is always accessible, regardless of insertion order.

3. **Intuition (plain-language explanation)**  
   Like a hospital emergency room: the most urgent case gets treated first, even if others arrived earlier.

4. **Inputs & Outputs**  
   - Input: Sequence of enqueue (insert) and dequeue (extract) operations with priority values.  
   - Output: Always returns the highest priority element on dequeue.

5. **Step-by-step description (5–10 lines max)**  
1. Choose underlying data structure (binary heap, Fibonacci heap, etc.).
2. Enqueue: insert element with its priority value.
3. Dequeue: extract and return element with highest/lowest priority.
4. Update priority: modify existing element's priority (if supported).
5. Maintain heap property to ensure O(log n) operations.

6. **Tiny example (hand-simulated)**  
   Enqueue tasks: (A,5), (B,9), (C,3). Dequeue returns B (priority 9), then A (5), then C (3).

7. **Time & Space Complexity**  
   - Time: O(log n) enqueue/dequeue with binary heap; O(1) amortized with Fibonacci heap.  
   - Space: O(n) to store n elements.

8. **Strengths**  
- Essential for scheduling, graph algorithms, and event simulation.
- Efficient access to extremal elements.

9. **Weaknesses / limitations**  
- No efficient random access or search operations.
- Requires total ordering of priorities.

10. **Compare with alternatives**  
    Alternatives: Sorted Array, Balanced BST, Skip List

11. **30-second explanation (your own words)**  
A data structure that always gives you the most important item first, perfect for scheduling and optimization.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
