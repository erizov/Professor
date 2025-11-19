# Parameter Server

1. **Name of Algorithm**  
   Parameter Server

2. **What problem does it solve? (1 sentence)**  
   Centralizes model parameters on server nodes while workers compute gradients on data shards, enabling asynchronous or synchronous distributed training with flexible communication patterns.

3. **Intuition (plain-language explanation)**  
   Like a central library: workers (students) take data home, compute what they learned (gradients), send updates to the library (server), which updates the master book (model parameters) that everyone can read from.

4. **Inputs & Outputs**  
   - Input: Model parameters, worker nodes with data shards, server nodes, synchronization strategy (sync/async).  
   - Output: Updated model parameters on server, synchronized to workers.

5. **Step-by-step description (5–10 lines max)**  
1. Initialize: server stores global model parameters, workers pull initial parameters.
2. Each worker pulls current parameters from server.
3. Each worker computes gradients on its local data batch.
4. Workers send gradients to server (asynchronous: send immediately, synchronous: wait for all).
5. Server aggregates gradients: sum or average from all workers.
6. Server updates global parameters using aggregated gradients.
7. Server pushes updated parameters to workers (or workers pull on next iteration).
8. Repeat: workers pull updated parameters, compute new gradients, send to server.

6. **Tiny example (hand-simulated)**  
   4 workers, 1 server: server has global model → workers pull model → worker 0 computes gradients on batch 0, worker 1 on batch 1, etc. → workers send gradients to server → server averages: (grad0 + grad1 + grad2 + grad3) / 4 → server updates model → workers pull updated model.

7. **Time & Space Complexity**  
   - Time: O(T/P + C) where T is sequential time, P is workers, C is server communication (async: O(T/P), sync: O(T/P + max_worker_time)).  
   - Space: O(M) on server for global parameters, O(M) per worker for local copy, O(G) for gradients where G is gradient size.

8. **Strengths**  
- Flexible: supports both synchronous and asynchronous updates.
- Scalable: can add more workers without changing server architecture.

9. **Weaknesses / limitations**  
- Server can become bottleneck for large models.
- Asynchronous updates may cause staleness issues.

10. **Compare with alternatives**  
    Alternatives: AllReduce, Ring AllReduce, Gossip-based Updates, Distributed Parameter Server

11. **30-second explanation (your own words)**  
    Centralizes model parameters on server nodes while workers compute gradients locally, enabling flexible synchronous or asynchronous distributed training with centralized parameter management.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
