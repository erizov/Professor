# Cryptocurrency Wallets

1. **Name of Algorithm**  
   Cryptocurrency Wallets

2. **What problem does it solve? (1 sentence)**  
   Manages cryptographic keys and enables users to send, receive, and store cryptocurrencies securely, providing interface between users and blockchain networks.

3. **Intuition (plain-language explanation)**  
   Like a digital wallet: instead of holding physical cash and cards, a crypto wallet holds your private keys (like passwords) that prove you own your cryptocurrency - the wallet lets you check your balance, send coins, and receive coins, just like a physical wallet but for digital money.

4. **Inputs & Outputs**  
   - Input: Private keys (or seed phrase), blockchain network, transaction requests, recipient addresses.  
   - Output: Signed transactions, wallet balance, transaction history, public addresses.

5. **Step-by-step description (5–10 lines max)**  
1. Generate keys: create public-private key pair (or derive from seed phrase).
2. Store securely: encrypt and store private keys (hardware, software, or paper wallet).
3. Derive addresses: generate receiving addresses from public key.
4. Check balance: query blockchain for address balance and transaction history.
5. Create transaction: construct transaction with recipient, amount, fees.
6. Sign transaction: sign transaction with private key (proves ownership).
7. Broadcast: send signed transaction to blockchain network.
8. Monitor: track transaction status until confirmed on blockchain.

6. **Tiny example (hand-simulated)**  
   User opens wallet app → wallet generates key pair from seed phrase → displays address (0x123...) → user receives 1 ETH → wallet queries blockchain → shows balance: 1 ETH → user sends 0.5 ETH to friend → wallet signs transaction → broadcasts → transaction confirmed → balance: 0.5 ETH.

7. **Time & Space Complexity**  
   - Time: O(1) for key operations, O(1) for transaction creation, O(block_time) for confirmation.  
   - Space: O(1) for key storage (constant size keys), O(n) for transaction history where n is number of transactions.

8. **Strengths**  
- Security: private keys enable secure ownership and transactions.
- Control: users have full control over their funds (no bank needed).
- Portability: wallets can be used across devices and platforms.

9. **Weaknesses / limitations**  
- Key management: losing private keys means losing funds permanently.
- User experience: managing keys can be complex for non-technical users.
- Security risks: wallets can be compromised if keys are exposed.

10. **Compare with alternatives**  
    Alternatives: Hardware Wallets, Software Wallets, Paper Wallets, Custodial Wallets, Multi-signature Wallets

11. **30-second explanation (your own words)**  

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
