# NoSQL Indexing

1. **Name of Algorithm**  
   NoSQL Indexing

2. **What problem does it solve? (1 sentence)**  
   Creates indexes on NoSQL database fields to accelerate queries and searches, enabling fast data retrieval without scanning entire collections or tables.

3. **Intuition (plain-language explanation)**  
   Like an index in a book, but for NoSQL: NoSQL indexing creates lookup structures (like book indexes) that map field values to document/row locations - instead of scanning every document (like reading every page), you look up the value in the index (like using a book index) and jump directly to the right documents (like jumping to the right pages), making queries much faster.

4. **Inputs & Outputs**  
   - Input: Field names, index type, collection/table, index configuration.  
   - Output: Index structures, faster queries, improved search performance.

5. **Step-by-step description (5–10 lines max)**  
1. Identify fields: determine which fields are frequently queried.
2. Choose index type: select appropriate index type (B-tree, hash, text, geospatial, etc.).
3. Create index: build index structure mapping field values to document/row locations.
4. Store index: save index alongside data (in-memory or on-disk).
5. Update index: maintain index when data is inserted, updated, or deleted.
6. Use in queries: query engine uses index to speed up searches.
7. Monitor: track index usage and performance impact.
8. Optimize: adjust indexes based on query patterns and performance.

6. **Tiny example (hand-simulated)**  
   MongoDB collection: users (1M documents) → query: find users where age = 25 → without index: scans 1M documents (slow) → create index on age → with index: lookup age=25 in index → find document locations → retrieve documents → query time: 0.01s vs 1s (100x faster).

7. **Time & Space Complexity**  
   - Time: O(log n) for B-tree indexes, O(1) for hash indexes, O(n) for collection scans without index.  
   - Space: O(n) where n is number of indexed documents/rows (additional storage for index).

8. **Strengths**  
- Query performance: dramatically speeds up queries on indexed fields.
- Flexible: supports various index types (single field, compound, text, geospatial).
- Scalable: indexes can be distributed across nodes in distributed systems.

9. **Weaknesses / limitations**  
- Storage overhead: indexes require additional storage space.
- Write overhead: INSERT/UPDATE/DELETE operations must update indexes.
- Index maintenance: requires monitoring and optimization.

10. **Compare with alternatives**  
    Alternatives: Full Collection Scans, Materialized Views, Caching, Denormalization

11. **30-second explanation (your own words)**  
    Creates indexes on NoSQL database fields to accelerate queries and searches, enabling fast data retrieval without scanning entire collections or tables.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
