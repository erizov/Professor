# Pruning

1. **Name of Algorithm**  
   Pruning

2. **What problem does it solve? (1 sentence)**  
   Removes unnecessary weights, neurons, or layers from a trained neural network to reduce model size and inference time while maintaining accuracy, enabling deployment on resource-constrained devices.

3. **Intuition (plain-language explanation)**  
   Like trimming a tree: after training, identify which branches (weights/neurons) are least important, cut them out, and the tree (model) becomes smaller and faster while still functioning well.

4. **Inputs & Outputs**  
   - Input: Trained model, pruning criterion (magnitude, importance score), pruning ratio (sparsity target), fine-tuning data.  
   - Output: Pruned model with reduced parameters, maintained or slightly reduced accuracy.

5. **Step-by-step description (5–10 lines max)**  
1. Train model to convergence on full architecture.
2. Evaluate importance: compute importance scores for weights/neurons (e.g., magnitude, gradient-based, or activation-based).
3. Select pruning targets: identify weights/neurons with lowest importance scores.
4. Prune: set selected weights to zero (structured: remove entire neurons/channels, unstructured: remove individual weights).
5. Fine-tune: retrain pruned model (with remaining weights) to recover accuracy.
6. Optionally iterate: prune more → fine-tune → repeat until target sparsity reached.
7. Remove zero weights entirely to get final compact model.
8. Deploy pruned model with reduced size and faster inference.

6. **Tiny example (hand-simulated)**  
   CNN with 1M parameters: train to 95% accuracy → evaluate importance → find 60% of weights have magnitude < 0.01 → prune those weights → model now 400K parameters → fine-tune → accuracy 94.5% → deploy: 2.5x smaller, 2x faster inference.

7. **Time & Space Complexity**  
   - Time: O(T_train + P·T_finetune) where T_train is initial training, P is pruning iterations, T_finetune is fine-tuning time per iteration.  
   - Space: O(M) for original model, O(M·(1-s)) for pruned model where s is sparsity ratio.

8. **Strengths**  
- Significantly reduces model size and inference time.
- Can maintain accuracy with proper fine-tuning.

9. **Weaknesses / limitations**  
- Requires retraining/fine-tuning after pruning.
- Aggressive pruning may cause accuracy degradation.

10. **Compare with alternatives**  
    Alternatives: Quantization, Knowledge Distillation, Low-Rank Factorization, Structured Pruning

11. **30-second explanation (your own words)**  
    Removes unimportant weights or neurons from trained models based on importance criteria, then fine-tunes to recover accuracy, resulting in smaller, faster models suitable for deployment.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
