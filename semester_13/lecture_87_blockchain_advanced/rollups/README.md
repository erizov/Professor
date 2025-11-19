# Rollups

1. **Name of Algorithm**  
   Rollups

2. **What problem does it solve? (1 sentence)**  
   Scales blockchain by executing transactions off-chain, batching them, and submitting compressed transaction data and state roots to the main chain, achieving high throughput with main chain security.

3. **Intuition (plain-language explanation)**  
   Like a shipping container: Rollups are like shipping containers - instead of shipping items individually (expensive), you pack many items into a container (batch transactions), compress it (compress data), and ship the container (submit to main chain) - this reduces shipping costs (fees) while maintaining security (main chain validation).

4. **Inputs & Outputs**  
   - Input: Transactions, rollup sequencer, compression algorithm, state transitions, validity proofs (optional).  
   - Output: Rollup blocks, compressed transaction data, state roots, validity proofs (ZK-Rollups), fraud proofs (Optimistic Rollups).

5. **Step-by-step description (5–10 lines max)**  
1. Collect: collect transactions from users.
2. Execute: execute transactions off-chain (in rollup).
3. Batch: batch multiple transactions together.
4. Compress: compress transaction data.
5. Compute: compute new state root.
6. Prove: generate validity proof (ZK-Rollup) or prepare for fraud proof (Optimistic).
7. Submit: submit batch to main chain.
8. Verify: verify proof on main chain (ZK) or wait for challenge period (Optimistic).
9. Finalize: finalize state on main chain.
10. Settle: settle disputes if needed (Optimistic).

6. **Tiny example (hand-simulated)**  
   Rollup: collect 1000 tx → execute off-chain → batch → compress 1000 tx to 10KB → compute root → submit to main chain → verify → finalize → Rollup successful (100x cheaper).

7. **Time & Space Complexity**  
   - Time: O(b + v) where b is batch processing time, v is verification time (rollup operations).  
   - Space: O(c + s) where c is compressed data, s is state storage (rollup storage).

8. **Strengths**  
- Scalability: 10-100x throughput improvement.
- Security: inherits main chain security.
- Cost: significantly reduces transaction fees.

9. **Weaknesses / limitations**  
- Latency: some delay for finality (especially Optimistic).
- Complexity: requires sophisticated compression and proof systems.
- Centralization: sequencer can be centralized point of failure.

10. **Compare with alternatives**  
    Alternatives: Plasma, Sidechains, State Channels, Sharding

11. **30-second explanation (your own words)**  
    Layer 2 scaling solutions that execute transactions off-chain, batch and compress them, then submit to the main chain, achieving high throughput with main chain security guarantees.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
