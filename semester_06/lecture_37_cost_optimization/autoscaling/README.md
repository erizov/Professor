# Autoscaling

1. **Name of Algorithm**  
   Autoscaling

2. **What problem does it solve? (1 sentence)**  
   Automatically adjusts the number of compute resources (servers, containers, instances) based on workload demand, ensuring adequate capacity during peak loads while minimizing costs during low usage periods.

3. **Intuition (plain-language explanation)**  
   Like a restaurant that automatically adds or removes tables based on customer flow: when busy (high demand), add more servers to handle requests - when quiet (low demand), reduce servers to save costs - all automatically based on metrics like request rate or CPU usage.

4. **Inputs & Outputs**  
   - Input: Workload metrics (CPU, memory, request rate, queue length), scaling policies (min/max instances, target metrics, scale-up/down thresholds).  
   - Output: Dynamically adjusted number of compute instances, optimized for cost and performance.

5. **Step-by-step description (5–10 lines max)**  
1. Define scaling metrics: choose metrics to monitor (CPU utilization, request rate, latency, queue depth).
2. Set scaling policies: define min/max instances, target metric values, scale-up/down thresholds.
3. Monitor metrics: continuously collect metrics from running instances.
4. Evaluate scaling conditions: compare current metrics to thresholds (e.g., CPU > 70% for 5 minutes).
5. Scale up: add instances when metrics exceed upper threshold (e.g., launch new containers, add servers).
6. Scale down: remove instances when metrics below lower threshold (e.g., terminate idle instances).
7. Apply cooldown periods: wait between scaling actions to avoid oscillation (rapid scale up/down).
8. Balance load: distribute traffic across scaled instances using load balancer.

6. **Tiny example (hand-simulated)**  
   ML inference service: baseline 2 instances → traffic increases → CPU 80% for 5min → scale up to 5 instances → traffic decreases → CPU 30% for 10min → scale down to 2 instances → cost: pay only for instances used, not idle capacity.

7. **Time & Space Complexity**  
   - Time: O(1) for metric evaluation, O(T) for instance provisioning where T is instance startup time (typically 1-5 minutes).  
   - Space: O(N·R) where N is number of instances, R is resources per instance (scales with demand).

8. **Strengths**  
- Cost efficient: pay only for resources actually used.
- Handles traffic spikes: automatically scales to meet demand.
- Reduces manual intervention: no need to manually adjust capacity.

9. **Weaknesses / limitations**  
- Scaling delay: takes time to provision new instances (may cause temporary overload).
- Complexity: requires careful tuning of thresholds to avoid oscillation.

10. **Compare with alternatives**  
    Alternatives: Manual Scaling, Scheduled Scaling, Predictive Scaling, Fixed Capacity

11. **30-second explanation (your own words)**  
    Automatically adjusts compute resources based on workload demand, ensuring adequate capacity during peaks while minimizing costs during low usage through dynamic scaling policies.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
