# LLM Quantization

1. **Name of Algorithm**  
   LLM Quantization

2. **What problem does it solve? (1 sentence)**  
   Reduces precision of LLM weights and activations from FP32/FP16 to lower precision (INT8, INT4, etc.), significantly reducing model size and inference latency while maintaining acceptable accuracy.

3. **Intuition (plain-language explanation)**  
   Like compressing a high-resolution photo: instead of storing model weights as 32-bit floats (high precision), store them as 8-bit integers (lower precision) - the model becomes much smaller and faster, with minimal quality loss, like a compressed photo that still looks good.

4. **Inputs & Outputs**  
   - Input: Trained LLM (FP32/FP16), quantization method (post-training or quantization-aware training), calibration dataset, target precision.  
   - Output: Quantized LLM with reduced precision weights, smaller size, faster inference.

5. **Step-by-step description (5–10 lines max)**  
1. Choose quantization method: post-training quantization (PTQ) or quantization-aware training (QAT).
2. For PTQ: collect calibration data (representative samples) to determine quantization ranges.
3. Quantize weights: map FP32 weights to INT8 using scale and zero-point: q = round(w/scale) + zero_point.
4. Quantize activations: similarly quantize activations to INT8 (may use per-channel or per-tensor scaling).
5. For QAT: simulate quantization during training (fake quantization) to learn quantized-friendly weights.
6. Calibrate: determine optimal scales for each layer to minimize quantization error.
7. Validate: test quantized model accuracy compared to original (may require fine-tuning for INT4).
8. Deploy: use quantized model with INT8/INT4 operations on supported hardware.

6. **Tiny example (hand-simulated)**  
   LLM quantization: GPT-3.5 (FP16, 350GB) → quantize to INT8 → model size: 175GB (2x reduction) → inference: 200ms → 100ms (2x faster on INT8 hardware) → accuracy: 95% → 94% (minimal loss). INT4: 87.5GB (4x reduction), 50ms (4x faster), 92% accuracy.

7. **Time & Space Complexity**  
   - Time: O(M) for quantization where M is model size (one-time conversion), inference O(M/k) where k is precision reduction factor (2x for INT8, 4x for INT4).  
   - Space: O(M/k) for quantized model where k is reduction factor (2x for INT8, 4x for INT4), O(M) for calibration data.

8. **Strengths**  
- Significant size reduction: 2-4x smaller models (INT8/INT4).
- Faster inference: 2-4x speedup on supported hardware.
- Lower memory: enables running large models on consumer hardware.

9. **Weaknesses / limitations**  
- Accuracy loss: may cause noticeable degradation, especially with INT4.
- Hardware dependency: requires hardware support for low-precision operations.
- Calibration overhead: requires representative data and careful calibration.

10. **Compare with alternatives**  
    Alternatives: FP16/BF16, Pruning, Knowledge Distillation, Model Compression

11. **30-second explanation (your own words)**  
    Reduces precision of LLM weights and activations to lower precision (INT8/INT4), significantly reducing model size and inference latency while maintaining acceptable accuracy.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
