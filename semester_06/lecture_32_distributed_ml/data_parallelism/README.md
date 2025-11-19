# Data Parallelism

1. **Name of Algorithm**  
   Data Parallelism

2. **What problem does it solve? (1 sentence)**  
   Distributes training data across multiple workers, each training a copy of the model on different data shards, then synchronizes model updates to scale training horizontally.

3. **Intuition (plain-language explanation)**  
   Like dividing a large book among multiple readers: each person reads a different chapter (data shard), learns from it, then everyone shares what they learned to create a combined understanding (model).

4. **Inputs & Outputs**  
   - Input: Training dataset, model architecture, number of workers, synchronization method (AllReduce, Parameter Server).  
   - Output: Trained model with parameters synchronized across all workers.

5. **Step-by-step description (5–10 lines max)**  
1. Split training data into shards (one per worker).
2. Each worker loads full model architecture and its data shard.
3. Each worker performs forward pass on its data batch, computes loss.
4. Each worker performs backward pass, computes gradients for its batch.
5. Synchronize gradients: use AllReduce or Parameter Server to aggregate gradients across workers.
6. Each worker updates model parameters using aggregated gradients (typically averaged).
7. Repeat for next batch: each worker processes next batch from its shard.
8. Continue until all workers have processed their data shards.

6. **Tiny example (hand-simulated)**  
   Image classification: 1M images, 4 workers → worker 0 gets images 0-250K, worker 1 gets 250K-500K, etc. → each trains same ResNet model → gradients aggregated every batch → after epoch, all workers have same updated model.

7. **Time & Space Complexity**  
   - Time: O(T/P + C) where T is sequential training time, P is number of workers, C is communication overhead (near-linear speedup if C << T/P).  
   - Space: O(M + D/P) per worker where M is model size, D is dataset size (each worker stores full model, 1/P of data).

8. **Strengths**  
- Scales training with number of workers (near-linear speedup).
- Simple to implement and widely supported.

9. **Weaknesses / limitations**  
- Requires storing full model on each worker (memory constraint).
- Communication overhead can limit speedup for large models.

10. **Compare with alternatives**  
    Alternatives: Model Parallelism, Pipeline Parallelism, Hybrid Parallelism, Gradient Accumulation

11. **30-second explanation (your own words)**  
    Distributes data across workers, each training a full model copy on different shards, then synchronizes updates to achieve parallel training with near-linear speedup.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
