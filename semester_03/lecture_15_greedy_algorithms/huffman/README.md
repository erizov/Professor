# Huffman Coding

1. **Name of Algorithm**  
   Huffman Coding

2. **What problem does it solve? (1 sentence)**  
   Constructs an optimal prefix-free binary code for compressing data by assigning shorter codes to more frequent symbols.

3. **Intuition (plain-language explanation)**  
   Build a binary tree bottom-up: merge two least frequent symbols into a node, repeat until one tree remains; left edges=0, right edges=1.

4. **Inputs & Outputs**  
   - Input: Symbols with their frequencies (or probabilities).  
   - Output: Huffman tree and variable-length binary codes for each symbol.

5. **Step-by-step description (5–10 lines max)**  
1. Create a leaf node for each symbol with its frequency.
2. Insert all nodes into a min-priority queue (by frequency).
3. While queue has >1 node: extract two nodes with lowest frequencies, create internal node with sum frequency, insert back into queue.
4. Remaining node is root of Huffman tree.
5. Traverse tree to assign codes: left=0, right=1.

6. **Tiny example (hand-simulated)**  
   Symbols: A(5), B(2), C(1), D(1). Merge C+D(2), then B+(C+D)(4), then A+(B+C+D)(9). Codes: A=0, B=10, C=110, D=111. Average bits: (5×1+2×2+1×3+1×3)/9 ≈ 1.67.

7. **Time & Space Complexity**  
   - Time: O(n log n) where n is number of symbols (priority queue operations).  
   - Space: O(n) for tree and code table.

8. **Strengths**  
- Optimal prefix-free code (minimizes expected code length).
- Widely used in compression (ZIP, JPEG, MP3).

9. **Weaknesses / limitations**  
- Requires frequency table (two-pass encoding).
- Not adaptive (fixed codes for entire message).

10. **Compare with alternatives**  
    Alternatives: Arithmetic Coding, Lempel-Ziv (LZ77/LZ78), Run-Length Encoding

11. **30-second explanation (your own words)**  
    Builds a binary tree by repeatedly merging least frequent symbols, ensuring frequent symbols get short codes and minimizing total encoded length.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
