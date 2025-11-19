# RLHF (Reinforcement Learning from Human Feedback)

1. **Name of Algorithm**  
   RLHF (Reinforcement Learning from Human Feedback)

2. **What problem does it solve? (1 sentence)**  
   Aligns LLM behavior with human preferences by training models using reinforcement learning with human feedback as reward signal, making models more helpful, harmless, and honest.

3. **Intuition (plain-language explanation)**  
   Like training a dog with treats: humans provide feedback (rewards) on model outputs - good outputs get high rewards, bad outputs get low rewards - the model learns through reinforcement learning to produce outputs that humans prefer, becoming more aligned with human values.

4. **Inputs & Outputs**  
   - Input: Base LLM, human preference dataset, reward model, RL algorithm (PPO), prompt dataset.  
   - Output: RLHF-aligned LLM that produces outputs preferred by humans.

5. **Step-by-step description (5–10 lines max)**  
1. Collect human feedback: gather human preferences on model outputs (rankings, ratings, comparisons).
2. Train reward model: train a model to predict human preferences (reward model learns to score outputs).
3. Initialize policy: start with instruction-tuned or base LLM as initial policy.
4. Generate responses: use current policy to generate responses to prompts.
5. Score responses: use reward model to score generated responses.
6. Update policy: use PPO (Proximal Policy Optimization) to update policy to maximize rewards.
7. Apply KL penalty: add KL divergence penalty to prevent policy from deviating too far from base model.
8. Iterate: repeat generation, scoring, and policy updates until convergence.
9. Evaluate: test aligned model on safety, helpfulness, and honesty metrics.

6. **Tiny example (hand-simulated)**  
   RLHF alignment: base GPT-3 → collect human preferences: 'Helpful response' (reward +1), 'Harmful response' (reward -1), 'Neutral' (reward 0) → train reward model → use PPO to update GPT-3 policy → model learns to generate helpful, harmless responses → ChatGPT-like behavior.

7. **Time & Space Complexity**  
   - Time: O(I·(G + R + U)) where I is iterations, G is generation time, R is reward scoring, U is policy update (computationally expensive, requires significant resources).  
   - Space: O(M) for policy model, O(R) for reward model, O(D) for preference dataset where D is number of preference pairs.

8. **Strengths**  
- Alignment: significantly improves model alignment with human values.
- Safety: reduces harmful, biased, or untruthful outputs.
- Helpfulness: makes models more useful and responsive to user needs.

9. **Weaknesses / limitations**  
- Expensive: requires large-scale human feedback collection and compute.
- Complex: involves multiple stages (reward modeling, RL training).
- May over-optimize: models may exploit reward model rather than truly aligning.

10. **Compare with alternatives**  
    Alternatives: Supervised Fine-tuning, Constitutional AI, Self-Critique, Red Teaming

11. **30-second explanation (your own words)**  
    Aligns LLM behavior with human preferences by training models using reinforcement learning with human feedback as reward signal, making models more helpful, harmless, and honest.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
