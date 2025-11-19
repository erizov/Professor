# LLM Distillation

1. **Name of Algorithm**  
   LLM Distillation

2. **What problem does it solve? (1 sentence)**  
   Transfers knowledge from large, powerful teacher LLM to smaller, faster student LLM by training student to mimic teacher's outputs, enabling deployment of compact models with retained performance.

3. **Intuition (plain-language explanation)**  
   Like a master teaching an apprentice: the large teacher model (master) has learned complex patterns, and the small student model (apprentice) learns by mimicking the teacher's responses - the student becomes almost as good but much smaller and faster.

4. **Inputs & Outputs**  
   - Input: Large teacher LLM, small student LLM architecture, unlabeled data, distillation temperature, loss weights.  
   - Output: Distilled student LLM with reduced size but retained performance.

5. **Step-by-step description (5–10 lines max)**  
1. Prepare teacher: load or use large pre-trained teacher LLM (GPT-4, Claude, etc.).
2. Initialize student: create smaller student model (fewer layers, smaller dimensions).
3. Generate teacher outputs: run teacher on unlabeled data to get soft predictions (probability distributions over tokens).
4. Set temperature: use temperature scaling (T > 1) to soften teacher's probability distribution, revealing more information.
5. Train student: minimize distillation loss (KL divergence between teacher and student distributions) plus task loss.
6. Use soft targets: student learns from teacher's soft probabilities rather than hard labels.
7. Iterate: continue training until student approximates teacher's behavior.
8. Deploy student: use smaller, faster student model for inference.

6. **Tiny example (hand-simulated)**  
   LLM distillation: teacher GPT-4 (1T params) → student GPT-2 (124M params) → teacher generates soft predictions on 1M examples → student learns to match teacher's probability distributions → student achieves 80% of teacher's performance with 1000x fewer parameters → 10x faster inference.

7. **Time & Space Complexity**  
   - Time: O(E·(T_teacher + T_student)) where E is epochs, T_teacher is teacher inference time, T_student is student training time.  
   - Space: O(M_teacher + M_student) during training, O(M_student) for deployed student (much smaller than teacher).

8. **Strengths**  
- Size reduction: enables deployment of much smaller models.
- Speed improvement: smaller models have faster inference.
- Cost effective: reduces compute and memory requirements.

9. **Weaknesses / limitations**  
- Performance gap: student may not fully match teacher's capabilities.
- Requires teacher: needs access to large teacher model for training.
- Training overhead: requires generating teacher outputs on large dataset.

10. **Compare with alternatives**  
    Alternatives: Direct Training, Pruning, Quantization, Knowledge Distillation

11. **30-second explanation (your own words)**  
    Transfers knowledge from large teacher LLM to smaller student LLM by training student to mimic teacher's outputs, enabling deployment of compact models with retained performance.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
