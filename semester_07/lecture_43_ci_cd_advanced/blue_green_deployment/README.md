# Blue-Green Deployment

1. **Name of Algorithm**  
   Blue-Green Deployment

2. **What problem does it solve? (1 sentence)**  
   Maintains two identical production environments (blue and green) and switches traffic between them during deployments, enabling zero-downtime releases with instant rollback capability.

3. **Intuition (plain-language explanation)**  
   Like having two identical restaurants: you update the green one while blue serves customers, then switch all customers to green - if something's wrong, instantly switch back to blue (zero downtime, instant rollback).

4. **Inputs & Outputs**  
   - Input: New application version, blue environment (current production), green environment (new version), load balancer configuration.  
   - Output: Deployed new version with zero downtime, ability to instantly rollback, two identical environments maintained.

5. **Step-by-step description (5–10 lines max)**  
1. Maintain blue environment: keep current production version running and serving all traffic.
2. Prepare green environment: set up identical infrastructure and deploy new version to green.
3. Deploy to green: install new version in green environment without affecting blue.
4. Test green: run smoke tests and validation checks on green environment.
5. Switch traffic: update load balancer to route all traffic from blue to green.
6. Monitor: observe green environment for errors, performance issues, or anomalies.
7. Rollback (if needed): if issues detected, instantly switch traffic back to blue.
8. Cleanup: after successful deployment, keep green as new blue, decommission old blue.

6. **Tiny example (hand-simulated)**  
   Blue (v1) serving 100% traffic → deploy v2 to green → test green → switch load balancer: 100% traffic to green (v2) → monitor → if OK, keep green; if issues, switch back to blue (v1) instantly → zero downtime, instant rollback.

7. **Time & Space Complexity**  
   - Time: O(D + S) where D is deployment time to green, S is switch time (typically minutes for deployment, seconds for switch).  
   - Space: O(2·E) where E is environment size (requires two full production environments simultaneously).

8. **Strengths**  
- Zero downtime: seamless switch between environments.
- Instant rollback: can revert in seconds by switching traffic.
- Safe testing: can test new version in production-like environment before switching.

9. **Weaknesses / limitations**  
- Resource overhead: requires maintaining two full production environments.
- Cost: doubles infrastructure costs during deployment.
- Database complexity: requires careful handling of database migrations and state.

10. **Compare with alternatives**  
    Alternatives: Canary Deployment, Rolling Deployment, Big Bang Deployment, A/B Testing

11. **30-second explanation (your own words)**  
    Maintains two identical production environments and switches traffic between them during deployments, enabling zero-downtime releases with instant rollback capability.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
