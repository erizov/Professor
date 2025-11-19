# Consensus Algorithms

1. **Name of Algorithm**  
   Consensus Algorithms

2. **What problem does it solve? (1 sentence)**  
   Enables multiple distributed nodes to agree on a single value or decision despite network failures, node failures, and message delays, ensuring consistency in distributed systems.

3. **Intuition (plain-language explanation)**  
   Like a group vote: consensus algorithms are like getting a group of people to agree on a decision - even if some people are absent (node failures), messages are delayed (network issues), or people disagree initially, It ensures everyone eventually agrees on the same decision - it's like a democratic process where you need a majority vote, but it handles cases where votes might arrive late or some voters might be unavailable.

4. **Inputs & Outputs**  
   - Input: Node proposals, votes, network messages, node states, failure models.  
   - Output: Agreed value, consensus decision, consistent state across nodes.

5. **Step-by-step description (5–10 lines max)**  
1. Propose: nodes propose values they want to agree on.
2. Communicate: nodes exchange proposals and votes via network.
3. Collect: each node collects proposals from other nodes.
4. Vote: nodes vote on proposed values.
5. Count: count votes, determine if majority reached.
6. Decide: if majority agrees, nodes decide on agreed value.
7. Commit: nodes commit to the decided value.
8. Propagate: propagate decision to all nodes.
9. Handle failures: tolerate node failures and network partitions.
10. Ensure safety: guarantee all nodes agree on same value (safety).
11. Ensure liveness: guarantee system eventually reaches consensus (liveness).

6. **Tiny example (hand-simulated)**  
   Consensus: 5 nodes, 3 propose X, 2 propose Y → voting: 3 votes for X, 2 votes for Y → majority: X (3 > 5/2) → decision: all nodes agree on X → commit: all nodes commit X → consistency: all nodes have same value → consensus achieved.

7. **Time & Space Complexity**  
   - Time: O(n) to O(n²) depending on algorithm where n is number of nodes.  
   - Space: O(n) where n is number of nodes (state storage per node).

8. **Strengths**  
- Consistency: ensures all nodes agree on same value.
- Fault tolerance: tolerates node and network failures.
- Fundamental: essential for distributed systems consistency.

9. **Weaknesses / limitations**  
- Latency: may have high latency due to message exchanges.
- Complexity: consensus algorithms can be complex.
- Trade-offs: must balance between safety, liveness, and performance.

10. **Compare with alternatives**  
    Alternatives: Raft, Paxos, PBFT, Tendermint, Two-Phase Commit

11. **30-second explanation (your own words)**  
    Enables multiple distributed nodes to agree on a single value or decision despite network failures, node failures, and message delays, ensuring consistency in distributed systems.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
