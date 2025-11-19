# Blue-Green Deployment

1. **Name of Algorithm**  
   Blue-Green Deployment

2. **What problem does it solve? (1 sentence)**  
   Deploys new version alongside current version, then switches traffic to new version, enabling zero-downtime deployments and instant rollback.

3. **Intuition (plain-language explanation)**  
   Like having two identical theaters: run show in blue theater, prepare new show in green theater, then switch audience to green when ready.

4. **Inputs & Outputs**  
   - Input: Current production environment (blue), new application version, traffic routing configuration.  
   - Output: Deployed new version with zero downtime and rollback capability.

5. **Step-by-step description (5–10 lines max)**  
1. Deploy new version to green environment (parallel to blue).
2. Run smoke tests on green environment.
3. Switch traffic routing from blue to green.
4. Monitor green environment for issues.
5. If problems detected, route traffic back to blue (instant rollback).
6. Keep blue as backup or decommission after validation period.

6. **Tiny example (hand-simulated)**  
   Deploy v2.0 to green servers while v1.0 runs on blue. Test green, then update load balancer to route traffic to green. If errors occur, revert to blue.

7. **Time & Space Complexity**  
   - Time: O(1) for traffic switch (instantaneous).  
   - Space: O(2n) for maintaining two full environments simultaneously.

8. **Strengths**  
- Zero-downtime deployments.
- Instant rollback capability.

9. **Weaknesses / limitations**  
- Requires double infrastructure capacity.
- Database migration complexity.

10. **Compare with alternatives**  
    Alternatives: Canary Deployment, Rolling Deployment, Recreate Deployment

11. **30-second explanation (your own words)**  
    Maintains two identical production environments (blue and green), deploying new version to one while the other serves traffic, then switching instantly.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
