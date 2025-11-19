# bcrypt Password Hashing

1. **Name of Algorithm**  
   bcrypt Password Hashing

2. **What problem does it solve? (1 sentence)**  
   Derives computationally expensive password hashes that resist brute-force and rainbow-table attacks for stored credentials.

3. **Intuition (plain-language explanation)**  
   Combine salt with password and run an intentionally slow, memory-hard key setup (EksBlowfish) so attackers must spend significant effort per guess.

4. **Inputs & Outputs**  
   - Input: Password string, cost factor (log2 rounds), 128-bit salt.  
   - Output: 60-character hash string containing version, cost, salt, and checksum.

5. **Step-by-step description (5–10 lines max)**  
1. Generate random salt for each password.
2. Run EksBlowfishSetup with password and salt cost times (2^cost iterations).
3. Encrypt fixed text "OrpheanBeholderScryDoubt" 64 times with derived state.
4. Format output $2b$<cost>$<22-char-salt><31-char-hash>.
5. Verification: repeat process with same salt/cost and compare hashes.

6. **Tiny example (hand-simulated)**  
   Cost=12: hashing password "Sup3rSecret!" takes ~300 ms; stored hash includes salt so each account uses unique work factor.

7. **Time & Space Complexity**  
   - Time: O(2^cost) per hash; raising cost doubles runtime.  
   - Space: O(1) (minimal memory aside from small Blowfish state).

8. **Strengths**  
- Salted and adaptive: increase cost as hardware improves.
- Widely implemented in language runtimes.

9. **Weaknesses / limitations**  
- Limited to passwords ≤72 bytes.
- Blowfish-based design lacks modern memory hardness (see Argon2).

10. **Compare with alternatives**  
    Alternatives: Argon2id, scrypt, PBKDF2

11. **30-second explanation (your own words)**  
    Applies an expensive Blowfish key schedule with per-user salt so each password check consumes significant CPU, deterring offline cracking.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
