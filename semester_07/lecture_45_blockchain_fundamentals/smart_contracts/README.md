# Smart Contracts

1. **Name of Algorithm**  
   Smart Contracts

2. **What problem does it solve? (1 sentence)**  
   Executes programmable code automatically on blockchain when conditions are met, enabling trustless automation of agreements and decentralized applications without intermediaries.

3. **Intuition (plain-language explanation)**  
   Like a vending machine: you put in money (send transaction) and select a product (call function) - the machine automatically gives you the product (executes code) without needing a cashier. Smart contracts are like vending machines on blockchain: code that automatically executes when conditions are met, with no one able to stop or change it once deployed.

4. **Inputs & Outputs**  
   - Input: Contract code, function calls, transaction data, blockchain state, gas (execution fee).  
   - Output: Contract execution results, state changes, events, transaction receipts.

5. **Step-by-step description (5–10 lines max)**  
1. Deploy contract: developer writes and deploys smart contract code to blockchain.
2. Store code: contract bytecode stored on blockchain (immutable once deployed).
3. Call function: user sends transaction calling contract function with parameters.
4. Validate: network validates transaction (signature, gas, permissions).
5. Execute: blockchain node executes contract code in virtual machine (EVM, etc.).
6. Update state: contract execution modifies blockchain state (balances, variables, etc.).
7. Emit events: contract can emit events for off-chain monitoring.
8. Return result: execution result returned, transaction recorded on blockchain.
9. Pay gas: user pays gas fees for computation (prevents infinite loops).

6. **Tiny example (hand-simulated)**  
   Deploy 'Token' contract → user calls transfer(recipient, amount) → contract checks sender balance → if sufficient, deducts from sender, adds to recipient → emits Transfer event → transaction recorded → balance updated on blockchain → no intermediary needed.

7. **Time & Space Complexity**  
   - Time: O(1) per operation typically, but depends on contract complexity (gas limits prevent infinite loops).  
   - Space: O(1) per contract variable, O(n) for arrays/mappings where n is data size.

8. **Strengths**  
- Trustless: code executes automatically without trusted third party.
- Transparent: contract code and execution visible to all.
- Immutable: once deployed, contract cannot be changed (unless designed to be upgradeable).

9. **Weaknesses / limitations**  
- Irreversible: bugs cannot be fixed easily (code is immutable).
- Gas costs: execution requires payment (can be expensive for complex operations).
- Limited expressiveness: constrained by blockchain's computational model.

10. **Compare with alternatives**  
    Alternatives: Traditional Contracts, Centralized Automation, Off-chain Oracles, Layer 2 Solutions

11. **30-second explanation (your own words)**  
    Executes programmable code automatically on blockchain when conditions are met, enabling trustless automation of agreements and decentralized applications without intermediaries.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
