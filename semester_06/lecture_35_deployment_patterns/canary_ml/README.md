# Canary ML Deployment

1. **Name of Algorithm**  
   Canary ML Deployment

2. **What problem does it solve? (1 sentence)**  
   Gradually rolls out new ML model versions to a small subset of users (canary), monitors performance, and incrementally increases traffic if successful, reducing risk of deploying faulty models to all users.

3. **Intuition (plain-language explanation)**  
   Like a canary in a coal mine: test the new model on a small group first (canary) - if it works well, gradually give it to more users. If something's wrong, only a few users are affected, not everyone.

4. **Inputs & Outputs**  
   - Input: New model version, current production model, traffic routing system, monitoring metrics, rollout strategy (percentage increments).  
   - Output: Gradually deployed model with increasing traffic percentage, with ability to halt or rollback at any stage.

5. **Step-by-step description (5–10 lines max)**  
1. Deploy new model alongside current production model.
2. Route small percentage of traffic to new model (canary): start with 1-5% of users.
3. Monitor canary performance: track accuracy, latency, error rates, business metrics.
4. Compare canary vs production: ensure new model performs as well or better.
5. If metrics are good: gradually increase traffic (5% → 10% → 25% → 50% → 100%).
6. At each stage: monitor and validate before increasing further.
7. If issues detected: halt rollout, route traffic back to production, investigate.
8. If successful: complete rollout to 100%, retire old model.

6. **Tiny example (hand-simulated)**  
   Recommendation model: deploy v2.0 → route 5% traffic to canary → monitor: click-through rate +2% → increase to 10% → monitor: still good → increase to 25% → error rate spikes → halt, rollback to v1.0 → fix issue → redeploy.

7. **Time & Space Complexity**  
   - Time: O(D + R·M) where D is deployment time, R is rollout stages, M is monitoring time per stage (gradual rollout over hours/days).  
   - Space: O(M + C) where M is model size, C is canary infrastructure (typically small percentage of full production).

8. **Strengths**  
- Low risk: only small percentage of users affected if issues occur.
- Gradual validation: test model at scale incrementally.
- Easy rollback: can halt at any stage.

9. **Weaknesses / limitations**  
- Slower deployment: takes time to reach 100% traffic.
- Requires traffic routing infrastructure and monitoring.

10. **Compare with alternatives**  
    Alternatives: Blue-Green Deployment, Rolling Deployment, Shadow Deployment, A/B Testing

11. **30-second explanation (your own words)**  
    Gradually rolls out new ML models to increasing percentages of users, monitoring performance at each stage to safely validate and deploy with minimal risk.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
