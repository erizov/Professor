# Quantization

1. **Name of Algorithm**  
   Quantization

2. **What problem does it solve? (1 sentence)**  
   Reduces precision of model weights and activations from floating-point (32-bit) to lower precision (8-bit, 4-bit, etc.), reducing model size and accelerating inference on hardware that supports low-precision operations.

3. **Intuition (plain-language explanation)**  
   Like rounding numbers to fewer decimal places: instead of storing weights as 32-bit floats (0.123456789), store them as 8-bit integers (0.123) - takes less space and can be computed faster on specialized hardware, with minimal accuracy loss.

4. **Inputs & Outputs**  
   - Input: Trained model (FP32), target precision (INT8, INT4, etc.), calibration dataset, quantization scheme (post-training or quantization-aware training).  
   - Output: Quantized model with reduced precision weights/activations, smaller size, faster inference.

5. **Step-by-step description (5–10 lines max)**  
1. Choose quantization scheme: post-training quantization (PTQ) or quantization-aware training (QAT).
2. For PTQ: calibrate quantization ranges using representative data to determine min/max values for each layer.
3. Quantize weights: map FP32 values to INT8 using scale and zero-point: q = round(w/scale) + zero_point.
4. Quantize activations: similarly map activations to INT8 (may use different scales per layer).
5. For QAT: simulate quantization during training (fake quantization) to learn quantized-friendly weights.
6. Deploy quantized model: use INT8 operations on supported hardware (GPUs, TPUs, mobile chips).
7. Optionally fine-tune quantized model to recover accuracy.
8. Evaluate: measure accuracy and speedup compared to FP32 model.

6. **Tiny example (hand-simulated)**  
   ResNet-50: FP32 weights (4 bytes each) → quantize to INT8 (1 byte each) → model size: 100MB → 25MB (4x reduction) → inference: 50ms → 12ms (4x faster on INT8 hardware) → accuracy: 95% → 94.8% (minimal loss).

7. **Time & Space Complexity**  
   - Time: O(M) for quantization where M is model size (one-time conversion), inference O(M/4) for INT8 vs O(M) for FP32.  
   - Space: O(M/4) for INT8 model vs O(M) for FP32 (4x reduction), plus O(M) for calibration data.

8. **Strengths**  
- Significant size reduction (4x for INT8) and speedup on supported hardware.
- Minimal accuracy loss with proper calibration.

9. **Weaknesses / limitations**  
- Requires hardware support for low-precision operations.
- Extreme quantization (INT4) may cause noticeable accuracy drop.

10. **Compare with alternatives**  
    Alternatives: Pruning, Knowledge Distillation, Mixed Precision Training, Dynamic Quantization

11. **30-second explanation (your own words)**  
    Reduces weight and activation precision from FP32 to lower precision (INT8/INT4), achieving significant size reduction and speedup on specialized hardware with minimal accuracy loss.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
