# Proof of Stake (PoS)

1. **Name of Algorithm**  
   Proof of Stake (PoS)

2. **What problem does it solve? (1 sentence)**  
   Selects validators to create blocks based on amount of cryptocurrency staked, reducing energy consumption while maintaining network security through economic incentives.

3. **Intuition (plain-language explanation)**  
   Like a weighted lottery: instead of solving puzzles (expensive), validators 'stake' their coins as collateral - the more coins you stake, the higher your chance of being selected to validate blocks. If you validate incorrectly, you lose your stake (economic penalty), so validators are incentivized to be honest.

4. **Inputs & Outputs**  
   - Input: Staked cryptocurrency, validator selection algorithm, block candidate, validator's stake amount.  
   - Output: Validated block, validator rewards, updated stake balances.

5. **Step-by-step description (5–10 lines max)**  
1. Stake coins: validators lock cryptocurrency as stake (collateral).
2. Select validator: algorithm selects validator based on stake amount and randomness.
3. Propose block: selected validator creates and proposes new block.
4. Validate: other validators verify proposed block is valid.
5. Approve: validators vote to approve or reject block.
6. Finalize: if majority approve, block added to chain, validator earns reward.
7. Slash (if malicious): if validator acts maliciously, stake is slashed (penalty).
8. Update stake: adjust validator stakes based on rewards/penalties.

6. **Tiny example (hand-simulated)**  
   Validator stakes 1000 ETH → selected to validate block (probability proportional to stake) → proposes block → other validators verify → 2/3 approve → block finalized → validator earns 0.1 ETH reward → stake increases to 1000.1 ETH. If malicious: stake slashed, lose 100 ETH.

7. **Time & Space Complexity**  
   - Time: O(1) to select validator (deterministic/random selection), O(1) to validate block.  
   - Space: O(v) where v is number of validators (track stake amounts).

8. **Strengths**  
- Energy efficient: requires minimal computational resources (no mining).
- Fast: enables faster block times and higher throughput.
- Economic security: validators have financial stake in network security.

9. **Weaknesses / limitations**  
- Wealth concentration: those with more stake have more influence.
- Nothing at stake: validators might validate on multiple chains (addressed by slashing).
- Complexity: more complex validator selection and slashing mechanisms.

10. **Compare with alternatives**  
    Alternatives: Proof of Work, Delegated Proof of Stake, Proof of Authority, Hybrid PoW/PoS

11. **30-second explanation (your own words)**  
    Selects validators to create blocks based on amount of cryptocurrency staked, reducing energy consumption while maintaining network security through economic incentives.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
