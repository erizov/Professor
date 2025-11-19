# Mixture of Experts (MoE)

1. **Name of Algorithm**  
   Mixture of Experts (MoE)

2. **What problem does it solve? (1 sentence)**  
   Scales model capacity by using multiple expert networks where only a subset of experts are activated for each input, enabling very large models with manageable computational cost.

3. **Intuition (plain-language explanation)**  
   Like a team of specialists: Mixture of Experts is like having a team of specialists where each expert handles different types of problems - when a question comes in, a router (gating network) decides which 1-2 experts are best suited (like routing a medical question to a doctor, not a lawyer) - only those experts process the input, so you get the benefit of many specialists (large model capacity) without the cost of consulting all of them (computational efficiency).

4. **Inputs & Outputs**  
   - Input: Input tokens, expert networks, gating/router network, number of active experts, expert capacity.  
   - Output: Expert-selected outputs, routed computations, scaled model capacity, efficient processing.

5. **Step-by-step description (5–10 lines max)**  
1. Create experts: create multiple expert networks (feedforward layers).
2. Create router: create gating network that routes inputs to experts.
3. Route: router determines which experts to activate for each token.
4. Select: select top-k experts (typically 1-2) for each token.
5. Process: each selected expert processes the token independently.
6. Combine: combine outputs from selected experts (weighted sum or concatenation).
7. Load balance: ensure experts are used evenly (load balancing loss).
8. Train: train experts and router jointly.
9. Scale: scale model by adding more experts without proportional compute increase.
10. Optimize: optimize routing and expert utilization.

6. **Tiny example (hand-simulated)**  
   MoE: 8 experts, router selects top-2 → input token → router: scores experts → select: expert 3 (0.6), expert 7 (0.4) → process: both experts process token → combine: weighted sum (0.6·expert3 + 0.4·expert7) → output → capacity: 8 experts, compute: only 2 active → MoE scales efficiently.

7. **Time & Space Complexity**  
   - Time: O(e·d) where e is number of active experts (typically 1-2), d is expert dimension (much less than O(E·d) for all experts).  
   - Space: O(E·d) where E is total experts, d is expert size (all experts stored, but only few active).

8. **Strengths**  
- Scalability: enables very large models (trillions of parameters) with manageable compute.
- Efficiency: only activates subset of experts, reducing computation.
- Specialization: experts can specialize in different patterns or domains.

9. **Weaknesses / limitations**  
- Routing: routing decisions can be suboptimal.
- Load balancing: requires careful load balancing to use experts evenly.
- Complexity: more complex than dense models.

10. **Compare with alternatives**  
    Alternatives: Dense Models, Sparse Models, Conditional Computation, Switch Transformers

11. **30-second explanation (your own words)**  
    Scales model capacity by using multiple expert networks where only a subset of experts are activated for each input, enabling very large models with manageable computational cost.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
