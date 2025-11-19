# Derivatives (DeFi)

1. **Name of Algorithm**  
   Derivatives (DeFi)

2. **What problem does it solve? (1 sentence)**  
   Implements decentralized derivatives protocols that enable trading of financial derivatives (futures, options, perpetuals) on blockchain without intermediaries, providing transparent and accessible derivative markets.

3. **Intuition (plain-language explanation)**  
   Like derivatives but decentralized: DeFi Derivatives are like traditional derivatives (futures, options) but on blockchain - you trade contracts (like betting on future prices) without brokers - just as traditional derivatives enable price speculation, DeFi derivatives enable decentralized speculation.

4. **Inputs & Outputs**  
   - Input: Derivative contracts, collateral, positions, prices, liquidation parameters, margin requirements.  
   - Output: Derivative positions, PnL, liquidations, settlements, margin calls, trading fees.

5. **Step-by-step description (5–10 lines max)**  
1. Create: create derivative contract (futures, options).
2. Deposit: deposit collateral.
3. Open: open derivative position.
4. Price: track underlying asset price (oracle).
5. Margin: monitor margin requirements.
6. Liquidate: liquidate if margin insufficient.
7. Settle: settle contract at expiration.
8. Payout: payout profits/losses.
9. Close: close position early if desired.
10. Manage: manage risk and positions.

6. **Tiny example (hand-simulated)**  
   Derivatives: contract: ETH perpetual futures → deposit: 1000 USDC collateral → open: long position 10 ETH → price: ETH price increases → result: profit, position value increases → Derivatives successful.

7. **Time & Space Complexity**  
   - Time: O(1) for position operations (constant time contract operations).  
   - Space: O(p + c) where p is positions, c is contracts (position and contract storage).

8. **Strengths**  
- Accessibility: accessible to anyone with crypto.
- Transparency: transparent and auditable.
- Innovation: enables new derivative products.

9. **Weaknesses / limitations**  
- Risk: high risk, potential for large losses.
- Liquidation: liquidation risk if price moves against position.
- Oracles: depends on reliable price oracles.

10. **Compare with alternatives**  
    Alternatives: Traditional Derivatives, Centralized Crypto Derivatives, No Derivatives, Hybrid Approaches

11. **30-second explanation (your own words)**  
    Implements decentralized derivatives protocols that enable trading of financial derivatives (futures, options, perpetuals) on blockchain without intermediaries, providing transparent and accessible derivative markets.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
