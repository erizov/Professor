# Proximal Policy Optimization (PPO)

1. **Name of Algorithm**  
   Proximal Policy Optimization (PPO)

2. **What problem does it solve? (1 sentence)**  
   Stabilizes policy gradient updates by constraining policy changes, providing reliable performance improvements without complex second-order optimization.

3. **Intuition (plain-language explanation)**  
   Like taking cautious steps: update the policy but clip the change so it never moves too far from the previous policy, preventing destructive updates.

4. **Inputs & Outputs**  
   - Input: Policy πθ, old policy πθ_old, advantage estimates Â, clipping parameter ε, value function approximator.  
   - Output: Updated policy parameters that maximize clipped surrogate objective while maintaining trust region.

5. **Step-by-step description (5–10 lines max)**  
1. Collect trajectories using current policy; compute advantages (e.g., GAE).
2. Compute probability ratio r_t(θ) = πθ(a_t|s_t) / πθ_old(a_t|s_t).
3. Optimize clipped objective: L^CLIP = E[min(r_tÂ_t, clip(r_t,1−ε,1+ε)Â_t)].
4. Add value function loss and entropy bonus to total loss.
5. Perform multiple epochs of mini-batch SGD on collected data.
6. Update old policy parameters to current policy and repeat rollout.

6. **Tiny example (hand-simulated)**  
   MuJoCo Humanoid: PPO with ε=0.2 and GAE learns stable locomotion policies by preventing large destructive updates seen in vanilla policy gradients.

7. **Time & Space Complexity**  
   - Time: O(K·B·f) per iteration where K is epochs, B batch size, f network cost; more sample efficient than REINFORCE but still on-policy.  
   - Space: O(|θ| + buffer) for policy parameters and rollout storage.

8. **Strengths**  
- Stable training with simple clipping objective.
- Works well on continuous control benchmarks.

9. **Weaknesses / limitations**  
- Still on-policy; requires fresh samples each update.
- Performance sensitive to clipping parameter and advantage estimates.

10. **Compare with alternatives**  
    Alternatives: TRPO, Actor-Critic, SAC (off-policy)

11. **30-second explanation (your own words)**  
    Introduces a clipped surrogate objective that limits policy updates, ensuring new policies stay close to old ones while still improving performance.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
