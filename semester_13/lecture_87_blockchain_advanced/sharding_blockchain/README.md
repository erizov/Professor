# Blockchain Sharding

1. **Name of Algorithm**  
   Blockchain Sharding

2. **What problem does it solve? (1 sentence)**  
   Scales blockchain by partitioning the network into multiple shards that process transactions in parallel, each maintaining its own state and transaction history, enabling horizontal scaling.

3. **Intuition (plain-language explanation)**  
   Like dividing a library into sections: Blockchain sharding is like dividing a library into sections (shards) - instead of everyone using one catalog (single chain), each section has its own catalog (shard) - people can use different sections simultaneously (parallel processing), and the library (network) can handle more visitors (transactions) overall.

4. **Inputs & Outputs**  
   - Input: Transactions, shard assignment, validators, cross-shard communication, consensus mechanism.  
   - Output: Shard blocks, cross-shard transactions, aggregated state, network-wide consensus.

5. **Step-by-step description (5–10 lines max)**  
1. Partition: partition network into multiple shards.
2. Assign: assign validators to shards (randomly or by stake).
3. Route: route transactions to appropriate shards.
4. Process: process transactions within each shard in parallel.
5. Consensus: reach consensus within each shard.
6. Cross-shard: handle cross-shard transactions.
7. Aggregate: aggregate shard states periodically.
8. Sync: synchronize shard states across network.
9. Validate: validate cross-shard transactions.
10. Finalize: finalize shard blocks and network state.

6. **Tiny example (hand-simulated)**  
   Sharding: partition into 4 shards → assign validators → route tx to shard 2 → process in parallel → consensus in shard 2 → cross-shard tx to shard 3 → aggregate → Sharding successful (4x throughput).

7. **Time & Space Complexity**  
   - Time: O(t/s + c) where t is transactions, s is shards, c is cross-shard overhead (sharded complexity).  
   - Space: O(n/s) per shard where n is total state, s is shards (sharded storage).

8. **Strengths**  
- Scalability: linear scaling with number of shards.
- Parallelism: enables parallel transaction processing.
- Efficiency: reduces storage and processing per node.

9. **Weaknesses / limitations**  
- Complexity: complex cross-shard communication and consensus.
- Security: smaller shards may be more vulnerable to attacks.
- Synchronization: requires careful state synchronization.

10. **Compare with alternatives**  
    Alternatives: Rollups, Plasma, Sidechains, State Channels

11. **30-second explanation (your own words)**  
    A scaling technique that partitions the blockchain into multiple shards that process transactions in parallel, enabling horizontal scaling of transaction throughput.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
