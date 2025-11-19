# U-Net

1. **Name of Algorithm**  
   U-Net

2. **What problem does it solve? (1 sentence)**  
   Performs biomedical image segmentation using a symmetric encoder-decoder architecture with skip connections to preserve fine-grained spatial details.

3. **Intuition (plain-language explanation)**  
   Like a funnel with a mirror: compress information going down (encoder), then expand it back up (decoder), while keeping shortcuts (skip connections) to preserve details lost during compression.

4. **Inputs & Outputs**  
   - Input: Input images (often biomedical), encoder-decoder architecture, skip connections.  
   - Output: Pixel-wise segmentation maps with same spatial dimensions as input.

5. **Step-by-step description (5–10 lines max)**  
1. Encoder (contracting path): apply 3×3 conv + ReLU, then 2×2 max pooling (repeat 4-5 times).
2. Bottleneck: two 3×3 convolutions at lowest resolution.
3. Decoder (expansive path): 2×2 upsampling, concatenate with corresponding encoder feature map (skip connection), then 3×3 conv + ReLU (repeat 4-5 times).
4. Final layer: 1×1 convolution to map to number of classes.
5. Train with pixel-wise cross-entropy loss (optionally with dice loss).
6. Output segmentation map with class prediction for each pixel.

6. **Tiny example (hand-simulated)**  
   Input 572×572 → encoder: 64→128→256→512→1024 (downsampling) → decoder: 1024→512→256→128→64 (upsampling with skip connections) → output 388×388 segmentation map.

7. **Time & Space Complexity**  
   - Time: O(n²·c) where n is spatial size, c is channels (single forward pass, efficient).  
   - Space: O(n²·c) for feature maps (skip connections require storing encoder features).

8. **Strengths**  
- Excellent for biomedical segmentation with limited data.
- Skip connections preserve fine-grained details.

9. **Weaknesses / limitations**  
- Symmetric architecture may not be optimal for all tasks.
- Memory usage grows with input size due to skip connections.

10. **Compare with alternatives**  
    Alternatives: FCN, DeepLab, SegNet, Attention U-Net

11. **30-second explanation (your own words)**  
    Uses symmetric encoder-decoder architecture with skip connections to combine high-level semantic features with low-level spatial details, enabling precise segmentation.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
