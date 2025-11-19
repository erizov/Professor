# Pruning for Inference

1. **Name of Algorithm**  
   Pruning for Inference

2. **What problem does it solve? (1 sentence)**  
   Removes less important weights or neurons from trained models to reduce model size and accelerate inference while maintaining acceptable accuracy, enabling deployment on resource-constrained devices.

3. **Intuition (plain-language explanation)**  
   Like trimming a tree: pruning for inference is like trimming a tree to keep only the essential branches - you remove branches (weights/neurons) that don't contribute much to the tree's health (model accuracy), making the tree (model) smaller and easier to manage (faster inference) - the tree still functions well (maintains accuracy) but is more efficient (smaller, faster).

4. **Inputs & Outputs**  
   - Input: Trained model, pruning strategy, importance criteria, target sparsity, accuracy requirements.  
   - Output: Pruned model, reduced size, faster inference, maintained accuracy, optimized model.

5. **Step-by-step description (5–10 lines max)**  
1. Evaluate importance: evaluate importance of weights or neurons (magnitude, gradient, activation).
2. Select: select weights/neurons to prune based on importance criteria.
3. Prune: remove selected weights (set to zero) or remove neurons entirely.
4. Fine-tune: fine-tune pruned model to recover accuracy.
5. Iterate: optionally iterate pruning and fine-tuning (gradual pruning).
6. Validate: validate pruned model accuracy on test set.
7. Optimize: optimize pruning strategy for target sparsity and accuracy.
8. Deploy: deploy pruned model for inference.
9. Measure: measure inference speedup and accuracy impact.
10. Tune: tune pruning ratio based on accuracy-speed trade-off.

6. **Tiny example (hand-simulated)**  
   Pruning: BERT model (110M params) → evaluate: identify 50% least important weights → prune: remove 50% weights → fine-tune: recover accuracy → result: 55M params (50% reduction), 2x faster inference, 98% accuracy (vs 99% original) → pruned model deployable.

7. **Time & Space Complexity**  
   - Time: O(m) for pruning where m is model size, O(n) for fine-tuning where n is fine-tuning data size.  
   - Space: O(m·s) where m is model size, s is sparsity factor (reduced from O(m) full model).

8. **Strengths**  
- Efficiency: reduces model size and inference time.
- Deployability: enables deployment on resource-constrained devices.
- Maintains accuracy: can maintain good accuracy with proper pruning.

9. **Weaknesses / limitations**  
- Accuracy: may have some accuracy degradation.
- Fine-tuning: requires fine-tuning to recover accuracy.
- Sparsity: unstructured pruning may not speed up on all hardware.

10. **Compare with alternatives**  
    Alternatives: Full Model, Quantization, Knowledge Distillation, Structured Pruning

11. **30-second explanation (your own words)**  
    Removes less important weights or neurons from trained models to reduce model size and accelerate inference while maintaining acceptable accuracy, enabling deployment on resource-constrained devices.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
