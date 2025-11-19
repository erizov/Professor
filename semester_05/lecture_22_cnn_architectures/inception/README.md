# Inception (GoogLeNet)

1. **Name of Algorithm**  
   Inception (GoogLeNet)

2. **What problem does it solve? (1 sentence)**  
   Uses parallel convolutions of different sizes (1×1, 3×3, 5×5) in the same layer to capture features at multiple scales efficiently.

3. **Intuition (plain-language explanation)**  
   Like using multiple camera lenses simultaneously: capture details at different scales (close-up, medium, wide) in parallel, then combine the best views.

4. **Inputs & Outputs**  
   - Input: Input feature maps, multiple convolution filter sizes (1×1, 3×3, 5×5), max pooling.  
   - Output: Feature maps with multi-scale representations concatenated together.

5. **Step-by-step description (5–10 lines max)**  
1. Apply 1×1 convolution for dimensionality reduction and feature combination.
2. Apply 3×3 and 5×5 convolutions in parallel to capture different scales.
3. Apply max pooling for spatial reduction.
4. Concatenate outputs from all parallel paths.
5. Use 1×1 convolutions to reduce channel dimensions before expensive operations.
6. Stack multiple Inception modules to build deep network.

6. **Tiny example (hand-simulated)**  
   Input 256×256×192 → Inception module: 1×1 conv (64 filters), 3×3 conv (128 filters), 5×5 conv (32 filters), max pool → concatenate → output 256×256×256.

7. **Time & Space Complexity**  
   - Time: O(n²·c·k²) where n is spatial size, c is channels, k is kernel size (reduced by 1×1 bottlenecks).  
   - Space: O(n²·c) for feature maps (1×1 convolutions reduce memory).

8. **Strengths**  
- Captures multi-scale features efficiently.
- 1×1 convolutions reduce computational cost.

9. **Weaknesses / limitations**  
- Complex architecture with many hyperparameters.
- Wider layers increase memory usage.

10. **Compare with alternatives**  
    Alternatives: ResNet, VGG, EfficientNet, Standard Sequential CNNs

11. **30-second explanation (your own words)**  
    Uses parallel convolutions of different sizes in the same layer to capture features at multiple scales, improving representation power while controlling computational cost.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
