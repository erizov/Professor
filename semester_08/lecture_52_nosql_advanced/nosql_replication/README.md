# NoSQL Replication

1. **Name of Algorithm**  
   NoSQL Replication

2. **What problem does it solve? (1 sentence)**  
   Maintains multiple copies of NoSQL data across distributed nodes, enabling high availability, fault tolerance, and load distribution in distributed NoSQL systems.

3. **Intuition (plain-language explanation)**  
   Like backup copies for NoSQL: NoSQL replication creates multiple copies of data across different servers (like making photocopies and storing them in different locations) - if one server fails, others continue serving data (like having backup copies), and read requests can be distributed across copies (like multiple people reading different copies), improving performance and reliability.

4. **Inputs & Outputs**  
   - Input: Primary data, replication configuration, replication strategy (master-slave, master-master, etc.), network topology.  
   - Output: Replicated data copies, high availability, fault tolerance, load distribution.

5. **Step-by-step description (5–10 lines max)**  
1. Configure replication: set up replication strategy (master-slave, peer-to-peer, etc.).
2. Select nodes: choose nodes to participate in replication.
3. Initial sync: copy existing data from primary to replica nodes.
4. Monitor changes: track data changes (writes, updates, deletes) on primary.
5. Replicate changes: propagate changes to replica nodes (synchronously or asynchronously).
6. Apply changes: replicas apply changes to maintain consistency.
7. Handle conflicts: resolve conflicts in multi-master replication.
8. Failover: automatically promote replica to primary if primary fails.
9. Monitor: track replication lag and ensure replicas stay synchronized.

6. **Tiny example (hand-simulated)**  
   MongoDB replica set: primary node in New York → replicate to secondary nodes in London and Tokyo → writes go to primary → changes replicated to secondaries → reads can go to any node → if primary fails → automatic election → London becomes primary → zero downtime → high availability.

7. **Time & Space Complexity**  
   - Time: O(1) for replication setup, O(n) for initial sync where n is data size, O(1) per operation for ongoing replication.  
   - Space: O(d·r) where d is data size, r is replication factor (each replica stores full copy).

8. **Strengths**  
- High availability: system continues operating if nodes fail.
- Load distribution: read queries distributed across replicas.
- Fault tolerance: data survives node failures.

9. **Weaknesses / limitations**  
- Replication lag: replicas may be slightly behind primary.
- Storage cost: requires multiple copies of data.
- Complexity: managing replication across distributed nodes is complex.

10. **Compare with alternatives**  
    Alternatives: Single Node, Sharding, Backup and Restore, Clustering

11. **30-second explanation (your own words)**  
    Maintains multiple copies of NoSQL data across distributed nodes, enabling high availability, fault tolerance, and load distribution in distributed NoSQL systems.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
