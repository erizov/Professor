# Policy Gradient (REINFORCE)

1. **Name of Algorithm**  
   Policy Gradient (REINFORCE)

2. **What problem does it solve? (1 sentence)**  
   Directly optimizes stochastic policies by ascending the gradient of expected return, avoiding value-function approximation and enabling continuous action spaces.

3. **Intuition (plain-language explanation)**  
Treat policy parameters like weights that determine action probabilities; adjust them to increase the likelihood of actions that yielded high rewards.

4. **Inputs & Outputs**  
   - Input: Policy πθ(a|s), trajectories of states/actions/rewards, discount factor γ, baseline (optional).  
   - Output: Updated policy parameters θ that increase expected cumulative reward.

5. **Step-by-step description (5–10 lines max)**  
1. Roll out policy to collect trajectories (s₀,a₀,r₀,…,s_T).
2. Compute returns G_t = Σ_k γ^k r_{t+k}.
3. Estimate gradient: ∇θ J(θ) ≈ Σ_t ∇θ log πθ(a_t|s_t) (G_t − b_t) where b_t is baseline (often V(s_t)).
4. Update parameters θ ← θ + α ∇θ J(θ).
5. Repeat sampling and updating; optionally use variance reduction (baselines, advantage functions).
6. Use entropy regularization to encourage exploration.

6. **Tiny example (hand-simulated)**  
   MountainCarContinuous: policy outputs mean/variance of Gaussian torque; REINFORCE adjusts parameters so successful climbs become more probable.

7. **Time & Space Complexity**  
   - Time: O(T·f) per trajectory where T is steps and f is policy forward/backward cost; requires many trajectories for low-variance estimates.  
   - Space: O(|θ|) for policy parameters plus storage of trajectory data during updates.

8. **Strengths**  
- Works with continuous actions and stochastic policies.
- Optimizes policy directly without requiring value function.

9. **Weaknesses / limitations**  
- High variance gradient estimates lead to slow convergence.
- Requires on-policy data; trajectories cannot be reused extensively.

10. **Compare with alternatives**  
    Alternatives: Actor-Critic, PPO, Trust Region Policy Optimization (TRPO)

11. **30-second explanation (your own words)**  
    Uses the gradient of log policy probabilities weighted by returns to directly improve the policy, making rewarding actions more likely in future rollouts.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
