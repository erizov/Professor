# TensorFlow Lite (TFLite)

1. **Name of Algorithm**  
   TensorFlow Lite (TFLite)

2. **What problem does it solve? (1 sentence)**  
   Provides a lightweight framework for deploying TensorFlow models on mobile and edge devices, with optimized inference runtime, model conversion tools, and hardware acceleration support.

3. **Intuition (plain-language explanation)**  
   Like a compact version of TensorFlow made for phones: convert your big TensorFlow model into TFLite format, which is smaller and faster, then run it on Android/iOS devices with optimized inference engine.

4. **Inputs & Outputs**  
   - Input: TensorFlow model (SavedModel, Keras, or concrete function), quantization options, target device specifications.  
   - Output: TFLite model file (.tflite) optimized for mobile/edge deployment, ready for on-device inference.

5. **Step-by-step description (5–10 lines max)**  
1. Prepare TensorFlow model: ensure model is compatible (check for unsupported operations).
2. Convert to TFLite: use TFLiteConverter to convert SavedModel/Keras model to .tflite format.
3. Apply optimizations: enable quantization (INT8), pruning, or other optimizations during conversion.
4. Quantize (optional): use post-training quantization or quantization-aware training for INT8 models.
5. Validate TFLite model: test conversion accuracy and verify model behavior.
6. Deploy: integrate TFLite interpreter into mobile app (Android/iOS) or edge application.
7. Load model: use TFLite interpreter to load .tflite file on device.
8. Run inference: execute model on device CPU, GPU (via delegates), or specialized accelerators (NPU).

6. **Tiny example (hand-simulated)**  
   TensorFlow image classifier (SavedModel, 50MB) → TFLiteConverter with INT8 quantization → model.tflite (5MB) → deploy in Android app → TFLite interpreter loads model → camera captures image → inference: 30ms on phone CPU, works offline.

7. **Time & Space Complexity**  
   - Time: O(M) for conversion (one-time), inference O(M/k) where k is optimization factor (typically 2-5x faster than TensorFlow Mobile).  
   - Space: O(M/k) for TFLite model where k is compression factor (typically 4-10x smaller), O(M/k) for runtime memory.

8. **Strengths**  
- Optimized for mobile: smaller size and faster inference than full TensorFlow.
- Wide platform support: Android, iOS, embedded Linux, microcontrollers.
- Hardware acceleration: supports GPU, NPU delegates.

9. **Weaknesses / limitations**  
- Limited operation support: not all TensorFlow ops are supported.
- Requires model conversion step.

10. **Compare with alternatives**  
    Alternatives: ONNX Runtime Mobile, CoreML, TensorFlow Mobile, Native Mobile ML

11. **30-second explanation (your own words)**  
    Provides lightweight TensorFlow deployment framework for mobile and edge devices, with optimized inference runtime and model conversion tools enabling efficient on-device ML.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
