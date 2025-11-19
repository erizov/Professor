# Raft Blockchain

1. **Name of Algorithm**  
   Raft Blockchain

2. **What problem does it solve? (1 sentence)**  
   Implements Raft consensus algorithm for blockchains, providing a simpler alternative to Paxos with strong leader-based consensus, used in blockchain systems for fast and understandable consensus.

3. **Intuition (plain-language explanation)**  
   Like democratic leadership: Raft is like democratic leadership - you elect a leader (like electing a president) who makes decisions, and if the leader fails, you elect a new one - just as democratic leadership is understandable, Raft provides understandable consensus.

4. **Inputs & Outputs**  
   - Input: Transactions, nodes, leader election, log replication, consensus parameters.  
   - Output: Consensus decisions, replicated logs, finalized blocks, leader-based consensus, secure blockchain.

5. **Step-by-step description (5–10 lines max)**  
1. Elect: elect leader through voting.
2. Propose: leader proposes transactions.
3. Replicate: leader replicates log to followers.
4. Append: followers append to log.
5. Commit: commit after majority acknowledgment.
6. Apply: apply committed entries.
7. Heartbeat: leader sends heartbeats.
8. Re-elect: re-elect if leader fails.
9. Repeat: repeat for next entries.
10. Optimize: optimize consensus performance.

6. **Tiny example (hand-simulated)**  
   Raft Blockchain: nodes: 5 nodes → elect: node 1 elected leader → propose: leader proposes block → replicate: replicate to 4 followers → commit: 3 nodes acknowledge → result: block committed, consensus reached → Raft Blockchain successful.

7. **Time & Space Complexity**  
   - Time: O(n) where n is nodes (linear message complexity).  
   - Space: O(n + l) where n is nodes, l is log length (node and log storage).

8. **Strengths**  
- Simplicity: simpler than Paxos, easier to understand.
- Performance: fast consensus with strong leader.
- Safety: provides strong safety guarantees.

9. **Weaknesses / limitations**  
- Leader: requires leader (single point of coordination).
- Partition: may have issues with network partitions.
- Blockchain: designed for traditional distributed systems, adapted for blockchain.

10. **Compare with alternatives**  
    Alternatives: Paxos, PBFT, Proof of Stake, Other Consensus

11. **30-second explanation (your own words)**  
    Implements Raft consensus algorithm for blockchains, providing a simpler alternative to Paxos with strong leader-based consensus, used in blockchain systems for fast and understandable consensus.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
