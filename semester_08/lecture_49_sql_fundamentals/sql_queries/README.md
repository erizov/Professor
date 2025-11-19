# SQL Queries

1. **Name of Algorithm**  
   SQL Queries

2. **What problem does it solve? (1 sentence)**  
   Retrieve, filter, and manipulate relational data using declarative statements.

3. **Intuition (plain-language explanation)**  
   Describe the desired result set while the optimizer chooses an execution plan.

4. **Inputs & Outputs**  
   - Input: SQL statement (SELECT/INSERT/UPDATE/DELETE) plus database schema/data.  
   - Output: Result set, affected row count, or updated storage state.

5. **Step-by-step description (5–10 lines max)**  
1. Parse the SQL statement.
2. Validate against schema and permissions.
3. Generate a logical plan (joins, filters, projections).
4. Optimize into a physical plan using indexes and statistics.
5. Execute the plan and stream results back to the client.

6. **Tiny example (hand-simulated)**  
   SELECT name FROM customers WHERE country='Canada'; returns matching customer names.

7. **Time & Space Complexity**  
   - Time: Varies; indexed lookups approach O(log n), full scans O(n).  
   - Space: Driven by execution plan (temporary joins, sorting buffers).

8. **Strengths**  
- Declarative syntax hides implementation details.
- Mature optimizers leverage indexes and caches.

9. **Weaknesses / limitations**  
- Poorly written queries can degrade to full scans.
- Requires understanding of indexes and statistics for tuning.

10. **Compare with alternatives**  
    Alternatives: NoSQL query APIs, ORM-generated queries, Stored procedures

11. **30-second explanation (your own words)**  
    State what data you want, let the relational engine decide how to fetch it efficiently.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
