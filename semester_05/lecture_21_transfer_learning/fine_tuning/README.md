# Fine-Tuning

1. **Name of Algorithm**  
   Fine-Tuning

2. **What problem does it solve? (1 sentence)**  
   Adapts a pre-trained model to a new task by training some or all layers on target data, balancing transfer learning with task-specific adaptation.

3. **Intuition (plain-language explanation)**  
   Like adjusting a pre-tuned piano: start with good base tuning (pre-trained weights), then make small adjustments (fine-tune) to match your specific music (target task).

4. **Inputs & Outputs**  
   - Input: Pre-trained model, target dataset, learning rate, layers to fine-tune.  
   - Output: Adapted model optimized for target task with improved performance.

5. **Step-by-step description (5–10 lines max)**  
1. Load pre-trained model weights.
2. Optionally replace final layers for new task (e.g., different number of classes).
3. Freeze early layers, unfreeze later layers (or use differential learning rates).
4. Train on target dataset with lower learning rate than training from scratch.
5. Optionally unfreeze more layers and continue training.
6. Validate and adjust hyperparameters.

6. **Tiny example (hand-simulated)**  
   Pre-trained ResNet on ImageNet → replace last layer for 10 classes → freeze first 100 layers → fine-tune last layers on medical images with lr=0.001 → achieve 95% accuracy.

7. **Time & Space Complexity**  
   - Time: O(n·e·l) for n samples, e epochs, l layers (faster than full training).  
   - Space: O(m) for model weights plus O(b) for batch data during training.

8. **Strengths**  
- Better performance than feature extraction alone.
- More efficient than training from scratch.

9. **Weaknesses / limitations**  
- Requires more data and computation than feature extraction.
- Risk of overfitting with small datasets.

10. **Compare with alternatives**  
    Alternatives: Feature Extraction, Full Training from Scratch, Progressive Unfreezing

11. **30-second explanation (your own words)**  
    Adapts pre-trained models to new tasks by selectively training layers, combining transfer learning benefits with task-specific optimization.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
