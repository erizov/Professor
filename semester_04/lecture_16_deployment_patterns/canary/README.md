# Canary Deployment

1. **Name of Algorithm**  
   Canary Deployment

2. **What problem does it solve? (1 sentence)**  
   Gradually rolls out new version to a small subset of users, monitors for issues, then expands to full deployment if successful.

3. **Intuition (plain-language explanation)**  
   Like canaries in coal mines: test new version on small group first (canary), if safe, expand to everyone; if problems, stop and rollback.

4. **Inputs & Outputs**  
   - Input: New application version, traffic routing rules, monitoring tools, user segmentation.  
   - Output: Gradually deployed new version with risk mitigation and monitoring.

5. **Step-by-step description (5–10 lines max)**  
1. Deploy new version alongside current version.
2. Route small percentage of traffic (e.g., 5%) to new version.
3. Monitor metrics (error rates, latency, business metrics).
4. If metrics acceptable, gradually increase traffic percentage (10%, 25%, 50%, 100%).
5. If issues detected, route traffic back to old version.
6. Complete rollout or rollback based on monitoring.

6. **Tiny example (hand-simulated)**  
   Deploy v2.0, route 5% of users to it. Monitor: if error rate < 1%, increase to 25%, then 50%, then 100%. If errors spike, revert to v1.0.

7. **Time & Space Complexity**  
   - Time: O(n) where n is number of rollout stages (gradual process).  
   - Space: O(n) for maintaining both versions during transition.

8. **Strengths**  
- Low-risk gradual rollout.
- Early detection of issues with minimal impact.

9. **Weaknesses / limitations**  
- Requires traffic routing infrastructure.
- Slower than blue-green deployment.

10. **Compare with alternatives**  
    Alternatives: Blue-Green Deployment, Rolling Deployment, Feature Flags

11. **30-second explanation (your own words)**  
    Gradually exposes new version to increasing traffic percentages while monitoring for issues, enabling safe, risk-mitigated deployments.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
