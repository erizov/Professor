# Deployment Strategies

1. **Name of Algorithm**  
   Deployment Strategies

2. **What problem does it solve? (1 sentence)**  
   Defines approaches for releasing new software versions to production with minimal downtime and risk, enabling safe, controlled rollouts of application updates.

3. **Intuition (plain-language explanation)**  
   Like different ways to update a restaurant: you could close and renovate (big bang), update one section at a time (rolling), have two restaurants and switch (blue-green), or test with a few customers first (canary) - each strategy balances risk, downtime, and complexity differently.

4. **Inputs & Outputs**  
   - Input: New application version, current production environment, deployment strategy type, rollback plan.  
   - Output: Deployed new version, zero or minimal downtime, ability to rollback if needed.

5. **Step-by-step description (5–10 lines max)**  
1. Choose strategy: select deployment approach (big bang, rolling, blue-green, canary, etc.).
2. Prepare new version: build and package new application version.
3. Execute deployment: apply chosen strategy to deploy new version.
4. Monitor: track deployment progress, application health, and user metrics.
5. Validate: verify new version is working correctly (health checks, smoke tests).
6. Complete rollout: finish deployment according to strategy (all instances, full traffic, etc.).
7. Rollback (if needed): revert to previous version if issues detected.
8. Cleanup: remove old versions and resources after successful deployment.

6. **Tiny example (hand-simulated)**  
   Blue-green deployment: prepare green environment with v2 → deploy v2 to green → switch load balancer from blue (v1) to green (v2) → all traffic now on v2 → monitor → if issues, switch back to blue → if OK, keep green, decommission blue.

7. **Time & Space Complexity**  
   - Time: O(D) where D is deployment time (varies by strategy: minutes to hours).  
   - Space: O(2·E) for blue-green (two environments), O(E) for rolling/canary where E is environment size.

8. **Strengths**  
- Risk mitigation: enables safe, controlled deployments.
- Zero downtime: many strategies allow updates without service interruption.
- Fast rollback: quick reversion if issues occur.

9. **Weaknesses / limitations**  
- Resource overhead: some strategies require additional infrastructure.
- Complexity: more complex strategies require more setup and management.
- Cost: maintaining multiple environments increases costs.

10. **Compare with alternatives**  
    Alternatives: Big Bang Deployment, Rolling Deployment, Blue-Green, Canary, A/B Testing

11. **30-second explanation (your own words)**  
    Defines approaches for releasing new software versions to production with minimal downtime and risk, enabling safe, controlled rollouts of application updates.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
