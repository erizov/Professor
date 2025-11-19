# YOLO (You Only Look Once)

1. **Name of Algorithm**  
   YOLO (You Only Look Once)

2. **What problem does it solve? (1 sentence)**  
   Divides image into grid cells and predicts bounding boxes and class probabilities directly from full images in one evaluation, enabling real-time object detection.

3. **Intuition (plain-language explanation)**  
   Like a single glance at a scene: instead of scanning multiple times, look once and immediately identify what's where, trading some accuracy for speed.

4. **Inputs & Outputs**  
   - Input: Input image, grid division (e.g., 7×7), CNN backbone.  
   - Output: Grid of predictions: bounding boxes, confidence scores, and class probabilities.

5. **Step-by-step description (5–10 lines max)**  
1. Divide input image into S×S grid (e.g., 7×7).
2. Each grid cell predicts B bounding boxes and class probabilities.
3. For each bounding box, predict: center coordinates, width, height, confidence score.
4. Predict class probabilities for each grid cell (shared across boxes in that cell).
5. Combine predictions: final score = confidence × class probability.
6. Apply non-maximum suppression to remove overlapping detections.

6. **Tiny example (hand-simulated)**  
   Input 448×448 → divide into 7×7 grid → each cell predicts 2 boxes (x,y,w,h,confidence) + 20 class probs → 7×7×30 tensor → NMS → final detections. Processes at 45 FPS.

7. **Time & Space Complexity**  
   - Time: O(S²·B·C) where S is grid size, B is boxes per cell, C is classes (very fast: real-time).  
   - Space: O(S²·(B·5+C)) for grid predictions (compact representation).

8. **Strengths**  
- Extremely fast real-time detection.
- Sees entire image context, fewer false positives on background.

9. **Weaknesses / limitations**  
- Struggles with small objects and objects in groups.
- Limited to fixed number of detections per grid cell.

10. **Compare with alternatives**  
    Alternatives: YOLOv2/v3/v4/v5, SSD, Faster R-CNN, RetinaNet

11. **30-second explanation (your own words)**  
    Performs object detection in a single forward pass by dividing image into grid and predicting boxes and classes directly, achieving real-time speed with end-to-end learning.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
