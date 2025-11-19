# R-CNN (Region-based CNN)

1. **Name of Algorithm**  
   R-CNN (Region-based CNN)

2. **What problem does it solve? (1 sentence)**  
   Detects objects by first generating region proposals, then classifying each region with a CNN, combining selective search with deep learning.

3. **Intuition (plain-language explanation)**  
   Like a security guard checking suspicious areas: first identify potential regions (selective search), then examine each region carefully (CNN classification) to confirm if it contains an object.

4. **Inputs & Outputs**  
   - Input: Input image, region proposal algorithm (selective search), pre-trained CNN.  
   - Output: Bounding boxes with class labels and confidence scores for detected objects.

5. **Step-by-step description (5–10 lines max)**  
1. Generate ~2000 region proposals using selective search (bottom-up segmentation).
2. Warp each region proposal to fixed size (e.g., 227×227).
3. Extract features from each warped region using pre-trained CNN (e.g., AlexNet).
4. Train SVM classifiers for each object class on extracted features.
5. Apply bounding box regression to refine proposal coordinates.
6. Apply non-maximum suppression to remove duplicate detections.

6. **Tiny example (hand-simulated)**  
   Image → selective search finds 2000 regions → warp each to 227×227 → CNN extracts 4096-dim features → SVM classifies (person, car, dog) → bounding box regression → NMS → final detections.

7. **Time & Space Complexity**  
   - Time: O(n·m) where n is number of proposals (~2000), m is CNN forward pass time (slow: ~47s per image).  
   - Space: O(n·d) for n proposals with d-dimensional features (high memory usage).

8. **Strengths**  
- First successful application of CNNs to object detection.
- Achieves good accuracy on PASCAL VOC dataset.

9. **Weaknesses / limitations**  
- Very slow due to processing each proposal separately.
- High memory usage and training complexity.

10. **Compare with alternatives**  
    Alternatives: Fast R-CNN, Faster R-CNN, YOLO, SSD

11. **30-second explanation (your own words)**  
    Uses region proposals with CNN-based classification to detect objects, pioneering deep learning for object detection but suffering from slow inference speed.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
