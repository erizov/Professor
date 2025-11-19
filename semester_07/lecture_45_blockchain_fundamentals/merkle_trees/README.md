# Merkle Trees

1. **Name of Algorithm**  
   Merkle Trees

2. **What problem does it solve? (1 sentence)**  
Efficiently verifies data integrity and enables efficient proofs that specific transactions are included in a block without downloading entire block, reducing storage and bandwidth requirements.

3. **Intuition (plain-language explanation)**  
   Like a family tree for data: transactions are leaves, pairs are hashed together to form parents, parents are hashed to form grandparents, until you get one root hash - to prove a transaction exists, you only need the root and a few 'sibling' hashes along the path (Merkle proof), not all transactions.

4. **Inputs & Outputs**  
   - Input: List of transactions or data items, hash function (typically SHA-256).  
   - Output: Merkle root hash, Merkle tree structure, Merkle proofs for individual items.

5. **Step-by-step description (5–10 lines max)**  
1. Hash leaves: compute hash of each transaction/data item (leaf nodes).
2. Pair and hash: pair adjacent leaf hashes and hash them together (parent nodes).
3. Repeat: continue pairing and hashing until single root hash remains.
4. Store root: store Merkle root in block header (represents all transactions).
5. Generate proof: to prove transaction included, provide path from leaf to root (sibling hashes).
6. Verify proof: recipient verifies proof by recomputing hashes up to root.
7. Compare: verify computed root matches block header root.

6. **Tiny example (hand-simulated)**  
   4 transactions: T1, T2, T3, T4 → hash: H1, H2, H3, H4 → pair: H(H1||H2), H(H3||H4) → pair again: H(H(H1||H2)||H(H3||H4)) = Merkle root → to prove T1 included: provide H2, H(H3||H4), verify: H(H(H1||H2)||H(H3||H4)) = root.

7. **Time & Space Complexity**  
   - Time: O(n) to build tree, O(log n) to generate/verify proof where n is number of transactions.  
   - Space: O(n) to store tree, O(log n) for Merkle proof (only path needed, not full tree).

8. **Strengths**  
- Efficient verification: O(log n) proof size vs O(n) for full block.
- Data integrity: any change in transaction changes root hash.
- Scalability: enables light clients (SPV) without full blockchain download.

9. **Weaknesses / limitations**  
- Tree structure: requires organizing data into tree (overhead for small datasets).
- Hash collisions: theoretically possible but practically infeasible with good hash functions.
- Rebuilding: modifying tree requires recomputing affected branches.

10. **Compare with alternatives**  
    Alternatives: Full Block Verification, Hash Lists, Merkle Patricia Trees, Verkle Trees

11. **30-second explanation (your own words)**  
Efficiently verifies data integrity and enables efficient proofs that specific transactions are included in a block without downloading entire block, reducing storage and bandwidth requirements.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
