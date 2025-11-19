# SQL Transactions

1. **Name of Algorithm**  
   SQL Transactions

2. **What problem does it solve? (1 sentence)**  
   Bundle multiple statements into an atomic, consistent, isolated, durable unit of work.

3. **Intuition (plain-language explanation)**  
   Either all operations succeed together or none do, safeguarding integrity even under failures.

4. **Inputs & Outputs**  
   - Input: BEGIN/COMMIT/ROLLBACK directives plus SQL statements.  
   - Output: Committed data changes or a rollback to the previous state.

5. **Step-by-step description (5–10 lines max)**  
1. BEGIN (implicit or explicit) starts a transaction context.
2. Execute one or more SQL statements.
3. If all succeed, issue COMMIT to persist changes.
4. On error or manual cancel, issue ROLLBACK to undo.
5. DBMS enforces ACID properties via logging and locking.

6. **Tiny example (hand-simulated)**  
   Transfer funds: debit one account, credit another, COMMIT only if both succeed; else ROLLBACK.

7. **Time & Space Complexity**  
   - Time: Depends on enclosed statements; logging adds small overhead.  
   - Space: Requires log space for redo/undo records.

8. **Strengths**  
- Protects data integrity under concurrency and crashes.
- Simplifies multi-step operations for developers.

9. **Weaknesses / limitations**  
- Excessive transaction scope can cause contention.
- Long transactions hold locks, reducing throughput.

10. **Compare with alternatives**  
    Alternatives: Eventual consistency workflows, Application-level compensation logic

11. **30-second explanation (your own words)**  
    Group related statements so they behave as a single all-or-nothing change, ensuring ACID guarantees.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
