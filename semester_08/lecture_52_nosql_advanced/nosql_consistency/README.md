# NoSQL Consistency Models

1. **Name of Algorithm**  
   NoSQL Consistency Models

2. **What problem does it solve? (1 sentence)**  
   Defines data consistency guarantees in distributed NoSQL systems, balancing between strong consistency (ACID) and eventual consistency (BASE) based on application requirements.

3. **Intuition (plain-language explanation)**  
   Like different levels of synchronization: NoSQL consistency models are like different ways to keep multiple copies in sync - strong consistency is like everyone reading the same book at the same time (always up-to-date, but slower), while eventual consistency is like everyone having their own copy that eventually syncs (faster, but may have temporary differences) - you choose based on whether you need immediate accuracy or can tolerate temporary inconsistencies.

4. **Inputs & Outputs**  
   - Input: Consistency model type, replication configuration, application requirements, CAP theorem trade-offs.  
   - Output: Consistency guarantees, data synchronization behavior, performance characteristics.

5. **Step-by-step description (5–10 lines max)**  
1. Choose model: select consistency model (strong, eventual, causal, session, etc.).
2. Configure replication: set up replication with chosen consistency guarantees.
3. Define rules: establish rules for read/write consistency (read-your-writes, monotonic reads, etc.).
4. Implement: implement consistency mechanisms (vector clocks, version vectors, etc.).
5. Monitor: track consistency violations and synchronization lag.
6. Tune: adjust consistency levels based on performance and accuracy requirements.
7. Handle conflicts: implement conflict resolution for eventual consistency.
8. Document: document consistency guarantees for application developers.

6. **Tiny example (hand-simulated)**  
   NoSQL database with eventual consistency → write to node A → replicate to nodes B, C → read from node B (may see old data temporarily) → eventually all nodes sync → all reads see same data → trade-off: faster writes, eventual accuracy vs strong consistency: slower writes, immediate accuracy.

7. **Time & Space Complexity**  
   - Time: O(1) for eventual consistency (fast), O(n) for strong consistency where n is number of replicas (slower due to coordination).  
   - Space: O(r) where r is replication overhead (vector clocks, version vectors).

8. **Strengths**  
- Performance: eventual consistency enables high performance and availability.
- Scalability: allows distributed systems to scale horizontally.
- Flexibility: can choose consistency level based on use case.

9. **Weaknesses / limitations**  
- Complexity: managing consistency in distributed systems is complex.
- Conflict resolution: eventual consistency requires conflict resolution strategies.
- Application complexity: developers must handle potential inconsistencies.

10. **Compare with alternatives**  
    Alternatives: Strong Consistency (ACID), Eventual Consistency (BASE), Causal Consistency, Session Consistency

11. **30-second explanation (your own words)**  
    Defines data consistency guarantees in distributed NoSQL systems, balancing between strong consistency (ACID) and eventual consistency (BASE) based on application requirements.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
