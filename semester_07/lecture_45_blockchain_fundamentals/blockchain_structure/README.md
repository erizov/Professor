# Blockchain Structure

1. **Name of Algorithm**  
   Blockchain Structure

2. **What problem does it solve? (1 sentence)**  
   Organizes data into cryptographically linked blocks forming an immutable, distributed ledger, enabling trustless transactions and decentralized record-keeping without central authority.

3. **Intuition (plain-language explanation)**  
   Like a digital ledger book where each page (block) contains transactions, and each page references the previous page's fingerprint (hash) - if someone tries to change an old page, all subsequent pages become invalid, making tampering obvious. The ledger is copied across many computers, so no single authority controls it.

4. **Inputs & Outputs**  
   - Input: Transactions, previous block hash, timestamp, nonce (for mining), block data.  
   - Output: New block with transactions, block hash, link to previous block, updated blockchain.

5. **Step-by-step description (5–10 lines max)**  
1. Collect transactions: gather pending transactions into a block candidate.
2. Create block header: include previous block hash, Merkle root of transactions, timestamp, nonce.
3. Calculate hash: compute cryptographic hash of block header (SHA-256).
4. Mine block: find nonce that produces hash meeting difficulty target (proof of work).
5. Validate: verify all transactions in block are valid (signatures, balances, etc.).
6. Append block: add validated block to blockchain (link via previous hash).
7. Broadcast: distribute new block to all network participants.
8. Consensus: network agrees on longest valid chain (consensus mechanism).

6. **Tiny example (hand-simulated)**  
   Block 1: transactions [A→B: 10, C→D: 5] → hash: abc123 → Block 2: prev_hash=abc123, transactions [B→E: 3] → hash: def456 → Block 3: prev_hash=def456, transactions [E→F: 2] → chain: Block1→Block2→Block3 (immutable, tamper-evident).

7. **Time & Space Complexity**  
   - Time: O(1) to add block once mined, O(2^d) for mining where d is difficulty (exponential in difficulty).  
   - Space: O(n) where n is number of blocks (linear growth, each block stores transactions and metadata).

8. **Strengths**  
- Immutability: once added, blocks cannot be altered without invalidating chain.
- Decentralization: no single point of failure or control.
- Transparency: all transactions visible to network participants.

9. **Weaknesses / limitations**  
- Scalability: limited transaction throughput (e.g., Bitcoin ~7 TPS).
- Energy consumption: proof of work requires significant computational resources.
- Storage: full blockchain requires storing all historical transactions.

10. **Compare with alternatives**  
    Alternatives: Centralized Databases, Distributed Ledgers, Directed Acyclic Graphs (DAG), Hashgraph

11. **30-second explanation (your own words)**  
    Organizes data into cryptographically linked blocks forming an immutable, distributed ledger, enabling trustless transactions and decentralized record-keeping without central authority.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
