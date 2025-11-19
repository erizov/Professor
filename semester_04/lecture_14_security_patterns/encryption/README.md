# Encryption

1. **Name of Algorithm**  
   Encryption

2. **What problem does it solve? (1 sentence)**  
   Transforms readable data (plaintext) into unreadable form (ciphertext) to protect confidentiality, ensuring only authorized parties can decrypt.

3. **Intuition (plain-language explanation)**  
   Like a secret code: scramble data using a key so only those with the key can unscramble and read it.

4. **Inputs & Outputs**  
   - Input: Plaintext data, encryption key, encryption algorithm (symmetric or asymmetric).  
   - Output: Ciphertext (encrypted data) and optionally initialization vector (IV) or nonce.

5. **Step-by-step description (5–10 lines max)**  
1. Select encryption algorithm (AES, RSA, ChaCha20, etc.).
2. Generate or use existing encryption key.
3. For symmetric: use same key for encryption/decryption.
4. For asymmetric: use public key to encrypt, private key to decrypt.
5. Apply encryption algorithm to produce ciphertext.
6. Store/transmit ciphertext; decrypt with corresponding key when needed.

6. **Tiny example (hand-simulated)**  
   Encrypt 'Hello' with AES-256: plaintext → ciphertext 'a3f9b2c1...' using key. Decrypt with same key → 'Hello'.

7. **Time & Space Complexity**  
   - Time: Symmetric: O(n) for n bytes; Asymmetric: O(n·k) where k is key size.  
   - Space: O(n) for ciphertext (similar to plaintext size, plus IV/nonce overhead).

8. **Strengths**  
- Protects data confidentiality at rest and in transit.
- Industry-standard algorithms (AES, RSA) are well-tested.

9. **Weaknesses / limitations**  
- Key management complexity (generation, storage, rotation).
- Performance overhead, especially for asymmetric encryption.

10. **Compare with alternatives**  
    Alternatives: Symmetric Encryption (AES), Asymmetric Encryption (RSA, ECC), Hybrid Encryption

11. **30-second explanation (your own words)**  
    Converts plaintext to ciphertext using cryptographic algorithms and keys, ensuring data remains confidential and can only be read by authorized parties with the decryption key.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
