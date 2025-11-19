# Consistent Hashing

1. **Name of Algorithm**  
   Consistent Hashing

2. **What problem does it solve? (1 sentence)**  
   Distributes keys across dynamic clusters so adding/removing nodes only remaps a small fraction of keys, enabling scalable caches and storage rings.

3. **Intuition (plain-language explanation)**  
   Hash both nodes and keys onto a ring; each key goes to the next clockwise node, so membership changes affect only neighboring intervals.

4. **Inputs & Outputs**  
   - Input: Set of server nodes, hash function, replication factor, key identifiers.  
   - Output: Deterministic mapping from keys to nodes (and replicas).

5. **Step-by-step description (5–10 lines max)**  
1. Hash each node (optionally multiple virtual nodes) onto 0..2^m ring.
2. Hash each key onto same ring.
3. Assign key to first node clockwise from key hash.
4. Replicate by selecting subsequent clockwise nodes.
5. When node joins/leaves, reassign only keys in affected ranges.
6. Rebalance by adjusting virtual node count per server.

6. **Tiny example (hand-simulated)**  
   Distributed cache (Amazon Dynamo): each cache server owns ring intervals; adding a node only migrates ~1/n of keys.

7. **Time & Space Complexity**  
   - Time: Lookup O(log n) using balanced tree of node positions; O(1) with jump hash approximations.  
   - Space: O(n · v) for n nodes with v virtual replicas stored in ring map.

8. **Strengths**  
- Minimal key reshuffling on node churn.
- Supports heterogenous node capacity via virtual nodes.

9. **Weaknesses / limitations**  
- Requires uniform hash distribution; hotspots possible.
- Rebalancing metadata adds operational complexity.

10. **Compare with alternatives**  
    Alternatives: Jump Consistent Hash, Rendezvous Hashing, Modulo Hashing

11. **30-second explanation (your own words)**  
    Places nodes and keys on the same hash ring so keys map to nearest clockwise node, limiting the amount of data moved during topology changes.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
