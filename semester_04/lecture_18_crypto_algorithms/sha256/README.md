# SHA-256 Hash Function

1. **Name of Algorithm**  
   SHA-256 Hash Function

2. **What problem does it solve? (1 sentence)**  
   Computes fixed-length digests for arbitrary data, enabling integrity checks, digital signatures, and proof-of-work schemes.

3. **Intuition (plain-language explanation)**  
   Process data in 512-bit chunks through nonlinear bit-wise operations (Ch, Maj, Σ) so small input changes avalanche into unrelated 256-bit outputs.

4. **Inputs & Outputs**  
   - Input: Message of arbitrary length, processed as 512-bit blocks after padding.  
   - Output: 256-bit (32-byte) hash value.

5. **Step-by-step description (5–10 lines max)**  
1. Pad message with 1-bit, zeros, and 64-bit length to multiple of 512 bits.
2. Initialize 8 working variables with SHA-256 constants.
3. For each block: extend 16 words to 64 via schedule; iterate 64 rounds mixing message schedule with constants.
4. Update hash state by adding working variables modulo 2^32.
5. Concatenate final 8 words to produce 256-bit digest.

6. **Tiny example (hand-simulated)**  
   "hello" → SHA-256 = 2cf24d...; widely used to verify file downloads and Bitcoin block headers.

7. **Time & Space Complexity**  
   - Time: O(n) where n is number of 512-bit blocks.  
   - Space: O(1) (small state of 8×32-bit words plus schedule).

8. **Strengths**  
- Collision resistant (no known practical attacks).
- Deterministic with uniform output distribution.

9. **Weaknesses / limitations**  
- Not suitable for password storage (too fast).
- Vulnerable to length-extension attacks without proper construction.

10. **Compare with alternatives**  
    Alternatives: SHA-3, BLAKE3, SHA-512/256

11. **30-second explanation (your own words)**  
    Iterative compression function that mixes message words with constants and bitwise operations to produce a 256-bit digest resistant to preimage/collision attacks.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
