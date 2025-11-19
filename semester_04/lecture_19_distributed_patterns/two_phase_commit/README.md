# Two-Phase Commit (2PC)

1. **Name of Algorithm**  
   Two-Phase Commit (2PC)

2. **What problem does it solve? (1 sentence)**  
   Coordinates distributed transactions across multiple participants to achieve atomic commit or abort.

3. **Intuition (plain-language explanation)**  
   Use a coordinator that first collects votes (prepare phase) and then instructs all participants to commit or roll back in unison.

4. **Inputs & Outputs**  
   - Input: Coordinator node, participant nodes, transaction data, persistent logs.  
   - Output: Consistent commit/abort decision replicated to all participants.

5. **Step-by-step description (5–10 lines max)**  
1. Coordinator sends PREPARE to participants asking if they can commit.
2. Each participant votes YES (and logs intent) or NO, then waits.
3. If all YES, coordinator logs COMMIT and sends COMMIT messages; otherwise sends ABORT.
4. Participants apply action (commit/abort), log outcome, and acknowledge.
5. Coordinator cleans up after receiving acknowledgements.
6. Recovery: participants replay logs to determine final decision on restart.

6. **Tiny example (hand-simulated)**  
   Bank transfer across databases: coordinator ensures both debit and credit either commit or abort together to maintain consistency.

7. **Time & Space Complexity**  
   - Time: Two rounds of messaging O(n) plus logging.  
   - Space: O(n) for participants' logs and coordinator state.

8. **Strengths**  
- Provides atomicity across heterogeneous systems.
- Simple protocol widely implemented in databases/message brokers.

9. **Weaknesses / limitations**  
- Blocking: participants must wait if coordinator crashes.
- Does not tolerate coordinator failure without extra protocols (3PC).

10. **Compare with alternatives**  
    Alternatives: Three-Phase Commit, Paxos/Raft Transactions, Saga Pattern

11. **30-second explanation (your own words)**  
    Uses a coordinator-driven prepare/commit handshake so either all participants commit or all abort, ensuring distributed atomicity at the cost of blocking.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
