# Deep Q-Network (DQN)

1. **Name of Algorithm**  
   Deep Q-Network (DQN)

2. **What problem does it solve? (1 sentence)**  
   Approximates the Q-value function with a deep neural network, enabling Q-learning to scale to high-dimensional state spaces like raw images.

3. **Intuition (plain-language explanation)**  
   Replace the Q-table with a neural network that predicts action values from pixels, while using replay buffers and target networks to stabilize learning.

4. **Inputs & Outputs**  
   - Input: State observations (e.g., image frames), action space, replay buffer, hyperparameters (learning rate, γ, ε for ε-greedy).  
   - Output: Trained Q-network Q(s,a; θ) that estimates expected return for each action; derived policy selects argmax_a Q(s,a).

5. **Step-by-step description (5–10 lines max)**  
1. Initialize Q-network with random weights θ and target network with weights θ⁻ = θ.
2. Interact with environment using ε-greedy policy; store transitions (s,a,r,s′,done) in replay buffer.
3. Sample mini-batches from replay buffer.
4. Compute target y = r + γ(1−done) max_{a′} Q(s′,a′; θ⁻).
5. Minimize loss (y − Q(s,a; θ))² via gradient descent.
6. Periodically update target network weights θ⁻ ← θ.
7. Decay ε over time to shift from exploration to exploitation.

6. **Tiny example (hand-simulated)**  
   Atari Breakout: input 84×84×4 frames; network outputs Q-values for joystick moves; DQN learns to control paddle and break bricks achieving human-level scores.

7. **Time & Space Complexity**  
   - Time: O(B·f) per update where B is batch size and f is network forward/backward cost; overall depends on number of environment steps.  
   - Space: O(|θ| + buffer_size) for network weights and replay memory (often 1e6 transitions).

8. **Strengths**  
- Handles high-dimensional inputs (images) without handcrafted features.
- Replay buffer decorrelates data, improving sample efficiency.

9. **Weaknesses / limitations**  
- Only supports discrete action spaces.
- Sensitive to hyperparameters; can suffer from overestimation bias.

10. **Compare with alternatives**  
    Alternatives: Double DQN, Dueling DQN, Actor-Critic, PPO

11. **30-second explanation (your own words)**  
    Uses a neural network to approximate Q-values combined with experience replay and target networks to stabilize Q-learning in complex environments.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
