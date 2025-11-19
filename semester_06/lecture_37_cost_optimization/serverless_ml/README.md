# Serverless ML

1. **Name of Algorithm**  
   Serverless ML

2. **What problem does it solve? (1 sentence)**  
   Deploys ML models on serverless platforms (AWS Lambda, Azure Functions, Google Cloud Functions) that automatically manage infrastructure, scale to zero when idle, and charge only for actual execution time, reducing operational overhead and costs.

3. **Intuition (plain-language explanation)**  
   Like a pay-per-use gym: instead of renting a server 24/7 (expensive), use serverless functions that only run when you need them - you pay only for the seconds the function executes, and the platform handles all the infrastructure management.

4. **Inputs & Outputs**  
   - Input: ML model, inference code, serverless platform configuration, trigger (API Gateway, event, schedule).  
   - Output: Serverless ML function that executes on-demand, scales automatically, and charges per invocation.

5. **Step-by-step description (5–10 lines max)**  
1. Package model: bundle model file with inference code into deployment package.
2. Create serverless function: define function handler, runtime (Python, Node.js), memory allocation, timeout.
3. Configure triggers: set up API Gateway, event sources, or scheduled triggers to invoke function.
4. Deploy function: upload package to serverless platform (Lambda, Functions, etc.).
5. Function execution: platform automatically provisions container, loads model, runs inference, returns result.
6. Auto-scaling: platform automatically scales functions based on concurrent requests (no manual configuration).
7. Scale to zero: function automatically shuts down when idle (no cost when not in use).
8. Monitor: track invocations, duration, errors, and costs through platform metrics.

6. **Tiny example (hand-simulated)**  
   Image classification: API request → API Gateway → Lambda function (loads ResNet-50 from S3) → inference (200ms) → return prediction → function terminates → cost: $0.0000167 per 100ms (pay only for execution time, no idle costs).

7. **Time & Space Complexity**  
   - Time: O(C + I) where C is cold start time (model loading, typically 1-5s), I is inference time (warm starts are faster).  
   - Space: O(M) for model in function package, O(M) for model in memory during execution (limited by function memory limit, typically 512MB-10GB).

8. **Strengths**  
- Cost efficient: pay only for execution time, no idle costs.
- Zero operational overhead: platform manages infrastructure, scaling, monitoring.
- Automatic scaling: handles traffic spikes without configuration.

9. **Weaknesses / limitations**  
- Cold start latency: first request may be slow due to model loading.
- Size limits: model size constrained by function package and memory limits.
- Timeout limits: functions have maximum execution time (typically 15 minutes).

10. **Compare with alternatives**  
    Alternatives: Container-based Deployment, Managed ML Services, Kubernetes, Virtual Machines

11. **30-second explanation (your own words)**  
    Deploys ML models on serverless platforms that automatically manage infrastructure, scale to zero when idle, and charge only for execution time, reducing operational overhead and costs.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
