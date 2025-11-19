# Confidential Transactions

1. **Name of Algorithm**  
   Confidential Transactions

2. **What problem does it solve? (1 sentence)**  
   Implements confidential transactions that hide transaction amounts while maintaining verifiability, enabling privacy-preserving blockchain transactions where amounts are encrypted but still verifiable.

3. **Intuition (plain-language explanation)**  
   Like private transactions: Confidential Transactions are like private transactions - you hide the amounts (like hiding prices) but still prove they're valid - just as you can have private but verifiable transactions, confidential transactions hide amounts but remain verifiable.

4. **Inputs & Outputs**  
   - Input: Transaction amounts, public keys, commitment schemes, range proofs, encryption keys.  
   - Output: Confidential transactions, encrypted amounts, verifiable commitments, range proofs, private transactions.

5. **Step-by-step description (5–10 lines max)**  
1. Commit: commit to transaction amount using commitment scheme.
2. Encrypt: encrypt amount information.
3. Prove: generate range proof (amount is valid).
4. Sign: sign transaction.
5. Broadcast: broadcast confidential transaction.
6. Verify: verify commitment and range proof.
7. Validate: validate transaction without seeing amount.
8. Record: record on blockchain.
9. Reveal: optionally reveal amount to authorized parties.
10. Audit: enable auditing if needed.

6. **Tiny example (hand-simulated)**  
   Confidential Transactions: amount: 10 BTC → commit: create commitment → encrypt: encrypt amount → prove: range proof (0 < amount < max) → verify: verify without seeing amount → result: private transaction verified → Confidential Transactions successful.

7. **Time & Space Complexity**  
   - Time: O(1) for transaction operations (constant time commitment and proof operations).  
   - Space: O(1) per transaction (commitment and proof storage).

8. **Strengths**  
- Privacy: hides transaction amounts.
- Verifiability: maintains transaction verifiability.
- Auditability: enables optional auditing.

9. **Weaknesses / limitations**  
- Overhead: adds overhead to transactions.
- Complexity: cryptographic operations are complex.
- Scalability: may impact scalability.

10. **Compare with alternatives**  
    Alternatives: Transparent Transactions, Full Anonymity, Selective Privacy, Other Privacy Methods

11. **30-second explanation (your own words)**  
    Implements confidential transactions that hide transaction amounts while maintaining verifiability, enabling privacy-preserving blockchain transactions where amounts are encrypted but still verifiable.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
