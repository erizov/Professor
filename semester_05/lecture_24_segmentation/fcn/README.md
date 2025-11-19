# FCN (Fully Convolutional Network)

1. **Name of Algorithm**  
   FCN (Fully Convolutional Network)

2. **What problem does it solve? (1 sentence)**  
   Performs pixel-level semantic segmentation by replacing fully connected layers with convolutions, enabling dense prediction on arbitrary-sized images.

3. **Intuition (plain-language explanation)**  
   Like a paint-by-numbers map: instead of classifying whole images, classify each pixel to create a detailed segmentation map showing what each pixel belongs to.

4. **Inputs & Outputs**  
   - Input: Input images of arbitrary size, pre-trained CNN (e.g., VGG, ResNet).  
   - Output: Dense pixel-wise class predictions (segmentation map) with same spatial dimensions as input.

5. **Step-by-step description (5–10 lines max)**  
1. Start with pre-trained CNN (e.g., VGG-16) and remove fully connected layers.
2. Convert FC layers to 1×1 convolutions to maintain spatial information.
3. Add upsampling layers (transposed convolutions) to restore spatial resolution.
4. Use skip connections from earlier layers to combine fine and coarse features.
5. Apply pixel-wise softmax to produce class probabilities for each pixel.
6. Train end-to-end with pixel-wise cross-entropy loss.

6. **Tiny example (hand-simulated)**  
   Input 500×500 image → VGG extracts features → remove FC layers → add 1×1 conv + upsampling → skip connections from pool3, pool4 → output 500×500 segmentation map with class per pixel.

7. **Time & Space Complexity**  
   - Time: O(n²·c) where n is spatial size, c is number of classes (single forward pass).  
   - Space: O(n²·c) for output segmentation map plus O(n²·d) for feature maps.

8. **Strengths**  
- First successful end-to-end CNN for semantic segmentation.
- Handles arbitrary input sizes and produces dense predictions.

9. **Weaknesses / limitations**  
- Coarse predictions due to information loss in downsampling.
- Requires skip connections for fine-grained details.

10. **Compare with alternatives**  
    Alternatives: U-Net, DeepLab, PSPNet, SegNet

11. **30-second explanation (your own words)**  
    Converts classification CNNs to segmentation networks by replacing FC layers with convolutions and adding upsampling, enabling dense pixel-wise predictions.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
