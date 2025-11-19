# Transfer Learning

1. **Name of Algorithm**  
   Transfer Learning

2. **What problem does it solve? (1 sentence)**  
   Applies knowledge learned from one task (source) to improve learning on a related task (target), reducing data and training requirements.

3. **Intuition (plain-language explanation)**  
   Like learning to drive a car after knowing how to ride a bike: transfer balance and coordination skills (learned features) to the new task (driving) instead of starting from scratch.

4. **Inputs & Outputs**  
   - Input: Pre-trained model on source task, target task dataset, transfer strategy.  
   - Output: Model adapted for target task with improved performance and efficiency.

5. **Step-by-step description (5–10 lines max)**  
1. Train or obtain model on large source dataset (e.g., ImageNet).
2. Identify transferable knowledge (features, representations).
3. Choose transfer strategy: feature extraction, fine-tuning, or domain adaptation.
4. Apply strategy to adapt model for target task.
5. Train on target dataset (often with less data than needed for from-scratch training).
6. Evaluate and iterate on transfer approach.

6. **Tiny example (hand-simulated)**  
   Model trained on ImageNet (1M images, 1000 classes) → transfer to medical diagnosis (1000 images, 5 classes) → fine-tune → achieve 90% accuracy vs 60% from scratch.

7. **Time & Space Complexity**  
   - Time: O(n_s + n_t·e) where n_s is source data size, n_t is target data size, e is epochs (much faster than training from scratch).  
   - Space: O(m) for model weights (same as base model).

8. **Strengths**  
- Reduces data requirements for target task.
- Faster training and better performance than from-scratch learning.

9. **Weaknesses / limitations**  
- Requires related source and target tasks.
- Negative transfer possible if tasks are too different.

10. **Compare with alternatives**  
    Alternatives: Training from Scratch, Multi-Task Learning, Domain Adaptation

11. **30-second explanation (your own words)**  
    Leverages knowledge from a source task to improve learning on a target task, enabling effective learning with limited data by transferring learned representations.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
