# Model Parallelism

1. **Name of Algorithm**  
   Model Parallelism

2. **What problem does it solve? (1 sentence)**  
   Splits a large model across multiple devices/GPUs, with each device holding a portion of the model layers, enabling training of models too large to fit on a single device.

3. **Intuition (plain-language explanation)**  
   Like dividing a large book among multiple shelves: if the model is too big for one GPU's memory, split it across multiple GPUs - each GPU holds different layers, and data flows through them sequentially.

4. **Inputs & Outputs**  
   - Input: Large model architecture, number of devices/GPUs, layer partitioning strategy.  
   - Output: Trained model with parameters distributed across devices.

5. **Step-by-step description (5–10 lines max)**  
1. Partition model into segments: assign different layers to different devices (e.g., layers 0-10 on GPU 0, layers 11-20 on GPU 1).
2. Each device stores only its assigned layers and their parameters.
3. Forward pass: input data flows sequentially through devices (GPU 0 → GPU 1 → GPU 2).
4. Each device computes activations for its layers and passes to next device.
5. Backward pass: gradients flow in reverse (GPU 2 → GPU 1 → GPU 0).
6. Each device computes gradients for its layers and updates its parameters.
7. Synchronize activations and gradients between devices during forward/backward passes.
8. Repeat for next batch.

6. **Tiny example (hand-simulated)**  
   Transformer with 48 layers, 4 GPUs: GPU 0 holds layers 0-11, GPU 1 holds 12-23, GPU 2 holds 24-35, GPU 3 holds 36-47 → input flows: GPU 0 → GPU 1 → GPU 2 → GPU 3 → output → gradients flow back: GPU 3 → GPU 2 → GPU 1 → GPU 0.

7. **Time & Space Complexity**  
   - Time: O(T + C·L) where T is computation time, C is communication cost between devices, L is number of layer boundaries (sequential processing).  
   - Space: O(M/P) per device where M is model size, P is number of devices (each device stores 1/P of model).

8. **Strengths**  
- Enables training models larger than single device memory.
- Memory efficient: each device only stores its portion.

9. **Weaknesses / limitations**  
- Sequential processing: cannot parallelize within batch (slower than data parallelism).
- Communication overhead at layer boundaries.

10. **Compare with alternatives**  
    Alternatives: Data Parallelism, Pipeline Parallelism, Hybrid Parallelism, Gradient Checkpointing

11. **30-second explanation (your own words)**  
    Splits model layers across multiple devices, with data flowing sequentially through devices during forward and backward passes, enabling training of models too large for single device memory.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
