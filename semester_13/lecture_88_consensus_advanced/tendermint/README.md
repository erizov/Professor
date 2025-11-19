# Tendermint

1. **Name of Algorithm**  
   Tendermint

2. **What problem does it solve? (1 sentence)**  
   Implements Tendermint consensus algorithm, a Byzantine fault-tolerant consensus protocol designed for blockchains, providing fast finality and high throughput with a focus on application-agnostic consensus.

3. **Intuition (plain-language explanation)**  
   Like efficient agreement: Tendermint is like efficient agreement protocols - validators agree on blocks efficiently through voting rounds - just as efficient voting reaches decisions, Tendermint reaches consensus efficiently.

4. **Inputs & Outputs**  
   - Input: Transactions, validators, voting power, consensus parameters, Byzantine fault tolerance.  
   - Output: Consensus decisions, finalized blocks, fast finality, high throughput, secure blockchain.

5. **Step-by-step description (5–10 lines max)**  
1. Propose: proposer (selected by voting power) proposes block.
2. Pre-vote: validators pre-vote on proposal.
3. Pre-commit: validators pre-commit after 2/3 pre-votes.
4. Commit: commit block after 2/3 pre-commits.
5. Finalize: finalize committed block.
6. Broadcast: broadcast finalized block.
7. Verify: verify block validity.
8. Update: update blockchain state.
9. Rotate: rotate proposer.
10. Repeat: repeat for next block.

6. **Tiny example (hand-simulated)**  
   Tendermint: validators: 100 validators → propose: proposer proposes block → pre-vote: 67 validators pre-vote → pre-commit: 67 validators pre-commit → commit: block committed in <1 second → result: fast, secure consensus → Tendermint successful.

7. **Time & Space Complexity**  
   - Time: O(n) where n is validators (linear communication complexity).  
   - Space: O(n + b) where n is validators, b is block size (validator and block storage).

8. **Strengths**  
- Finality: provides instant finality (no forks).
- Throughput: high transaction throughput.
- Application-agnostic: works with any application logic.

9. **Weaknesses / limitations**  
- Validator set: requires known validator set.
- Voting power: voting power distribution affects security.
- Complexity: consensus protocol is complex.

10. **Compare with alternatives**  
    Alternatives: Proof of Work, Proof of Stake, PBFT, Other BFT

11. **30-second explanation (your own words)**  
    Implements Tendermint consensus algorithm, a Byzantine fault-tolerant consensus protocol designed for blockchains, providing fast finality and high throughput with a focus on application-agnostic consensus.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
