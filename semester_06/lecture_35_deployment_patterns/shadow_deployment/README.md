# Shadow Deployment

1. **Name of Algorithm**  
   Shadow Deployment

2. **What problem does it solve? (1 sentence)**  
   Deploys new ML model alongside production model, running inference on both but only using production model's predictions, allowing validation of new model on real traffic without risk.

3. **Intuition (plain-language explanation)**  
   Like a shadow following you: the new model runs in parallel with production, processing the same inputs and making predictions, but you only use the production model's output. Compare them later to see if the new model is ready, with zero risk to users.

4. **Inputs & Outputs**  
   - Input: New model version, production model, traffic router, logging/monitoring system.  
   - Output: Shadow model running in parallel, predictions logged for comparison, no impact on live users.

5. **Step-by-step description (5–10 lines max)**  
1. Deploy new model (shadow) alongside production model.
2. Route all traffic to production model: users receive predictions from production only.
3. Duplicate traffic to shadow model: send same inputs to shadow model in parallel.
4. Run inference on both: production serves users, shadow processes silently.
5. Log predictions: record predictions from both models for comparison.
6. Compare performance: analyze accuracy, latency, business metrics between models.
7. Validate shadow model: ensure it performs as well or better than production.
8. If validated: promote shadow to production using blue-green or canary deployment.
9. If issues found: fix model, redeploy as shadow, repeat validation.

6. **Tiny example (hand-simulated)**  
   Fraud detection: production model (v1.0) serving users → deploy v2.0 as shadow → all requests go to v1.0 (users see v1.0 predictions) → v2.0 processes same requests silently → compare: v2.0 has 1% higher accuracy, similar latency → promote v2.0 to production via canary.

7. **Time & Space Complexity**  
   - Time: O(2·I) where I is inference time (running two models in parallel), O(C) for comparison analysis where C is comparison time.  
   - Space: O(2·M) for running two models, O(N·P) for logging predictions where N is number of requests, P is prediction size.

8. **Strengths**  
- Zero risk: new model doesn't affect users, only processes in background.
- Real-world validation: tests model on actual production traffic and data distribution.
- Comprehensive comparison: can compare all aspects (accuracy, latency, edge cases).

9. **Weaknesses / limitations**  
- Resource intensive: requires running two models (double compute cost).
- No immediate feedback: can't observe actual user impact until promotion.

10. **Compare with alternatives**  
    Alternatives: Blue-Green Deployment, Canary Deployment, A/B Testing, Offline Evaluation

11. **30-second explanation (your own words)**  
    Deploys new ML model in parallel with production, processing real traffic silently while only serving production predictions, enabling risk-free validation on real-world data before promotion.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
