# NAS (Neural Architecture Search)

1. **Name of Algorithm**  
   NAS (Neural Architecture Search)

2. **What problem does it solve? (1 sentence)**  
   Automatically discovers optimal neural network architectures for a given task and dataset by searching through architecture space, reducing manual design effort and potentially finding better architectures.

3. **Intuition (plain-language explanation)**  
   Like an AI architect designing buildings: instead of manually designing network architectures, use algorithms to explore millions of possible designs (different layer types, connections, widths), test them, and find the best one for your specific task.

4. **Inputs & Outputs**  
- Input: Search space (layer types, connections, hyperparameters), dataset, performance metric, search algorithm, computational budget.
   - Output: Discovered optimal architecture, trained model with that architecture.

5. **Step-by-step description (5–10 lines max)**  
1. Define search space: specify possible layer types (conv, attention, etc.), connection patterns, widths, depths.
2. Initialize search algorithm: reinforcement learning, evolutionary algorithms, or gradient-based methods.
3. Sample candidate architecture from search space.
4. Train candidate architecture (often with weight sharing or proxy tasks for speed).
5. Evaluate architecture performance on validation set.
6. Use performance as reward/signal to guide search algorithm.
7. Update search algorithm: RL updates policy, evolution selects best candidates, gradient-based updates architecture parameters.
8. Repeat: sample new candidates, train, evaluate, update search → continue until budget exhausted or convergence.
9. Return best architecture found, optionally train from scratch.

6. **Tiny example (hand-simulated)**  
   Image classification: search space = {conv layers, attention layers, skip connections, widths 32-512} → sample: 3 conv layers, 2 attention, width 256 → train 10 epochs → accuracy 92% → sample: 4 conv, 1 attention, width 128 → accuracy 94% → continue searching → find: 5 conv, 2 attention, width 192 → accuracy 96% (best).

7. **Time & Space Complexity**  
   - Time: O(S·T) where S is number of architectures sampled, T is training time per architecture (can be very expensive: thousands of GPU days).  
   - Space: O(A_max) for storing candidate architectures and their weights, where A_max is size of largest architecture in search space.

8. **Strengths**  
- Can discover architectures better than human-designed ones.
- Reduces manual architecture engineering effort.

9. **Weaknesses / limitations**  
- Computationally expensive (requires significant resources).
- May find architectures that overfit to specific datasets.

10. **Compare with alternatives**  
Alternatives: Manual Architecture Design, Transfer Learning, Architecture Templates, Efficient NAS (ENAS, DARTS)

11. **30-second explanation (your own words)**  
    Automatically searches through architecture space using algorithms like reinforcement learning or evolution to discover optimal neural network designs for specific tasks and datasets.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
