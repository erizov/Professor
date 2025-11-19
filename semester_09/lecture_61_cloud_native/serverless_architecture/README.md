# Serverless Architecture

1. **Name of Algorithm**  
   Serverless Architecture

2. **What problem does it solve? (1 sentence)**  
   Builds applications using serverless computing services (FaaS, managed databases, event-driven services) where developers don't manage servers, and the cloud provider handles infrastructure, scaling, and resource management automatically.

3. **Intuition (plain-language explanation)**  
   Like a fully managed restaurant: serverless architecture is like a fully managed restaurant where you just provide recipes (code) and ingredients (data), and the restaurant (cloud provider) handles everything else - cooking (execution), serving (scaling), cleaning (resource management), and maintenance (infrastructure) - you don't need to hire chefs, waiters, or manage the kitchen (servers) - you just focus on the food (business logic) and pay for what you serve (usage-based pricing).

4. **Inputs & Outputs**  
   - Input: Application code, event triggers, data, business logic, resource requirements.  
   - Output: Serverless application, auto-scaled services, managed infrastructure, event-driven system.

5. **Step-by-step description (5–10 lines max)**  
1. Design: design application using serverless services (functions, managed databases, event streams).
2. Write functions: write stateless functions for business logic.
3. Use managed services: use managed services (databases, storage, queues) instead of self-managed.
4. Configure triggers: configure event triggers for functions.
5. Deploy: deploy to serverless platform (no server provisioning).
6. Execute: functions execute when triggered by events.
7. Scale: platform automatically scales functions based on load.
8. Pay: pay only for actual usage (execution time, storage, requests).
9. Monitor: monitor application using serverless monitoring tools.
10. Update: update functions without managing infrastructure.

6. **Tiny example (hand-simulated)**  
   Serverless architecture: e-commerce app → API Gateway (managed) → Lambda functions (FaaS) → DynamoDB (managed database) → S3 (managed storage) → EventBridge (managed events) → no servers to manage → auto-scales: 10 requests → 10 functions, 1000 requests → 1000 functions → pay: only for actual usage → serverless architecture.

7. **Time & Space Complexity**  
   - Time: O(f) where f is function execution time (varies by business logic).  
   - Space: O(d) where d is data size (managed by cloud provider, no persistent server storage).

8. **Strengths**  
- No infrastructure: eliminates server management overhead.
- Auto-scaling: automatically scales to any load.
- Cost-effective: pay only for actual usage.

9. **Weaknesses / limitations**  
- Vendor lock-in: applications depend on cloud provider services.
- Cold starts: first invocation may have latency.
- Debugging: debugging distributed serverless applications can be challenging.

10. **Compare with alternatives**  
    Alternatives: Traditional Servers, Containers, Virtual Machines, Hybrid Architecture

11. **30-second explanation (your own words)**  
    Builds applications using serverless computing services (FaaS, managed databases, event-driven services) where developers don't manage servers, and the cloud provider handles infrastructure, scaling, and resource management automatically.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
