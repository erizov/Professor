# SSD (Single Shot Detector)

1. **Name of Algorithm**  
   SSD (Single Shot Detector)

2. **What problem does it solve? (1 sentence)**  
   Detects objects in a single forward pass by applying multiple default boxes at different scales and aspect ratios to feature maps at various layers.

3. **Intuition (plain-language explanation)**  
   Like a multi-scale fishing net: cast nets of different sizes (default boxes) at different depths (feature map layers) to catch objects of various sizes in one pass.

4. **Inputs & Outputs**  
   - Input: Input image, base CNN (e.g., VGG), multi-scale feature maps, default boxes.  
   - Output: Bounding boxes with class predictions and confidence scores in single pass.

5. **Step-by-step description (5–10 lines max)**  
1. Extract feature maps from multiple CNN layers (different scales).
2. Generate default boxes (anchor boxes) at each feature map location with different scales and aspect ratios.
3. For each default box, predict: class scores and bounding box offsets.
4. Match default boxes to ground truth boxes using IoU threshold.
5. Train with multi-task loss: classification loss + localization loss.
6. Apply non-maximum suppression to remove duplicate detections.

6. **Tiny example (hand-simulated)**  
   Input 300×300 → VGG extracts features at 38×38, 19×19, 10×10, 5×5, 3×3, 1×1 → each location has 4-6 default boxes → predict class+box for each → NMS → final detections.

7. **Time & Space Complexity**  
   - Time: O(n·k) where n is number of default boxes (~8732 for 300×300 input), k is prediction time per box (fast: ~58 FPS).  
   - Space: O(n·(c+4)) for n boxes with c classes and 4 box coordinates.

8. **Strengths**  
- Fast single-shot detection (real-time capable).
- Good accuracy-speed trade-off.

9. **Weaknesses / limitations**  
- Struggles with small objects.
- Requires careful default box design.

10. **Compare with alternatives**  
    Alternatives: YOLO, Faster R-CNN, RetinaNet, EfficientDet

11. **30-second explanation (your own words)**  
    Performs object detection in a single forward pass using multi-scale feature maps and default boxes, achieving real-time speed with competitive accuracy.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
