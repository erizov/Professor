# Leader Election

1. **Name of Algorithm**  
   Leader Election

2. **What problem does it solve? (1 sentence)**  
   Selects a single coordinator among distributed nodes to serialize actions (e.g., lock management, replication control).

3. **Intuition (plain-language explanation)**  
   Nodes compete based on priorities (IDs, timestamps); the "highest" remaining alive becomes leader and others defer until failure triggers a new election.

4. **Inputs & Outputs**  
   - Input: Cluster membership, node identifiers/priorities, communication channel (message passing).  
   - Output: Identity of the current leader and election status.

5. **Step-by-step description (5–10 lines max)**  
1. Detect need for election (startup or leader failure).
2. Each candidate broadcasts election message to higher-priority nodes.
3. If no higher node responds, candidate declares leadership.
4. Leader announces victory; others acknowledge and follow.
5. Monitor leader heartbeats; on timeout, restart election.
6. Persist leader metadata to avoid split-brain where possible.

6. **Tiny example (hand-simulated)**  
Bully algorithm: nodes have unique IDs; highest ID node alive becomes coordinator. ZooKeeper/Etcd use Raft to elect leader for log replication.

7. **Time & Space Complexity**  
   - Time: Bully algorithm worst-case O(n^2) messages; consensus-based elections ~O(n).  
   - Space: O(n) to track membership and leader state.

8. **Strengths**  
- Ensures single coordinator for critical sections.
- Detects failures and reconfigures automatically.

9. **Weaknesses / limitations**  
- Susceptible to split-brain without quorum/consensus safeguards.
- Frequent elections can disrupt system stability.

10. **Compare with alternatives**  
    Alternatives: Raft Consensus, Paxos, Randomized Leader Rotation

11. **30-second explanation (your own words)**  
    Runs a coordination protocol so exactly one node assumes leadership while others remain followers, with re-election triggered on leader failure.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
