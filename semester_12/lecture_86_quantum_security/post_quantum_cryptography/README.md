# Post-Quantum Cryptography

1. **Name of Algorithm**  
   Post-Quantum Cryptography

2. **What problem does it solve? (1 sentence)**  
   Develops cryptographic algorithms that are secure against attacks from both classical and quantum computers, ensuring long-term security as quantum computers become available.

3. **Intuition (plain-language explanation)**  
   Like future-proof security: Post-Quantum Cryptography is like future-proof security - you use encryption that works even when quantum computers exist (which can break current encryption) - just as you prepare for future threats, post-quantum crypto prepares for quantum threats.

4. **Inputs & Outputs**  
   - Input: Classical data, post-quantum algorithms, key material, security parameters, implementation requirements.  
   - Output: Post-quantum secure encryption, quantum-resistant keys, secure communication, future-proof security.

5. **Step-by-step description (5–10 lines max)**  
1. Select: select post-quantum algorithm (lattice, code-based, etc.).
2. Generate: generate post-quantum keys.
3. Encrypt: encrypt data using post-quantum algorithm.
4. Sign: create post-quantum signatures.
5. Verify: verify post-quantum signatures.
6. Deploy: deploy in systems.
7. Migrate: migrate from classical crypto.
8. Validate: validate security properties.
9. Monitor: monitor for vulnerabilities.
10. Update: update as standards evolve.

6. **Tiny example (hand-simulated)**  
   Post-Quantum Cryptography: algorithm: CRYSTALS-Kyber → generate: post-quantum keys → encrypt: encrypt message → result: secure against quantum attacks → Post-Quantum Cryptography operational.

7. **Time & Space Complexity**  
   - Time: O(n) where n is data size (varies by algorithm, typically polynomial).  
   - Space: O(n) where n is key/data size (algorithm-dependent).

8. **Strengths**  
- Security: secure against quantum attacks.
- Future-proof: ensures long-term security.
- Standards: NIST standardized algorithms available.

9. **Weaknesses / limitations**  
- Performance: may be slower than classical crypto.
- Migration: requires migration from classical crypto.
- Maturity: field is still evolving.

10. **Compare with alternatives**  
    Alternatives: Classical Cryptography, Quantum Cryptography, Hybrid Approaches, Quantum Key Distribution

11. **30-second explanation (your own words)**  
    Develops cryptographic algorithms that are secure against attacks from both classical and quantum computers, ensuring long-term security as quantum computers become available.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
