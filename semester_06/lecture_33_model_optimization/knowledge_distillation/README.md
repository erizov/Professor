# Knowledge Distillation

1. **Name of Algorithm**  
   Knowledge Distillation

2. **What problem does it solve? (1 sentence)**  
   Transfers knowledge from a large, accurate teacher model to a smaller, faster student model by training the student to mimic the teacher's predictions, enabling deployment of compact models without significant accuracy loss.

3. **Intuition (plain-language explanation)**  
   Like a student learning from a master: the large teacher model (master) has learned subtle patterns, and the small student model learns to make similar predictions by mimicking the teacher's 'soft' predictions (probabilities) rather than just hard labels.

4. **Inputs & Outputs**  
   - Input: Large teacher model (pre-trained), small student model architecture, training data, temperature parameter, distillation loss weight.  
   - Output: Trained student model that approximates teacher's performance with smaller size.

5. **Step-by-step description (5–10 lines max)**  
1. Train or load large teacher model on training data.
2. Initialize small student model (fewer parameters, simpler architecture).
3. Generate teacher predictions: run teacher on training data to get soft labels (probability distributions).
4. Train student with combined loss: distillation loss (match teacher's soft predictions) + task loss (match ground truth labels).
5. Distillation loss: KL divergence between teacher and student probability distributions (scaled by temperature T).
6. Task loss: cross-entropy between student predictions and true labels.
7. Total loss: α·L_distill + (1-α)·L_task where α balances the two objectives.
8. Train student until it learns to approximate teacher's behavior.

6. **Tiny example (hand-simulated)**  
   Image classification: teacher ResNet-50 (25M params, 95% accuracy) → student MobileNet (3M params) → teacher predicts [0.7 cat, 0.2 dog, 0.1 bird] → student learns to predict similar distribution → student achieves 93% accuracy with 8x fewer parameters.

7. **Time & Space Complexity**  
   - Time: O(E·(T_teacher + T_student)) where E is epochs, T_teacher is teacher inference time, T_student is student training time.  
   - Space: O(M_teacher + M_student) for storing both models during training, O(M_student) for deployed student.

8. **Strengths**  
- Enables deployment of compact, fast models.
- Student can learn subtle patterns from teacher's soft predictions.

9. **Weaknesses / limitations**  
- Requires training and storing teacher model first.
- Student may not fully capture teacher's knowledge.

10. **Compare with alternatives**  
    Alternatives: Pruning, Quantization, Neural Architecture Search, Direct Training

11. **30-second explanation (your own words)**  
    Transfers knowledge from large teacher to small student by training student to mimic teacher's soft predictions, enabling compact models that retain much of teacher's accuracy.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
