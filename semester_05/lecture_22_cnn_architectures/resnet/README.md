# ResNet (Residual Network)

1. **Name of Algorithm**  
   ResNet (Residual Network)

2. **What problem does it solve? (1 sentence)**  
   Enables training of very deep networks by using skip connections (residual blocks) that allow gradients to flow directly, solving the vanishing gradient problem.

3. **Intuition (plain-language explanation)**  
   Like a highway bypass: if the main road (layers) is blocked, use the bypass (skip connection) to get through. This makes it easier to train very deep networks.

4. **Inputs & Outputs**  
   - Input: Input feature maps, residual block configuration, number of layers.  
   - Output: Deep network with residual connections enabling effective gradient flow.

5. **Step-by-step description (5–10 lines max)**  
1. Define residual block: F(x) = activation(conv(x) + x) where x is input (skip connection).
2. Stack multiple residual blocks to build deep network.
3. Use identity mapping for skip connection when dimensions match.
4. Use 1×1 convolution for skip connection when dimensions need adjustment.
5. Apply batch normalization and ReLU after convolutions.
6. Train network end-to-end with standard backpropagation.

6. **Tiny example (hand-simulated)**  
   ResNet-50: input → conv → 16 residual blocks (each with 2-3 conv layers) → global avg pool → classifier. Skip connections allow training 50+ layers vs 20 for plain CNN.

7. **Time & Space Complexity**  
   - Time: O(d·n²·c²) where d is depth, n is spatial size, c is channels (similar to plain CNN but enables deeper networks).  
   - Space: O(d·c²) for parameters (skip connections add minimal overhead).

8. **Strengths**  
- Enables training of very deep networks (100+ layers).
- Solves vanishing gradient problem effectively.

9. **Weaknesses / limitations**  
- Slightly more memory due to skip connections.
- May have redundant representations in very deep networks.

10. **Compare with alternatives**  
    Alternatives: Plain CNNs, DenseNet, Highway Networks, Inception

11. **30-second explanation (your own words)**  
    Uses skip connections in residual blocks to enable direct gradient flow, allowing training of very deep networks that would otherwise suffer from vanishing gradients.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
