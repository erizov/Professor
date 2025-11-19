# PBFT (Practical Byzantine Fault Tolerance)

1. **Name of Algorithm**  
   PBFT (Practical Byzantine Fault Tolerance)

2. **What problem does it solve? (1 sentence)**  
   Implements PBFT consensus algorithm, a Byzantine fault-tolerant consensus protocol that tolerates up to (n-1)/3 Byzantine failures in a network of n nodes, providing fast finality and high throughput.

3. **Intuition (plain-language explanation)**  
   Like agreement despite liars: PBFT is like reaching agreement even when some people lie (Byzantine failures) - you need 2/3 honest nodes to agree, and you can tolerate up to 1/3 liars - just as you can reach consensus despite some dishonest participants, PBFT reaches consensus despite Byzantine failures.

4. **Inputs & Outputs**  
   - Input: Transactions, validators, consensus parameters, Byzantine fault tolerance, network messages.  
   - Output: Consensus decisions, finalized blocks, fast finality, high throughput, secure blockchain.

5. **Step-by-step description (5–10 lines max)**  
1. Request: client sends request to primary.
2. Pre-prepare: primary broadcasts pre-prepare message.
3. Prepare: validators send prepare messages.
4. Commit: validators send commit messages after 2f+1 prepares.
5. Reply: validators reply to client after 2f+1 commits.
6. Finalize: finalize block after consensus.
7. View-change: change view if primary fails.
8. Verify: verify message authenticity.
9. Repeat: repeat for next block.
10. Optimize: optimize consensus performance.

6. **Tiny example (hand-simulated)**  
   PBFT: validators: 4 validators (tolerates 1 Byzantine) → request: client request → pre-prepare: primary broadcasts → prepare: 3 validators prepare → commit: 3 validators commit → result: consensus reached, block finalized → PBFT successful.

7. **Time & Space Complexity**  
   - Time: O(n²) where n is validators (message complexity, but fast in practice).  
   - Space: O(n) where n is validators (validator storage, message logs).

8. **Strengths**  
- Finality: provides fast finality.
- Throughput: high transaction throughput.
- Security: Byzantine fault tolerant.

9. **Weaknesses / limitations**  
- Scalability: O(n²) message complexity limits scalability.
- Primary: requires trusted primary (view-change handles failures).
- Network: requires reliable network.

10. **Compare with alternatives**  
    Alternatives: Proof of Work, Proof of Stake, Other BFT, HotStuff

11. **30-second explanation (your own words)**  
    Implements PBFT consensus algorithm, a Byzantine fault-tolerant consensus protocol that tolerates up to (n-1)/3 Byzantine failures in a network of n nodes, providing fast finality and high throughput.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
