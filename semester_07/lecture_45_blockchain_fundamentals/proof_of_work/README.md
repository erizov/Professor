# Proof of Work (PoW)

1. **Name of Algorithm**  
   Proof of Work (PoW)

2. **What problem does it solve? (1 sentence)**  
   Requires miners to solve computationally expensive cryptographic puzzles to validate blocks, securing blockchain network by making attacks economically infeasible.

3. **Intuition (plain-language explanation)**  
   Like a lottery where you buy tickets by doing hard math: miners compete to solve a difficult puzzle (finding a number that makes block hash start with many zeros) - the first to solve gets to add the block and earn rewards. The difficulty ensures blocks are added at steady rate, and attacking requires enormous computational power (expensive).

4. **Inputs & Outputs**  
   - Input: Block candidate with transactions, previous block hash, difficulty target, nonce (variable to adjust).  
   - Output: Valid block with nonce meeting difficulty, block hash, mining reward.

5. **Step-by-step description (5–10 lines max)**  
1. Prepare block: create block with transactions, previous hash, timestamp.
2. Set difficulty: network adjusts target hash (number of leading zeros required).
3. Try nonce: start with nonce = 0, increment and recompute block hash.
4. Check hash: verify if hash meets difficulty target (hash < target).
5. Repeat: if hash doesn't meet target, increment nonce and try again.
6. Find solution: when hash meets target, nonce is valid proof of work.
7. Broadcast: miner broadcasts block with valid nonce to network.
8. Verify: other nodes verify hash meets difficulty (quick verification).
9. Accept: if valid, network accepts block, miner receives reward.

6. **Tiny example (hand-simulated)**  
   Block with transactions → hash with nonce=0: 7a3f9... (doesn't meet target) → nonce=1: 9b2e1... → ... → nonce=1234567: 0000a3f9... (meets target, 4 leading zeros) → broadcast block → network verifies → block accepted → miner earns Bitcoin reward.

7. **Time & Space Complexity**  
   - Time: O(2^d) expected attempts where d is difficulty (exponential in difficulty), O(1) to verify.  
   - Space: O(1) per mining attempt (constant space for hash computation).

8. **Strengths**  
- Security: requires enormous computational power to attack (51% attack expensive).
- Proven: Bitcoin's security model proven over 15+ years.
- Decentralization: anyone with hardware can participate in mining.

9. **Weaknesses / limitations**  
- Energy consumption: extremely energy-intensive (Bitcoin uses more energy than some countries).
- Slow: block time typically 10+ minutes (Bitcoin), limiting throughput.
- Hardware arms race: favors those with specialized mining hardware (ASICs).

10. **Compare with alternatives**  
    Alternatives: Proof of Stake, Proof of Authority, Delegated Proof of Stake, Proof of Space

11. **30-second explanation (your own words)**  
    Requires miners to solve computationally expensive cryptographic puzzles to validate blocks, securing blockchain network by making attacks economically infeasible.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
