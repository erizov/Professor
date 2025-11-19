# NoSQL Sharding

1. **Name of Algorithm**  
   NoSQL Sharding

2. **What problem does it solve? (1 sentence)**  
   Partitions large datasets across multiple database nodes (shards) based on shard key, enabling horizontal scaling and distributing data and load across cluster.

3. **Intuition (plain-language explanation)**  
   Like dividing a large library into sections: NoSQL sharding is like splitting a huge library into smaller sections (shards) - instead of one massive library (single database), you have multiple smaller libraries (shards) organized by topic (shard key) - when you need a book, you know which section to go to (which shard), making it faster and allowing the library to grow by adding more sections.

4. **Inputs & Outputs**  
   - Input: Dataset, shard key, number of shards, sharding strategy, cluster nodes.  
   - Output: Sharded database, distributed data, balanced load, scalable system.

5. **Step-by-step description (5–10 lines max)**  
1. Choose shard key: select field(s) to partition data (e.g., user_id, region).
2. Determine shards: decide number of shards and shard boundaries.
3. Assign nodes: assign each shard to a database node.
4. Partition data: distribute data across shards based on shard key.
5. Route queries: route queries to appropriate shard(s) based on shard key.
6. Balance: ensure data and load are evenly distributed across shards.
7. Monitor: track shard sizes, query distribution, and performance.
8. Reshard: redistribute data if shards become unbalanced or cluster grows.

6. **Tiny example (hand-simulated)**  
   MongoDB sharding: shard key = user_id → 3 shards → shard 1: user_id 0-999, shard 2: user_id 1000-1999, shard 3: user_id 2000-2999 → query for user_id=1500 → routed to shard 2 → fast lookup → data distributed → can add more shards as data grows.

7. **Time & Space Complexity**  
   - Time: O(1) for shard routing, O(n/k) for queries where n is data size, k is number of shards (parallel processing).  
   - Space: O(d/k) per shard where d is total data, k is number of shards (data partitioned).

8. **Strengths**  
- Horizontal scaling: enables scaling by adding more shards.
- Performance: queries only access relevant shard(s), improving speed.
- Load distribution: distributes read/write load across multiple nodes.

9. **Weaknesses / limitations**  
- Shard key selection: poor shard key can cause uneven distribution.
- Cross-shard queries: queries spanning multiple shards are complex.
- Resharding: moving data between shards can be expensive.

10. **Compare with alternatives**  
    Alternatives: Single Database, Replication, Partitioning, Vertical Scaling

11. **30-second explanation (your own words)**  
    Partitions large datasets across multiple database nodes (shards) based on shard key, enabling horizontal scaling and distributing data and load across cluster.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
