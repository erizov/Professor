# EfficientNet

1. **Name of Algorithm**  
   EfficientNet

2. **What problem does it solve? (1 sentence)**  
   Scales CNN depth, width, and resolution uniformly using compound scaling to achieve better accuracy and efficiency than scaling dimensions independently.

3. **Intuition (plain-language explanation)**  
   Like adjusting a camera's zoom, aperture, and ISO together: balance all three dimensions (depth, width, resolution) proportionally for optimal performance, rather than just making one bigger.

4. **Inputs & Outputs**  
   - Input: Input images, base EfficientNet architecture, compound scaling coefficient φ.  
   - Output: Scaled EfficientNet model with optimized depth, width, and resolution.

5. **Step-by-step description (5–10 lines max)**  
1. Start with baseline EfficientNet-B0 architecture (found via neural architecture search).
2. Apply compound scaling: depth^α × width^β × resolution^γ = 2^φ, where α+β+γ=1.
3. Scale depth (number of layers), width (number of channels), and resolution (input size) together.
4. Train scaled model on target dataset.
5. Iterate to find optimal φ for accuracy/efficiency trade-off.

6. **Tiny example (hand-simulated)**  
   EfficientNet-B0 baseline → scale with φ=1 → EfficientNet-B1 (depth×1.2, width×1.1, resolution×1.15) → achieves better accuracy than ResNet-50 with 8x fewer parameters.

7. **Time & Space Complexity**  
   - Time: O(d·w²·r²) where d is depth, w is width, r is resolution (scales polynomially with φ).  
   - Space: O(d·w²) for model parameters (grows with compound scaling).

8. **Strengths**  
- Achieves state-of-the-art accuracy with fewer parameters.
- Systematic scaling approach outperforms ad-hoc scaling.

9. **Weaknesses / limitations**  
- Requires careful tuning of compound scaling coefficients.
- Higher resolution increases memory requirements.

10. **Compare with alternatives**  
    Alternatives: ResNet, MobileNet, Inception, Manual Architecture Scaling

11. **30-second explanation (your own words)**  
    Uses compound scaling to uniformly scale depth, width, and resolution, achieving better accuracy-efficiency trade-offs than scaling dimensions independently.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
