# Meta-Learning (Learning to Learn)

1. **Name of Algorithm**  
   Meta-Learning (Learning to Learn)

2. **What problem does it solve? (1 sentence)**  
   Trains models to learn how to learn, enabling them to quickly adapt to new tasks with minimal data by leveraging experience from learning many previous tasks.

3. **Intuition (plain-language explanation)**  
   Like learning study techniques: Meta-Learning is like learning how to study effectively - once you know good study techniques (meta-knowledge), you can quickly learn any new subject - meta-learning does this for AI: it learns general learning strategies from many tasks, then uses those strategies to quickly learn new tasks with little data.

4. **Inputs & Outputs**  
   - Input: Multiple training tasks, few examples per task, meta-learning algorithm, adaptation mechanism.  
   - Output: Meta-learned model, fast adaptation, learning strategies, few-shot capability, efficient learner.

5. **Step-by-step description (5–10 lines max)**  
1. Sample tasks: sample multiple tasks from task distribution.
2. Split: split each task into support (training) and query (test) sets.
3. Train: train model on support set of each task.
4. Test: test on query set to compute loss.
5. Meta-update: update meta-parameters based on performance across tasks.
6. Learn strategy: learn general learning strategy from many tasks.
7. New task: receive new task with few examples.
8. Adapt: quickly adapt using learned strategy.
9. Predict: make predictions on new task.
10. Iterate: iterate meta-learning to improve strategy.

6. **Tiny example (hand-simulated)**  
   Meta-Learning: tasks: 100 different classification tasks → learn: learn general learning strategy → new task: classify 5 types of birds with 1 example each → adapt: use learned strategy to adapt quickly → predict: classify new bird images → result: 90% accuracy with 5 examples → Meta-Learning successful.

7. **Time & Space Complexity**  
   - Time: O(t·(n + a)) where t is number of tasks, n is training time per task, a is adaptation time (meta-training phase).  
   - Space: O(m + s) where m is model size, s is strategy storage (meta-parameters).

8. **Strengths**  
- Fast adaptation: enables rapid adaptation to new tasks.
- Data efficiency: learns from few examples using prior experience.
- Generalization: learns generalizable learning strategies.

9. **Weaknesses / limitations**  
- Pre-training: requires extensive pre-training on many tasks.
- Task distribution: performance depends on similarity of new tasks to training tasks.
- Complexity: meta-learning algorithms can be complex to design and train.

10. **Compare with alternatives**  
    Alternatives: Transfer Learning, Few-Shot Learning, Multi-Task Learning, Pre-training

11. **30-second explanation (your own words)**  
    Trains models to learn how to learn, enabling them to quickly adapt to new tasks with minimal data by leveraging experience from learning many previous tasks.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
