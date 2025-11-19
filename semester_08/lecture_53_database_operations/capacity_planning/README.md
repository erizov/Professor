# Database Capacity Planning

1. **Name of Algorithm**  
   Database Capacity Planning

2. **What problem does it solve? (1 sentence)**  
   Forecasts future database resource requirements (storage, compute, memory) based on growth trends and usage patterns, ensuring adequate capacity to meet future needs.

3. **Intuition (plain-language explanation)**  
Like planning for a growing family: capacity planning is like planning house size for a growing family - you analyze current usage (how much space you use now), growth trends (how fast the family is growing), and forecast future needs (how much space you'll need in 2 years) - then you plan resources (buy bigger house, add rooms) to ensure you have enough capacity before you run out.

4. **Inputs & Outputs**  
   - Input: Current usage metrics, growth trends, business projections, performance requirements, resource constraints.  
   - Output: Capacity forecasts, resource requirements, scaling plans, budget estimates.

5. **Step-by-step description (5–10 lines max)**  
1. Collect metrics: gather current usage data (storage, CPU, memory, I/O, connections).
2. Analyze trends: identify growth patterns and trends over time.
3. Project growth: forecast future growth based on historical data and business projections.
4. Calculate requirements: estimate future resource needs (storage, compute, memory).
5. Plan scaling: determine when and how to scale (add storage, upgrade hardware, add nodes).
6. Estimate costs: calculate costs for required resources.
7. Create timeline: establish timeline for capacity additions.
8. Monitor: continuously monitor usage and adjust forecasts.
9. Review: periodically review and update capacity plans.

6. **Tiny example (hand-simulated)**  
   Database capacity planning: current storage: 500GB, growth: 50GB/month → forecast: 1TB in 10 months → plan: add 1TB storage in 8 months → current CPU: 60% utilization, growth: 5%/month → forecast: 90% in 6 months → plan: upgrade CPU in 5 months → proactive capacity planning → avoid capacity issues.

7. **Time & Space Complexity**  
   - Time: O(m) where m is number of metrics to analyze (planning phase).  
   - Space: O(h) where h is historical data size (metrics storage).

8. **Strengths**  
- Proactive: prevents capacity issues before they occur.
- Cost optimization: enables budget planning and cost optimization.
- Performance: ensures adequate resources for performance requirements.

9. **Weaknesses / limitations**  
- Uncertainty: forecasts may be inaccurate due to unpredictable growth.
- Complexity: requires analysis of multiple metrics and trends.
- Over-provisioning: may lead to over-provisioning if forecasts are too high.

10. **Compare with alternatives**  
    Alternatives: Reactive Scaling, Auto-scaling, Cloud Elasticity, Resource Monitoring

11. **30-second explanation (your own words)**  
    Forecasts future database resource requirements (storage, compute, memory) based on growth trends and usage patterns, ensuring adequate capacity to meet future needs.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
