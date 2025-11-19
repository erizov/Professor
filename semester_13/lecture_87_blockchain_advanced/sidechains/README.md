# Sidechains

1. **Name of Algorithm**  
   Sidechains

2. **What problem does it solve? (1 sentence)**  
   Enables blockchain interoperability and scaling by creating separate blockchains (sidechains) that are pegged to the main chain, allowing assets and data to move between chains.

3. **Intuition (plain-language explanation)**  
   Like connected islands: Sidechains are like islands connected by bridges to the mainland (main chain) - you can move between islands (sidechains) and the mainland, each island can have different rules (consensus, features), but they're all connected - this allows experimentation and scaling while maintaining connection to the main chain.

4. **Inputs & Outputs**  
   - Input: Assets to transfer, sidechain configuration, peg mechanism, validators, consensus parameters.  
   - Output: Sidechain blocks, pegged assets, cross-chain transfers, sidechain state.

5. **Step-by-step description (5–10 lines max)**  
1. Create: create sidechain with its own consensus and rules.
2. Peg: establish two-way peg with main chain.
3. Lock: lock assets on main chain.
4. Transfer: transfer assets to sidechain.
5. Process: process transactions on sidechain.
6. Unlock: unlock assets on main chain when transferring back.
7. Validate: validate peg operations and transfers.
8. Monitor: monitor sidechain security and liveness.
9. Settle: settle cross-chain transactions.
10. Maintain: maintain peg security and sidechain operations.

6. **Tiny example (hand-simulated)**  
   Sidechain: create sidechain → establish peg → lock 10 ETH on main chain → transfer 10 ETH to sidechain → process tx on sidechain → transfer back → unlock on main chain → Sidechain successful.

7. **Time & Space Complexity**  
   - Time: O(t + p) where t is transaction time, p is peg operation time (sidechain operations).  
   - Space: O(s + m) where s is sidechain state, m is main chain state (sidechain storage).

8. **Strengths**  
- Flexibility: allows experimentation with different consensus and features.
- Interoperability: enables asset and data transfer between chains.
- Scalability: offloads transactions from main chain.

9. **Weaknesses / limitations**  
- Security: sidechain security is independent (weaker than main chain).
- Peg: two-way peg can be complex and risky.
- Trust: may require trusted validators for peg.

10. **Compare with alternatives**  
    Alternatives: Rollups, Plasma, State Channels, Sharding

11. **30-second explanation (your own words)**  
    Separate blockchains that are pegged to the main chain, enabling asset transfer and interoperability while allowing different consensus mechanisms and features.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
