# Feature Flags

1. **Name of Algorithm**  
   Feature Flags

2. **What problem does it solve? (1 sentence)**  
   Enables runtime control of feature visibility and behavior without code deployment, allowing gradual feature rollouts, A/B testing, and instant feature toggling.

3. **Intuition (plain-language explanation)**  
   Like a light switch for features: deploy code with new feature (light installed) but keep it off (flag disabled) - when ready, flip the switch (enable flag) to turn on feature instantly, no deployment needed (like turning on a light without rewiring).

4. **Inputs & Outputs**  
   - Input: Feature flag configuration, application code with feature checks, flag management system, user/context data.  
   - Output: Runtime feature control, gradual rollouts, A/B test results, instant feature toggling.

5. **Step-by-step description (5–10 lines max)**  
1. Implement feature: develop feature code with feature flag checks (if flag enabled, show feature).
2. Deploy code: deploy feature code to production with flag disabled (feature hidden).
3. Configure flag: set up feature flag in management system (percentage rollout, user targeting, etc.).
4. Enable gradually: enable flag for small percentage (e.g., 10% of users).
5. Monitor: track feature usage, errors, performance metrics.
6. Increase rollout: if metrics positive, gradually increase percentage (10% → 50% → 100%).
7. A/B test (optional): compare feature variants by enabling different flags for different user groups.
8. Disable if needed: instantly disable feature by turning off flag (no code deployment required).
9. Remove flag: after feature stable, remove flag checks from code in next deployment.

6. **Tiny example (hand-simulated)**  
   Develop 'dark mode' feature → deploy with flag disabled → enable for 10% users → monitor: positive feedback, no errors → increase to 50% → 100% → feature fully rolled out → later, remove flag code.

7. **Time & Space Complexity**  
   - Time: O(1) for flag evaluation (constant time check), O(D) for deployment (one-time, feature can be toggled without redeployment).  
   - Space: O(F) where F is number of feature flags (minimal overhead per flag).

8. **Strengths**  
- Instant control: enable/disable features without deployment.
- Risk mitigation: gradual rollout reduces risk of issues.
- A/B testing: enables experimentation with different feature variants.

9. **Weaknesses / limitations**  
- Code complexity: requires feature flag checks throughout codebase.
- Technical debt: flags need cleanup after features are stable.
- Management overhead: requires flag management system and processes.

10. **Compare with alternatives**  
    Alternatives: Branch-based Deployments, Configuration-based Toggles, Canary Deployments, A/B Testing

11. **30-second explanation (your own words)**  

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
