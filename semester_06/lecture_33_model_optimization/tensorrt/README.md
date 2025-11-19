# TensorRT

1. **Name of Algorithm**  
   TensorRT

2. **What problem does it solve? (1 sentence)**  
   Optimizes and accelerates deep learning inference on NVIDIA GPUs by performing graph optimizations, layer fusion, precision calibration, and kernel auto-tuning for maximum performance.

3. **Intuition (plain-language explanation)**  
   Like a race car tuner for your model: takes your neural network and fine-tunes it specifically for NVIDIA GPUs - combines operations, optimizes memory usage, and finds the fastest way to run it, making inference much faster.

4. **Inputs & Outputs**  
   - Input: Trained model (ONNX, TensorFlow, PyTorch), calibration dataset (for INT8), target GPU architecture, optimization profile.  
   - Output: Optimized TensorRT engine (.engine file) with fused operations and optimized kernels for target GPU.

5. **Step-by-step description (5–10 lines max)**  
1. Load model: import from ONNX, TensorFlow, or PyTorch format.
2. Build TensorRT engine: parse model graph, apply optimizations (layer fusion, kernel selection).
3. Optimize graph: fuse operations (conv+bn+relu → single kernel), eliminate redundant operations.
4. Select kernels: choose fastest CUDA kernels for each layer based on GPU architecture.
5. Calibrate for INT8 (optional): use calibration dataset to determine quantization scales for INT8 inference.
6. Build engine: compile optimized graph into TensorRT engine file (.engine).
7. Serialize engine: save optimized engine for deployment (can be reused without rebuilding).
8. Deploy: load engine in inference application, run optimized inference on GPU.

6. **Tiny example (hand-simulated)**  
   ResNet-50 ONNX model → TensorRT optimization → layer fusion: conv+bn+relu fused → INT8 quantization → optimized engine → inference: 50ms → 8ms (6x speedup) on NVIDIA V100 GPU.

7. **Time & Space Complexity**  
   - Time: O(M·T_build) for engine building where M is model size, T_build includes optimization time (one-time cost), inference O(M/k) where k is speedup factor.  
   - Space: O(M) for engine file (may be larger than original due to optimized kernels), O(M) for GPU memory during inference.

8. **Strengths**  
- Significant inference speedup (2-10x) on NVIDIA GPUs.
- Automatic optimization: no manual tuning required.

9. **Weaknesses / limitations**  
- NVIDIA GPU only (not portable to other hardware).
- Engine building can be time-consuming.

10. **Compare with alternatives**  
    Alternatives: ONNX Runtime, TensorFlow Lite, OpenVINO, Native CUDA

11. **30-second explanation (your own words)**  
    Optimizes and accelerates deep learning inference on NVIDIA GPUs through graph optimizations, layer fusion, and kernel auto-tuning, achieving significant speedup with minimal accuracy loss.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
