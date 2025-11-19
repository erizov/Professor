# Blue-Green ML Deployment

1. **Name of Algorithm**  
   Blue-Green ML Deployment

2. **What problem does it solve? (1 sentence)**  
   Deploys ML models using blue-green deployment pattern: maintains two identical production environments (blue and green), allowing instant rollback by switching traffic between environments, minimizing deployment risk.

3. **Intuition (plain-language explanation)**  
   Like having two identical restaurants: one (blue) serves customers now, while you prepare the other (green) with new menu. When ready, switch all customers to green - if something's wrong, instantly switch back to blue. No downtime, safe rollback.

4. **Inputs & Outputs**  
   - Input: New model version, blue environment (current production), green environment (new deployment), traffic router/load balancer.  
   - Output: Deployed model in green environment, with ability to instantly switch traffic or rollback to blue.

5. **Step-by-step description (5–10 lines max)**  
1. Maintain blue environment: current production model serving live traffic.
2. Deploy new model to green environment: identical infrastructure, new model version.
3. Validate green environment: test model performance, accuracy, latency on green (no live traffic yet).
4. Switch traffic: route all traffic from blue to green using load balancer or router.
5. Monitor green: track metrics (accuracy, latency, error rates) to ensure model performs well.
6. If issues detected: instantly switch traffic back to blue (rollback) - no downtime.
7. If successful: keep green as new production, blue becomes staging for next deployment.
8. Repeat: next deployment uses current green as new blue, deploy to new green.

6. **Tiny example (hand-simulated)**  
   Fraud detection model: blue (v1.0, 95% accuracy) serving 100% traffic → deploy v1.1 to green → validate: 96% accuracy → switch 100% traffic to green → monitor: error rate spikes → rollback to blue → investigate issue → fix → redeploy to green.

7. **Time & Space Complexity**  
   - Time: O(1) for traffic switching (instant), O(D) for deployment where D is deployment time (typically minutes).  
   - Space: O(2·M) for maintaining two environments where M is infrastructure cost per environment (double the resources).

8. **Strengths**  
- Zero-downtime deployments: seamless traffic switching.
- Instant rollback: switch back to previous version immediately if issues occur.
- Safe testing: validate new model in production-like environment before traffic switch.

9. **Weaknesses / limitations**  
- Resource intensive: requires maintaining two complete environments.
- Higher infrastructure costs: double the compute/storage resources.

10. **Compare with alternatives**  
    Alternatives: Canary Deployment, Rolling Deployment, Shadow Deployment, A/B Testing

11. **30-second explanation (your own words)**  
    Maintains two identical production environments (blue/green) for ML models, enabling instant traffic switching and rollback with zero downtime for safe deployments.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
