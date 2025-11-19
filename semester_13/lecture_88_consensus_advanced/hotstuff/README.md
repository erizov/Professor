# HotStuff

1. **Name of Algorithm**  
   HotStuff

2. **What problem does it solve? (1 sentence)**  
   Achieves Byzantine fault tolerance with linear message complexity and optimistic responsiveness using a three-phase consensus protocol with a rotating leader and pipelined block proposals.

3. **Intuition (plain-language explanation)**  
   Like an efficient assembly line: HotStuff is like an efficient assembly line with a rotating supervisor (leader) - instead of stopping the line for each decision (expensive), the line keeps moving (pipelining) while the supervisor coordinates (three-phase consensus) - if the supervisor is slow, you rotate to a new one (leader change) - this enables fast, efficient consensus even with leader failures.

4. **Inputs & Outputs**  
   - Input: Transactions, leader rotation, replicas, consensus messages, timeout mechanisms.  
   - Output: Committed blocks, consensus certificates, leader decisions, pipelined proposals.

5. **Step-by-step description (5–10 lines max)**  
1. Propose: leader proposes block with sequence number.
2. Prepare: replicas vote on proposal (prepare phase).
3. Pre-commit: if prepared, replicas pre-commit.
4. Commit: if pre-committed, replicas commit.
5. Pipeline: pipeline multiple proposals for efficiency.
6. Rotate: rotate leader if timeout or failure.
7. Sync: synchronize on committed blocks.
8. Optimize: use optimistic path when leader is honest.
9. Recover: recover from leader failures quickly.
10. Finalize: finalize committed blocks.

6. **Tiny example (hand-simulated)**  
   HotStuff: leader proposes block 100 → prepare votes → pre-commit → commit → pipeline block 101 → commit block 100 → HotStuff successful (linear messages, fast).

7. **Time & Space Complexity**  
   - Time: O(n) message complexity, O(1) latency in optimistic case where n is replicas (HotStuff complexity).  
   - Space: O(n) for replica state, O(b) for pipelined blocks (HotStuff storage).

8. **Strengths**  
- Efficiency: linear message complexity (O(n) vs O(n²)).
- Speed: fast consensus with optimistic responsiveness.
- Robustness: handles leader failures gracefully.

9. **Weaknesses / limitations**  
- Complexity: more complex than basic BFT protocols.
- Leader: performance depends on leader quality.
- Pipelining: requires careful synchronization.

10. **Compare with alternatives**  
    Alternatives: Practical Byzantine Fault Tolerance, Raft, Tendermint, Algorand

11. **30-second explanation (your own words)**  
    A Byzantine fault-tolerant consensus protocol with linear message complexity and optimistic responsiveness, using a three-phase protocol with pipelined block proposals.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
