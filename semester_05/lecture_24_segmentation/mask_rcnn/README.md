# Mask R-CNN

1. **Name of Algorithm**  
   Mask R-CNN

2. **What problem does it solve? (1 sentence)**  
   Extends Faster R-CNN to simultaneously perform object detection, bounding box regression, and instance segmentation (pixel-level masks) in a unified framework.

3. **Intuition (plain-language explanation)**  
   Like a multi-tool: not only find objects (detection) and draw boxes (localization), but also precisely outline each object's shape (segmentation mask) in one pass.

4. **Inputs & Outputs**  
   - Input: Input images, region proposals (from RPN), feature maps.  
   - Output: Bounding boxes, class labels, confidence scores, and binary segmentation masks for each detected object.

5. **Step-by-step description (5–10 lines max)**  
1. Use Faster R-CNN backbone to generate region proposals via RPN.
2. Apply RoIAlign (instead of RoIPool) to extract fixed-size features from proposals.
3. Branch 1: Classify object and refine bounding box (as in Faster R-CNN).
4. Branch 2: Predict binary segmentation mask for each RoI using FCN head.
5. Train with multi-task loss: classification + box regression + mask prediction.
6. Apply non-maximum suppression and output detections with masks.

6. **Tiny example (hand-simulated)**  
   Image → RPN finds 1000 proposals → RoIAlign extracts 14×14 features → branch 1: class 'person' + box → branch 2: 28×28 binary mask → final: person at [x,y,w,h] with pixel mask.

7. **Time & Space Complexity**  
   - Time: O(n·m) where n is number of proposals, m is mask prediction time (slower than Faster R-CNN due to mask branch).  
   - Space: O(n·k²) for n proposals with k×k mask predictions (additional memory for masks).

8. **Strengths**  
- Unified framework for detection and segmentation.
- High-quality instance segmentation with precise masks.

9. **Weaknesses / limitations**  
- Slower than detection-only methods.
- Requires instance-level segmentation annotations for training.

10. **Compare with alternatives**  
    Alternatives: FCN, U-Net, YOLACT, SOLO

11. **30-second explanation (your own words)**  
    Extends Faster R-CNN with a mask prediction branch, enabling simultaneous object detection and instance segmentation in a unified end-to-end framework.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
