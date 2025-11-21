# Raft Blockchain

1. **Name of Algorithm**  

## Code Files


## Algorithm Visualization

### Flowchart (ASCII)


```
Raft Blockchain Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Initialize │
│   data      │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Process   ├──────┐
│  condition?│      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│  Execute   │      │
│  operation │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│    End      │
└─────────────┘
```


### Step-by-Step Execution


```
Raft Blockchain Step-by-Step Execution:

Input: [example data]

Step 1: Initialize
State: [initial state]

Step 2: Process
State: [intermediate state]

Step 3: Finalize
State: [final state]

Result: [output]
```


### Interactive Flowchart (Mermaid)


```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize data]
    Init --> Process{Process condition}
    Process -->|True| Execute[Execute operation]
    Execute --> Done{Complete?}
    Done -->|No| Process
    Done -->|Yes| End([End])
    Process -->|False| End
```


> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.
- [Python Implementation](semester_13/lecture_88_consensus_advanced/raft_blockchain/algorithm.py)
- [Java Implementation](semester_13/lecture_88_consensus_advanced/raft_blockchain/Algorithm.java)
- [Python Tests](semester_13/lecture_88_consensus_advanced/raft_blockchain/test_algorithm.py)


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
