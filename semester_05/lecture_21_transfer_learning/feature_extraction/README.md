# Feature Extraction

1. **Name of Algorithm**  
   Feature Extraction

2. **What problem does it solve? (1 sentence)**  
   Uses pre-trained neural network layers to extract meaningful features from new data, leveraging learned representations without retraining the entire model.

3. **Intuition (plain-language explanation)**  
   Like using a professional photographer's camera settings: apply their learned expertise (pre-trained layers) to capture good features from your photos (new data) without learning photography from scratch.

4. **Inputs & Outputs**  
   - Input: Pre-trained model (typically CNN), new dataset, feature extraction layer configuration.  
   - Output: Feature vectors representing high-level patterns in the input data.

5. **Step-by-step description (5–10 lines max)**  
1. Load pre-trained model (e.g., ImageNet-trained ResNet).
2. Remove final classification layers.
3. Freeze all layers (set trainable=False).
4. Pass new data through frozen layers to extract features.
5. Use extracted features as input to new classifier or downstream task.
6. Optionally fine-tune some layers if needed.

6. **Tiny example (hand-simulated)**  
   Pre-trained ResNet on ImageNet → remove last layer → extract 2048-dim features from cat images → train simple classifier on features → achieve good accuracy with little data.

7. **Time & Space Complexity**  
   - Time: O(n·d) for n samples with d-dimensional features (faster than training from scratch).  
   - Space: O(m) for pre-trained model weights plus O(n·d) for extracted features.

8. **Strengths**  
- Leverages powerful pre-trained representations.
- Requires less data and training time than training from scratch.

9. **Weaknesses / limitations**  
- Features may not be optimal for target task.
- Limited to tasks similar to pre-training domain.

10. **Compare with alternatives**  
    Alternatives: Fine-tuning, End-to-End Training, Domain Adaptation

11. **30-second explanation (your own words)**  
Extracts high-level features using frozen pre-trained model layers, enabling effective learning on new tasks with limited data by leveraging transferable representations.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
