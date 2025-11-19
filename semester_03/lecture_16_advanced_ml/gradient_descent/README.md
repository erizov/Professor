# Gradient Descent

1. **Name of Algorithm**  
   Gradient Descent

2. **What problem does it solve? (1 sentence)**  
   Optimizes differentiable objective functions by iteratively moving parameters in the direction of steepest descent to find a local minimum.

3. **Intuition (plain-language explanation)**  
   Imagine descending a foggy hill with only local slope information: step downhill proportional to the slope and step size (learning rate).

4. **Inputs & Outputs**  
   - Input: Objective function J(θ), gradient ∇J(θ), initial parameters θ₀, learning rate α, stopping criteria (iterations or tolerance).  
   - Output: Optimized parameter vector θ* approximating a (local) minimum of J.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize parameters θ₀ (random or heuristic).
2. Repeat until convergence: compute gradient g = ∇J(θ).
3. Update parameters θ ← θ − α · g.
4. Adapt learning rate or use schedules (optional).
5. Stop when gradient norm < ε or iterations reach limit.

6. **Tiny example (hand-simulated)**  
   Linear regression cost J(θ) = (1/2m) Σ (hθ(xᵢ) − yᵢ)². Gradient descent updates θ simultaneously until training error plateaus.

7. **Time & Space Complexity**  
   - Time: O(k · n · d) for k iterations on dataset of n samples with d features (full-batch).  
   - Space: O(d) for parameter vector; O(n·d) if full dataset kept in memory.

8. **Strengths**  
- Scales to high-dimensional problems with stochastic/mini-batch variants.
- Simple to implement and differentiable-model agnostic.

9. **Weaknesses / limitations**  
- Sensitive to learning rate; may diverge or be slow.
- Gets trapped in local minima/saddle points on non-convex surfaces.

10. **Compare with alternatives**  
    Alternatives: Stochastic Gradient Descent, Momentum/Nesterov, Adam/Adaptive Optimizers

11. **30-second explanation (your own words)**  
    Iteratively nudges parameters opposite the gradient so the objective decreases each step, converging toward minima when learning rate and convergence criteria are well tuned.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
