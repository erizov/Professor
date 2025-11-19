# Gossip Protocol

1. **Name of Algorithm**  
   Gossip Protocol

2. **What problem does it solve? (1 sentence)**  
   Disseminates state information in large-scale distributed systems using epidemic-style message spreading for scalability and fault tolerance.

3. **Intuition (plain-language explanation)**  
   Like rumors spreading: each node periodically contacts random peers to exchange updates, so information eventually reaches everyone without central coordination.

4. **Inputs & Outputs**  
   - Input: Cluster of nodes, heartbeat/state data, gossip interval, fan-out (number of peers per round).  
   - Output: Eventual consistency of membership or state across nodes.

5. **Step-by-step description (5–10 lines max)**  
1. Each node maintains local state (heartbeats, version vectors).
2. On each tick, select k random peers.
3. Send local state digests; peers reconcile by merging newer entries.
4. Update detection timers to suspect failed nodes lacking fresh heartbeats.
5. Propagate membership changes (join/leave/fail) via subsequent gossip rounds.
6. Tune fan-out and interval to balance convergence speed and bandwidth.

6. **Tiny example (hand-simulated)**  
   Amazon Dynamo-style membership: every 1s, node gossips to 3 peers; failure detected after missing N heartbeats across multiple peers.

7. **Time & Space Complexity**  
   - Time: Each round O(k) messages per node; convergence typically O(log n) rounds to reach all nodes.  
   - Space: O(n) per node to track membership metadata.

8. **Strengths**  
- Highly fault-tolerant and decentralized.
- Scales to thousands of nodes with bounded load.

9. **Weaknesses / limitations**  
- Only eventually consistent; temporary disagreement possible.
- Bandwidth usage grows with state size.

10. **Compare with alternatives**  
    Alternatives: Centralized Membership Service, Raft/Consensus-based registries, Multicast/Broadcast protocols

11. **30-second explanation (your own words)**  
    Nodes periodically exchange membership/state updates with random peers, allowing information to percolate through the cluster without a coordinator.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
