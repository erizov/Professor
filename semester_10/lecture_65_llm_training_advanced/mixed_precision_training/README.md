# Mixed Precision Training

1. **Name of Algorithm**  
   Mixed Precision Training

2. **What problem does it solve? (1 sentence)**  
   Accelerates neural network training by using lower precision (FP16/BF16) for most operations while maintaining FP32 precision for critical operations, reducing memory usage and increasing training speed on modern GPUs.

3. **Intuition (plain-language explanation)**  
   Like using different tools for different tasks: mixed precision training is like using a fast but less precise tool (FP16) for most work and a slower but precise tool (FP32) only when you need accuracy - you do most calculations quickly with FP16 (like rough measurements), but use FP32 for critical calculations that need precision (like final measurements) - this makes the overall work much faster while maintaining accuracy where it matters.

4. **Inputs & Outputs**  
   - Input: Model weights, activations, gradients, loss scaling, precision settings, GPU support.  
   - Output: Faster training, reduced memory, maintained accuracy, optimized computation.

5. **Step-by-step description (5–10 lines max)**  
1. Configure: configure mixed precision training (FP16/BF16 for most ops, FP32 for critical).
2. Forward pass: perform forward pass using FP16/BF16 for activations and weights.
3. Compute loss: compute loss in FP16/BF16.
4. Scale loss: scale loss by factor (e.g., 2^16) to prevent underflow.
5. Backward pass: compute gradients in FP16/BF16.
6. Unscale: unscale gradients before optimizer step.
7. Master weights: maintain FP32 master copy of weights for precision.
8. Update: update FP32 master weights, then copy to FP16 for next iteration.
9. Handle overflow: detect and handle gradient overflow (skip update if overflow).
10. Optimize: optimize loss scaling and precision settings.

6. **Tiny example (hand-simulated)**  
   Mixed precision: transformer training → FP32 baseline: 100 hours, 16GB memory → mixed precision: FP16 for most ops, FP32 for master weights → speed: 2x faster (50 hours) → memory: 50% reduction (8GB) → accuracy: 99.5% of FP32 → mixed precision successful.

7. **Time & Space Complexity**  
   - Time: O(n/2) approximately where n is FP32 training time (2x speedup on modern GPUs with tensor cores).  
   - Space: O(m/2) where m is FP32 memory usage (approximately 50% reduction with FP16).

8. **Strengths**  
- Speed: 1.5-2x faster training on modern GPUs with tensor cores.
- Memory: reduces memory usage by ~50%, enabling larger batch sizes.
- Accuracy: maintains model accuracy with proper loss scaling.

9. **Weaknesses / limitations**  
- Hardware: requires GPU support for mixed precision (Tensor Cores, etc.).
- Tuning: requires tuning loss scaling factor.
- Overflow: risk of gradient overflow if not properly scaled.

10. **Compare with alternatives**  
    Alternatives: FP32 Training, FP16 Training, BF16 Training, INT8 Training

11. **30-second explanation (your own words)**  
    Accelerates neural network training by using lower precision (FP16/BF16) for most operations while maintaining FP32 precision for critical operations, reducing memory usage and increasing training speed on modern GPUs.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
