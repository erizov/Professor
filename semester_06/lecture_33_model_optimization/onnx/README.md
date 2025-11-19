# ONNX (Open Neural Network Exchange)

1. **Name of Algorithm**  
   ONNX (Open Neural Network Exchange)

2. **What problem does it solve? (1 sentence)**  
   Provides an open standard format for representing machine learning models, enabling interoperability between different frameworks (PyTorch, TensorFlow, etc.) and deployment across diverse platforms and hardware.

3. **Intuition (plain-language explanation)**  
   Like a universal translator for ML models: convert your model from any framework (PyTorch, TensorFlow) into ONNX format, then run it on any platform (mobile, edge, cloud) that supports ONNX - one model, many destinations.

4. **Inputs & Outputs**  
   - Input: Trained model from source framework (PyTorch, TensorFlow, etc.), model architecture, weights.  
   - Output: ONNX model file (.onnx) that can be run on ONNX-compatible runtimes.

5. **Step-by-step description (5–10 lines max)**  
1. Export model from source framework: use framework-specific ONNX exporter (torch.onnx.export, tf2onnx).
2. Define input/output shapes and data types for the ONNX graph.
3. Convert framework operations to ONNX operators: map framework ops (conv, relu, etc.) to ONNX standard ops.
4. Serialize model to ONNX protobuf format (.onnx file).
5. Validate ONNX model: check graph structure, operator compatibility, shape inference.
6. Optimize ONNX model (optional): use ONNX Runtime optimizations (graph fusion, constant folding).
7. Deploy: load ONNX model in target runtime (ONNX Runtime, TensorRT, etc.) on target platform.
8. Run inference: execute ONNX model on CPU, GPU, or specialized hardware.

6. **Tiny example (hand-simulated)**  
   PyTorch ResNet-50 → export to ONNX → get resnet50.onnx (50MB) → deploy on mobile using ONNX Runtime → inference: 30ms on iPhone, 25ms on Android → same model works on both platforms.

7. **Time & Space Complexity**  
   - Time: O(M) for conversion where M is model size (one-time), inference depends on runtime and hardware.  
   - Space: O(M) for ONNX model file (similar to original model size, may be slightly larger due to metadata).

8. **Strengths**  
- Framework-agnostic: convert from any framework to any platform.
- Widely supported by major ML frameworks and runtimes.

9. **Weaknesses / limitations**  
- Not all framework operations are supported (may require workarounds).
- Conversion may introduce slight numerical differences.

10. **Compare with alternatives**  
    Alternatives: TensorFlow Lite, CoreML, TensorRT, Native Framework Deployment

11. **30-second explanation (your own words)**  
    Provides open standard format for ML models, enabling framework-agnostic deployment across diverse platforms and hardware through standardized model representation.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
