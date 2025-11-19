# Federated Learning

1. **Name of Algorithm**  
   Federated Learning

2. **What problem does it solve? (1 sentence)**  
   Trains machine learning models across decentralized devices (phones, edge devices) without centralizing raw data, preserving privacy while enabling collaborative learning.

3. **Intuition (plain-language explanation)**  
   Like a study group where everyone learns from their own notes (local data) without sharing the notes themselves - only sharing what they learned (model updates), so privacy is preserved while everyone benefits from collective knowledge.

4. **Inputs & Outputs**  
   - Input: Local datasets on distributed devices, initial global model, aggregation server, privacy parameters.  
   - Output: Trained global model without exposing raw training data, updated local models on devices.

5. **Step-by-step description (5–10 lines max)**  
1. Server initializes global model and distributes to participating devices.
2. Each device trains model locally on its private data for several epochs.
3. Each device computes model updates (gradients or updated weights).
4. Devices send encrypted/compressed updates to server (not raw data).
5. Server aggregates updates from multiple devices (federated averaging: weighted average by data size).
6. Server updates global model with aggregated updates.
7. Server distributes updated global model to devices.
8. Repeat for multiple rounds until convergence.

6. **Tiny example (hand-simulated)**  
   Mobile keyboard: 1000 phones each have local typing data → each trains language model locally → send model updates (not text) to server → server averages updates → distributes improved model → phones get better predictions without sharing personal text.

7. **Time & Space Complexity**  
   - Time: O(R·(E·T_local + C)) where R is rounds, E is local epochs, T_local is local training time, C is communication cost (depends on network).  
   - Space: O(M) per device for model, O(D_local) for local data, O(M·N) on server for aggregating N device updates.

8. **Strengths**  
- Preserves data privacy (raw data never leaves devices).
- Enables training on sensitive or distributed data.

9. **Weaknesses / limitations**  
- Communication overhead and device heterogeneity challenges.
- May require differential privacy or secure aggregation for strong privacy guarantees.

10. **Compare with alternatives**  
    Alternatives: Centralized Training, Split Learning, Secure Multi-Party Computation, Federated Averaging (FedAvg)

11. **30-second explanation (your own words)**  
    Trains models across decentralized devices by aggregating local updates without centralizing raw data, enabling privacy-preserving collaborative learning.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
