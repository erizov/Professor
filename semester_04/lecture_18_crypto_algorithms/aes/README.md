# Advanced Encryption Standard (AES)

1. **Name of Algorithm**  
   Advanced Encryption Standard (AES)

2. **What problem does it solve? (1 sentence)**  
   Provides fast, secure symmetric-key encryption for protecting data at rest and in transit across modern systems.

3. **Intuition (plain-language explanation)**  
   Encrypt data by repeatedly applying substitution and permutation rounds that mix bytes and columns so ciphertext appears random without the key.

4. **Inputs & Outputs**  
   - Input: Plaintext block (128 bits), secret key (128/192/256 bits), mode of operation (CBC, GCM, CTR), optional IV/nonce.  
   - Output: Ciphertext block (128 bits) or full encrypted message with authentication tag for AEAD modes.

5. **Step-by-step description (5–10 lines max)**  
1. Expand secret key into round keys via key schedule.
2. Initial AddRoundKey: XOR plaintext with first round key.
3. For Nr-1 rounds: SubBytes, ShiftRows, MixColumns, AddRoundKey.
4. Final round omits MixColumns.
5. For modes like CBC/GCM, combine block cipher with chaining/nonce logic.
6. Decrypt by applying inverse operations with round keys in reverse.

6. **Tiny example (hand-simulated)**  
   AES-256-GCM encrypting API payload: generate random 96-bit nonce, encrypt plaintext with key, produce ciphertext and 128-bit auth tag stored alongside nonce.

7. **Time & Space Complexity**  
   - Time: O(N · Nr) where N is number of 128-bit blocks and Nr is 10/12/14 rounds depending on key size.  
   - Space: O(1) beyond key schedule (≈240 bytes for AES-256).

8. **Strengths**  
- NIST-standardized, hardware accelerated (AES-NI).
- Supports authenticated encryption (GCM, CCM).

9. **Weaknesses / limitations**  
- Symmetric key distribution required.
- Implementation must protect against side-channel leaks.

10. **Compare with alternatives**  
    Alternatives: ChaCha20-Poly1305, Camellia, Twofish

11. **30-second explanation (your own words)**  
    Uses repeated substitution-permutation rounds keyed by a shared secret to scramble data into ciphertext resistant to cryptanalysis.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
