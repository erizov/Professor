# RSA Public-Key Cryptography

1. **Name of Algorithm**  
   RSA Public-Key Cryptography

2. **What problem does it solve? (1 sentence)**  
   Enables secure key exchange, encryption, and digital signatures using asymmetric key pairs derived from large primes.

3. **Intuition (plain-language explanation)**  
   Multiplying large primes is easy but factoring their product is hard; leverage modular exponentiation with public/private exponents for encryption/signing.

4. **Inputs & Outputs**  
   - Input: Public modulus n=p·q, public exponent e, private exponent d, message m (properly padded).  
   - Output: Ciphertext c = m^e mod n for encryption; signature s = m^d mod n for signing.

5. **Step-by-step description (5–10 lines max)**  
1. Key generation: choose random primes p,q; compute n=p·q and φ(n).
2. Select public exponent e (commonly 65537) coprime to φ(n).
3. Compute private exponent d ≡ e^{-1} mod φ(n).
4. Encryption: apply modular exponentiation with e; decryption uses d.
5. Always wrap messages with padding (OAEP for encryption, PSS for signatures).
6. Validate signatures by raising s^e mod n and comparing to hashed message.

6. **Tiny example (hand-simulated)**  
   TLS handshake: client verifies server certificate by checking RSA-PSS signature signed with CA's private key.

7. **Time & Space Complexity**  
   - Time: Modular exponentiation O(log e · log^2 n) using square-and-multiply; key generation involves probabilistic primality tests.  
   - Space: O(|n|) to store modulus and exponents (2048+ bits).

8. **Strengths**  
- Mature ecosystem and interoperability.
- Enables asymmetric trust models (certificates).

9. **Weaknesses / limitations**  
- Slow compared to symmetric crypto; large key sizes.
- Padding/oracle attacks if implemented incorrectly.

10. **Compare with alternatives**  
    Alternatives: Elliptic Curve Cryptography (ECDSA/ECDH), Diffie-Hellman, Ed25519

11. **30-second explanation (your own words)**  
    Relies on the hardness of factoring a large composite number, using paired exponents for encryption/decryption or signing/verification.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
