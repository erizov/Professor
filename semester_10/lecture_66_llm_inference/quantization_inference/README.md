# Quantization for Inference

1. **Name of Algorithm**  
   Quantization for Inference

2. **What problem does it solve? (1 sentence)**  
   Reduces precision of model weights and activations from FP32 to lower precision (INT8, INT4) during inference, reducing model size and accelerating inference on hardware that supports low-precision operations.

3. **Intuition (plain-language explanation)**  
   Like using a simpler measuring tool: quantization for inference is like using a ruler with fewer markings (INT8) instead of a precise caliper (FP32) - the simpler ruler (lower precision) is faster to use and takes less space, and for most measurements (inference), it's accurate enough - you trade a tiny bit of precision for much better speed and efficiency, making measurements (inference) much faster.

4. **Inputs & Outputs**  
   - Input: FP32 model, target precision, calibration data, quantization scheme, hardware support.  
   - Output: Quantized model, reduced precision, faster inference, smaller model, optimized deployment.

5. **Step-by-step description (5–10 lines max)**  
1. Calibrate: calibrate quantization parameters using representative data.
2. Quantize weights: convert FP32 weights to target precision (INT8, INT4).
3. Quantize activations: convert activations to target precision during inference.
4. Scale: apply scaling factors to maintain numerical range.
5. Dequantize: dequantize outputs if needed (convert back to FP32).
6. Validate: validate quantized model accuracy on test set.
7. Optimize: optimize quantization scheme (per-tensor, per-channel) for accuracy.
8. Deploy: deploy quantized model on target hardware.
9. Measure: measure inference speedup and accuracy impact.
10. Tune: tune quantization parameters for optimal accuracy-speed trade-off.

6. **Tiny example (hand-simulated)**  
   Quantization: GPT-3 (FP32, 700GB) → INT8 quantization → calibrate: determine scaling factors → quantize: convert weights to INT8 → result: 175GB (4x smaller), 2-4x faster inference, 99% accuracy (vs 100% FP32) → quantized model deployable on INT8 hardware.

7. **Time & Space Complexity**  
   - Time: O(m) for quantization where m is model size, O(1) per operation (faster with INT8 operations).  
   - Space: O(m/p) where m is FP32 model size, p is precision reduction factor (4x for INT8, 8x for INT4).

8. **Strengths**  
- Speed: 2-4x faster inference on supported hardware.
- Size: 4x smaller model (INT8) or 8x smaller (INT4).
- Efficiency: better energy efficiency and lower memory bandwidth.

9. **Weaknesses / limitations**  
- Hardware: requires hardware support for low-precision operations.
- Accuracy: may have slight accuracy degradation.
- Calibration: requires calibration data and careful tuning.

10. **Compare with alternatives**  
    Alternatives: FP32 Inference, FP16 Inference, Dynamic Quantization, Post-Training Quantization

11. **30-second explanation (your own words)**  
    Reduces precision of model weights and activations from FP32 to lower precision (INT8, INT4) during inference, reducing model size and accelerating inference on hardware that supports low-precision operations.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
