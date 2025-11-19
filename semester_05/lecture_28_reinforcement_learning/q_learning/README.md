# Q-Learning

1. **Name of Algorithm**  
   Q-Learning

2. **What problem does it solve? (1 sentence)**  
   Off-policy TD control algorithm that learns optimal action-value function for Markov Decision Processes with discrete states/actions.

3. **Intuition (plain-language explanation)**  
   Update your estimate of action usefulness by bootstrapping: new Q-value = old Q-value plus learning rate times error between received reward + best future estimate and current estimate.

4. **Inputs & Outputs**  
   - Input: Discrete state/action space, learning rate α, discount factor γ, exploration policy (e.g., ε-greedy).  
   - Output: Q-table Q(s,a) with estimated expected returns; derived greedy policy π(s) = argmax_a Q(s,a).

5. **Step-by-step description (5–10 lines max)**  
1. Initialize Q(s,a) arbitrarily.
2. For each episode: start at initial state.
3. Choose action a using ε-greedy policy w.r.t Q.
4. Observe reward r and next state s′.
5. Update Q(s,a) ← Q(s,a) + α [r + γ max_{a′} Q(s′,a′) − Q(s,a)].
6. Set s ← s′ and repeat until terminal state.
7. Gradually decay ε to shift toward exploitation.

6. **Tiny example (hand-simulated)**  
   Gridworld: agent updates Q-values for moving north/south/east/west; eventually learns optimal path to goal while avoiding traps.

7. **Time & Space Complexity**  
   - Time: O(E·A) where E is number of state transitions and A is action count per update (max over actions).  
   - Space: O(|S|·|A|) for Q-table (scales poorly in large/continuous spaces).

8. **Strengths**  
- Converges to optimal policy under standard assumptions.
- Simple to implement; off-policy allows reuse of experience.

9. **Weaknesses / limitations**  
- Not directly applicable to large/continuous state spaces (requires function approximation).
- Requires sufficient exploration to converge.

10. **Compare with alternatives**  
    Alternatives: SARSA, DQN (function approximation), Policy Gradient

11. **30-second explanation (your own words)**  
    Iteratively updates action-value estimates using Bellman optimality equation, enabling agents to learn optimal policies through exploration and bootstrapping.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
