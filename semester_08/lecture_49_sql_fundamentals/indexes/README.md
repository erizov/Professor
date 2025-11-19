# Database Indexes

1. **Name of Algorithm**  
   Database Indexes

2. **What problem does it solve? (1 sentence)**  
   Accelerates data retrieval by creating ordered data structures that map column values to row locations, enabling fast lookups without scanning entire tables.

3. **Intuition (plain-language explanation)**  
   Like a book index: instead of reading every page to find a topic (full table scan), an index lists topics with page numbers (column values with row pointers) - you look up the topic in the index (fast) and jump directly to the right page (row), making searches much faster.

4. **Inputs & Outputs**  
   - Input: Table columns, index type (B-tree, hash, bitmap, etc.), index definition.  
   - Output: Index structure, faster query performance, additional storage overhead.

5. **Step-by-step description (5–10 lines max)**  
1. Choose columns: identify columns frequently used in WHERE, JOIN, ORDER BY clauses.
2. Select index type: choose appropriate index type (B-tree for range queries, hash for equality, etc.).
3. Create index: build index structure mapping column values to row locations.
4. Store index: save index data structure alongside table data.
5. Update index: maintain index when table data is inserted, updated, or deleted.
6. Use in queries: query optimizer uses index to speed up data retrieval.
7. Monitor: track index usage and performance impact.
8. Maintain: periodically rebuild or reorganize indexes to optimize performance.

6. **Tiny example (hand-simulated)**  
   Table: users (1M rows) → query: SELECT * FROM users WHERE email = 'user@example.com' → without index: scans 1M rows (slow) → create index on email → with index: lookup email in index → find row pointer → retrieve row directly → query time: 0.001s vs 1s (1000x faster).

7. **Time & Space Complexity**  
   - Time: O(log n) for B-tree index lookups, O(1) for hash indexes, O(n) for full table scan without index.  
   - Space: O(n) where n is number of indexed rows (additional storage for index structure).

8. **Strengths**  
- Fast lookups: dramatically speeds up SELECT queries with WHERE clauses.
- Efficient sorting: enables fast ORDER BY operations.
- Join optimization: speeds up JOIN operations on indexed columns.

9. **Weaknesses / limitations**  
- Storage overhead: indexes require additional disk space.
- Write overhead: INSERT/UPDATE/DELETE operations must update indexes.
- Maintenance: indexes need periodic maintenance and optimization.

10. **Compare with alternatives**  
    Alternatives: Full Table Scans, Materialized Views, Partitioning, Caching

11. **30-second explanation (your own words)**  
    Accelerates data retrieval by creating ordered data structures that map column values to row locations, enabling fast lookups without scanning entire tables.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
