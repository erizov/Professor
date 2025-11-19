# AllReduce

1. **Name of Algorithm**  
   AllReduce

2. **What problem does it solve? (1 sentence)**  
   Efficiently aggregates (sums, averages, etc.) tensors across multiple workers in distributed training, ensuring all workers receive the same aggregated result for synchronous gradient updates.

3. **Intuition (plain-language explanation)**  
   Like a team meeting where everyone shares their work and everyone leaves with the same summary: each worker computes gradients, they all share and combine them, then everyone gets the same averaged gradients to update their model.

4. **Inputs & Outputs**  
   - Input: Local tensors/gradients from each worker, reduction operation (sum, mean, max), communication topology.  
   - Output: Aggregated tensor (same value on all workers) ready for model update.

5. **Step-by-step description (5–10 lines max)**  
1. Each worker computes local gradients from its data shard.
2. Workers organize in communication topology (ring, tree, or mesh).
3. Perform reduction: combine tensors using specified operation (typically sum for gradients).
4. Ring AllReduce: workers pass data in ring, each accumulates partial sums, then distributes final result.
5. Tree AllReduce: reduce up tree (combine), then broadcast down tree (distribute).
6. All workers receive identical aggregated result.
7. Each worker updates model parameters using aggregated gradients.
8. Repeat for next iteration.

6. **Tiny example (hand-simulated)**  
   4 workers training neural network: worker 0 has gradient [0.1, 0.2], worker 1 has [0.2, 0.3], worker 2 has [0.1, 0.1], worker 3 has [0.2, 0.2] → AllReduce (sum) → all workers get [0.6, 0.8] → divide by 4 (average) → update model with [0.15, 0.2].

7. **Time & Space Complexity**  
   - Time: O(P·D) where P is number of workers, D is tensor size (communication cost depends on topology: ring O(P·D), tree O(log P·D)).  
   - Space: O(D) per worker for storing local and aggregated tensors.

8. **Strengths**  
- Efficient communication pattern for distributed training.
- Ensures all workers have identical model state (synchronous).

9. **Weaknesses / limitations**  
- Synchronous: slowest worker determines speed (straggler problem).
- Requires network bandwidth proportional to model size.

10. **Compare with alternatives**  
    Alternatives: Parameter Server, Asynchronous SGD, Gradient Compression, Horovod, NCCL

11. **30-second explanation (your own words)**  
    Efficiently aggregates tensors across distributed workers using optimized communication patterns, ensuring all workers receive identical aggregated results for synchronous model updates.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
