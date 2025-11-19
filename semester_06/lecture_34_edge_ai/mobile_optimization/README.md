# Mobile Optimization

1. **Name of Algorithm**  
   Mobile Optimization

2. **What problem does it solve? (1 sentence)**  
   Optimizes machine learning models specifically for mobile devices (smartphones, tablets) by reducing model size, memory usage, and inference time while maintaining accuracy, enabling real-time on-device ML applications.

3. **Intuition (plain-language explanation)**  
   Like packing a suitcase efficiently: take a large model and compress it (quantization, pruning) so it fits in a phone's limited memory and runs fast on mobile processors, while keeping it accurate enough for the task.

4. **Inputs & Outputs**  
   - Input: Trained model, target mobile platform (iOS/Android), optimization techniques (quantization, pruning, architecture search).  
   - Output: Optimized mobile model with reduced size and latency, suitable for on-device deployment.

5. **Step-by-step description (5–10 lines max)**  
1. Analyze model: identify bottlenecks (large layers, expensive operations).
2. Apply quantization: convert FP32 to INT8 to reduce size and speed up inference.
3. Apply pruning: remove unimportant weights to further reduce model size.
4. Use mobile-friendly architectures: replace heavy operations with efficient alternatives (depthwise separable conv, mobile blocks).
5. Optimize for mobile hardware: leverage mobile GPU (Metal on iOS, OpenGL/Vulkan on Android) or Neural Processing Units (NPUs).
6. Convert to mobile format: TensorFlow Lite, CoreML (iOS), or ONNX Runtime Mobile.
7. Benchmark on target devices: measure latency, memory usage, battery impact.
8. Iterate: further optimize if latency or size targets not met.

6. **Tiny example (hand-simulated)**  
   Image classification: ResNet-50 (100MB, 200ms) → quantize to INT8 (25MB) → replace with MobileNet (4MB) → optimize for iPhone GPU → CoreML format → deploy → inference: 15ms, 4MB model, works offline.

7. **Time & Space Complexity**  
   - Time: O(M·O) for optimization where M is model size, O is optimization iterations, inference O(M/k) where k is optimization factor (typically 2-10x speedup).  
   - Space: O(M/k) for optimized model where k is compression factor (typically 4-10x reduction), O(M/k) for runtime memory.

8. **Strengths**  
- Enables real-time ML on mobile devices.
- Reduces battery consumption compared to cloud inference.
- Works offline without network dependency.

9. **Weaknesses / limitations**  
- Requires significant optimization effort.
- May sacrifice some accuracy for speed/size.

10. **Compare with alternatives**  
    Alternatives: Cloud Inference, Hybrid Mobile-Cloud, Edge Computing, Progressive Web Apps

11. **30-second explanation (your own words)**  
    Optimizes ML models for mobile devices through quantization, pruning, and architecture optimization, enabling real-time on-device inference with reduced size and latency.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
