# Caching

1. **Name of Algorithm**  
   Caching

2. **What problem does it solve? (1 sentence)**  
   Stores frequently accessed data in fast storage to reduce latency and load on primary data sources, improving application performance.

3. **Intuition (plain-language explanation)**  
   Like keeping frequently used items on your desk: instead of going to storage (database) every time, grab from desk (cache) for instant access.

4. **Inputs & Outputs**  
   - Input: Data to cache, cache key, TTL (time-to-live), cache eviction policy.  
   - Output: Cached data with fast retrieval and reduced load on primary sources.

5. **Step-by-step description (5–10 lines max)**  
1. Check cache for requested data using key.
2. If cache hit: return cached data immediately.
3. If cache miss: fetch from primary source (database, API).
4. Store fetched data in cache with TTL.
5. Return data to caller.
6. Evict expired or least-recently-used entries when cache full.

6. **Tiny example (hand-simulated)**  
   User requests product info → check cache for product:123 → miss → fetch from database → store in cache (TTL 1 hour) → return. Next request hits cache instantly.

7. **Time & Space Complexity**  
   - Time: O(1) for cache lookup (hash table); O(n) for primary source fetch.  
   - Space: O(n) for cached data (bounded by cache size limit).

8. **Strengths**  
- Dramatically reduces latency for frequently accessed data.
- Reduces load on primary data sources.

9. **Weaknesses / limitations**  
- Cache invalidation complexity.
- Memory overhead for cached data.

10. **Compare with alternatives**  
    Alternatives: CDN, Database Query Optimization, In-Memory Databases

11. **30-second explanation (your own words)**  
    Stores frequently accessed data in fast storage (memory) to enable instant retrieval and reduce load on slower primary data sources.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
