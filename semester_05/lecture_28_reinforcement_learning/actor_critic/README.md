# Actor-Critic

1. **Name of Algorithm**  
   Actor-Critic

2. **What problem does it solve? (1 sentence)**  
   Combines policy-based (actor) and value-based (critic) reinforcement learning to learn both the policy and value function simultaneously for stable, sample-efficient learning.

3. **Intuition (plain-language explanation)**  
   Like a coach and a player: the actor decides what action to take, while the critic evaluates how good that action was, guiding the actor to improve.

4. **Inputs & Outputs**  
   - Input: State observations, policy network parameters (actor), value network parameters (critic), reward signal, discount factor γ.  
   - Output: Updated policy parameters for the actor and value estimates for the critic; learned policy that maps states to action probabilities.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize actor (policy πθ) and critic (value Vw) networks.
2. For each timestep: observe state s, sample action a ~ πθ(a|s).
3. Execute action, receive reward r and next state s′.
4. Critic computes TD error δ = r + γVw(s′) − Vw(s).
5. Update critic parameters via gradient descent to minimize δ².
6. Update actor parameters via policy gradient: θ ← θ + αδ∇θ log πθ(a|s).
7. Repeat across episodes; optionally use advantage estimates or entropy regularization.

6. **Tiny example (hand-simulated)**  
   CartPole: actor outputs probability of moving left/right; critic estimates expected return. Critic TD-error guides actor to choose actions that keep pole balanced longer.

7. **Time & Space Complexity**  
   - Time: Per step O(f_actor + f_critic) forward/backward passes; training cost scales with episodes × steps.  
   - Space: O(|θ| + |w|) for actor and critic parameters plus replay buffers if used.

8. **Strengths**  
- Lower variance than pure policy gradients due to critic baseline.
- Handles continuous action spaces with appropriate actor parameterization.

9. **Weaknesses / limitations**  
- Critic bias can destabilize learning if value estimates are poor.
- Two networks increase complexity and tuning effort.

10. **Compare with alternatives**  
    Alternatives: REINFORCE (policy gradient), Q-Learning/DQN, PPO/A3C

11. **30-second explanation (your own words)**  
    Trains an actor to choose actions and a critic to evaluate them, using TD errors to provide low-variance gradient estimates that improve the policy.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
