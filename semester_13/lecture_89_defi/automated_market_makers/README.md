# Automated Market Makers (AMM)

1. **Name of Algorithm**  
   Automated Market Makers (AMM)

2. **What problem does it solve? (1 sentence)**  
   Implements Automated Market Makers, decentralized exchange protocols that use mathematical formulas (like constant product formula) to determine asset prices and enable trading without traditional order books.

3. **Intuition (plain-language explanation)**  
   Like automatic pricing: AMMs are like automatic pricing systems - instead of buyers and sellers matching orders (like traditional exchanges), a formula automatically sets prices based on supply and demand - just as automatic pricing adjusts prices, AMMs automatically price assets.

4. **Inputs & Outputs**  
   - Input: Liquidity pools, trading pairs, liquidity provider tokens, swap requests, AMM formulas.  
   - Output: Asset swaps, updated prices, liquidity pool balances, trading fees, LP tokens.

5. **Step-by-step description (5–10 lines max)**  
1. Provide: liquidity providers add assets to pools.
2. Calculate: calculate prices using AMM formula (x * y = k).
3. Swap: users swap assets through pools.
4. Update: update pool balances after swap.
5. Price: new price determined by new balances.
6. Fee: collect trading fees.
7. Distribute: distribute fees to liquidity providers.
8. Track: track LP token ownership.
9. Remove: allow liquidity removal.
10. Optimize: optimize for low slippage.

6. **Tiny example (hand-simulated)**  
   AMM: pool: ETH/USDC pool (100 ETH, 200,000 USDC) → swap: user swaps 10 ETH for USDC → calculate: new price from formula → update: pool now 110 ETH, 181,818 USDC → result: user receives 18,182 USDC → AMM successful.

7. **Time & Space Complexity**  
   - Time: O(1) for swap calculation (constant time formula evaluation).  
   - Space: O(p) where p is number of pools (pool storage).

8. **Strengths**  
- Decentralization: fully decentralized, no order books needed.
- Accessibility: easy to use, always available.
- Liquidity: incentivizes liquidity provision.

9. **Weaknesses / limitations**  
- Slippage: large trades cause price slippage.
- Impermanent loss: liquidity providers face impermanent loss.
- Formula: simple formulas may not capture all market dynamics.

10. **Compare with alternatives**  
    Alternatives: Order Books, Centralized Exchanges, Other AMM Formulas, Hybrid Approaches

11. **30-second explanation (your own words)**  
    Implements Automated Market Makers, decentralized exchange protocols that use mathematical formulas (like constant product formula) to determine asset prices and enable trading without traditional order books.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
