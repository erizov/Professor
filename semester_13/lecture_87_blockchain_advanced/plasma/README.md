# Plasma

1. **Name of Algorithm**  
   Plasma

2. **What problem does it solve? (1 sentence)**  
   Scales blockchain transactions by creating child chains (Plasma chains) that process transactions off the main chain and periodically commit state roots, reducing main chain congestion and fees.

3. **Intuition (plain-language explanation)**  
   Like branch offices: Plasma is like a company with branch offices - the main office (main chain) doesn't handle every transaction, instead branch offices (Plasma chains) handle most transactions locally and only report summaries (state roots) to the main office - this reduces workload on the main office while maintaining security through fraud proofs.

4. **Inputs & Outputs**  
   - Input: Transactions, Plasma chain configuration, operator, state commitments, fraud proofs, exit requests.  
   - Output: Plasma chain blocks, state roots, committed transactions, exit proofs, scaled throughput.

5. **Step-by-step description (5–10 lines max)**  
1. Create: create Plasma child chain with operator.
2. Process: process transactions on Plasma chain (off-chain).
3. Commit: commit state roots to main chain periodically.
4. Validate: validate transactions using fraud proofs.
5. Exit: allow users to exit to main chain with proofs.
6. Challenge: challenge invalid state transitions.
7. Settle: settle disputes using fraud proofs.
8. Withdraw: withdraw funds to main chain after exit period.
9. Monitor: monitor Plasma chain for fraud.
10. Maintain: maintain Plasma chain security and liveness.

6. **Tiny example (hand-simulated)**  
   Plasma: create chain → process 1000 tx/s on Plasma → commit root every 10 blocks → user exits → submit exit proof → wait 7 days → withdraw to main chain → Plasma successful.

7. **Time & Space Complexity**  
   - Time: O(t + c) where t is transaction processing time, c is commitment time (Plasma operations).  
   - Space: O(s + p) where s is state storage, p is proof storage (Plasma storage).

8. **Strengths**  
- Scalability: significantly increases transaction throughput.
- Cost: reduces transaction fees on main chain.
- Flexibility: supports various Plasma chain designs.

9. **Weaknesses / limitations**  
- Complexity: complex exit and fraud proof mechanisms.
- Security: requires users to monitor for fraud.
- Liquidity: exit periods can lock funds temporarily.

10. **Compare with alternatives**  
    Alternatives: Rollups, Sidechains, State Channels, Sharding

11. **30-second explanation (your own words)**  
    A Layer 2 scaling solution that creates child chains that process transactions off-chain and commit state roots to the main chain, enabling high throughput while maintaining security.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
