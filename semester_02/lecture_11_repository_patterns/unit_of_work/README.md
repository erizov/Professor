# Unit of Work

1. **Name of Algorithm**  
   Unit of Work

2. **What problem does it solve? (1 sentence)**  
   Tracks changes to multiple business objects and coordinates a single transaction commit to ensure consistency.

3. **Intuition (plain-language explanation)**  
   Accumulate inserts/updates/deletes in memory, then write them as one atomic unit.

4. **Inputs & Outputs**  
   - Input: Tracked entities, change tracker, transaction boundary.  
   - Output: Persisted state or rolled-back transaction if errors occur.

5. **Step-by-step description (5–10 lines max)**  
1. Start a unit of work and attach entities.
2. Track changes (new, dirty, removed) as domain logic runs.
3. On commit, issue database commands in correct order within a transaction.
4. On rollback, discard pending changes.
5. Dispose unit of work at end of request.

6. **Tiny example (hand-simulated)**  
   EF Core DbContext tracks entity states; SaveChanges commits them within a transaction.

7. **Time & Space Complexity**  
   - Time: Depends on number of tracked entities; typically O(n) to iterate changes.  
   - Space: O(n) to store entity state and pending commands.

8. **Strengths**  
- Ensures transactional consistency across repositories.
- Reduces database round-trips by batching writes.

9. **Weaknesses / limitations**  
- Requires careful lifetime management to avoid stale state.
- Can consume memory if many entities are tracked.

10. **Compare with alternatives**  
    Alternatives: Explicit Transactions, Command Pattern, Saga Pattern

11. **30-second explanation (your own words)**  
    Buffer database operations in memory and commit them together so partial failures do not leave inconsistent state.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
