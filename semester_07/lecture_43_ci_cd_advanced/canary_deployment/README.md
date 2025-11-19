# Canary Deployment

1. **Name of Algorithm**  
   Canary Deployment

2. **What problem does it solve? (1 sentence)**  
   Gradually rolls out new version to a small subset of users before full deployment, enabling risk mitigation and early detection of issues with minimal impact.

3. **Intuition (plain-language explanation)**  
   Like testing water quality with a canary in a mine: deploy new version to 5% of users (the canary) - if they're fine, gradually increase to 100%; if issues appear, stop and rollback (minimal impact, early detection).

4. **Inputs & Outputs**  
   - Input: New application version, current production environment, traffic routing configuration, monitoring tools.  
   - Output: Gradually deployed new version, risk mitigation, ability to stop/rollback at any stage.

5. **Step-by-step description (5–10 lines max)**  
1. Deploy to canary: deploy new version alongside current version in production.
2. Route small traffic: direct small percentage (e.g., 5%) of traffic to new version.
3. Monitor metrics: track error rates, latency, performance, user feedback for canary.
4. Compare: compare canary metrics with current version metrics.
5. Gradual increase: if canary performs well, gradually increase traffic (5% → 25% → 50% → 100%).
6. Stop/rollback: if issues detected at any stage, stop rollout or rollback immediately.
7. Complete rollout: if all stages successful, route 100% traffic to new version.
8. Cleanup: remove old version after successful full deployment.

6. **Tiny example (hand-simulated)**  
   Deploy v2 alongside v1 → route 5% traffic to v2 (canary) → monitor: v2 has 0.1% error rate (same as v1) → increase to 25% → still good → 50% → 100% → v2 fully deployed, v1 removed → gradual, safe rollout.

7. **Time & Space Complexity**  
   - Time: O(D + M·S) where D is deployment time, M is monitoring duration per stage, S is number of stages (typically hours to days for full rollout).  
   - Space: O(E + δ) where E is environment size, δ is overhead for running both versions simultaneously (less than blue-green).

8. **Strengths**  
- Risk mitigation: limits impact of issues to small user subset.
- Real-world testing: tests new version with actual production traffic.
- Gradual rollout: can stop or adjust at any stage based on metrics.

9. **Weaknesses / limitations**  
- Complexity: requires sophisticated traffic routing and monitoring.
- Time: gradual rollout takes longer than instant switch.
- Monitoring overhead: requires comprehensive metrics and alerting.

10. **Compare with alternatives**  
    Alternatives: Blue-Green Deployment, Rolling Deployment, A/B Testing, Feature Flags

11. **30-second explanation (your own words)**  
    Gradually rolls out new version to a small subset of users before full deployment, enabling risk mitigation and early detection of issues with minimal impact.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
