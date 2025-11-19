# Decentralized Storage

1. **Name of Algorithm**  
   Decentralized Storage

2. **What problem does it solve? (1 sentence)**  
   Stores data across distributed network of nodes instead of centralized servers, providing censorship-resistant, resilient, and cost-effective data storage.

3. **Intuition (plain-language explanation)**  
   Like a distributed filing cabinet: instead of storing files in one office (centralized server), files are split into pieces and stored across many offices (nodes) worldwide - even if some offices close, your files are still accessible from other offices, and no single office controls your data.

4. **Inputs & Outputs**  
   - Input: Data to store, storage network (IPFS, Arweave, Filecoin, etc.), redundancy parameters.  
   - Output: Content identifier (CID), distributed storage across nodes, retrieval capability.

5. **Step-by-step description (5–10 lines max)**  
1. Split data: divide data into chunks or pieces (for redundancy and distribution).
2. Encrypt (optional): encrypt data chunks for privacy.
3. Generate hash: compute content identifier (hash) for each chunk.
4. Distribute: upload chunks to multiple storage nodes across network.
5. Verify: verify chunks are stored correctly (proof of storage).
6. Store metadata: record chunk locations and content identifiers.
7. Retrieve: fetch chunks using content identifier when needed.
8. Reassemble: reconstruct original data from retrieved chunks.

6. **Tiny example (hand-simulated)**  
   Upload 1GB file → split into 100 chunks (10MB each) → hash each chunk → distribute to 50 nodes (2 copies each) → store metadata with content IDs → later, request file → retrieve chunks from nodes → verify hashes → reassemble → original file recovered.

7. **Time & Space Complexity**  
   - Time: O(n) to split/upload where n is data size, O(log n) to retrieve (distributed lookup).  
   - Space: O(n) for data storage, O(r·n) with redundancy factor r (multiple copies).

8. **Strengths**  
- Censorship resistance: no single entity can remove data.
- Resilience: data survives even if many nodes fail.
- Cost-effective: can be cheaper than centralized cloud storage.

9. **Weaknesses / limitations**  
- Retrieval speed: may be slower than centralized storage (depends on network).
- Incentive alignment: requires economic incentives for nodes to store data.
- Data availability: relies on nodes staying online and accessible.

10. **Compare with alternatives**  
    Alternatives: Centralized Cloud Storage, IPFS, Arweave, Filecoin, Storj

11. **30-second explanation (your own words)**  
    Stores data across distributed network of nodes instead of centralized servers, providing censorship-resistant, resilient, and cost-effective data storage.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
