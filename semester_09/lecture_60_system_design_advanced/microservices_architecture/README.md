# Microservices Architecture

1. **Name of Algorithm**  
   Microservices Architecture

2. **What problem does it solve? (1 sentence)**  
   Structures applications as a collection of small, independent services that communicate over well-defined APIs, enabling independent development, deployment, and scaling of services.

3. **Intuition (plain-language explanation)**  
   Like a team of specialists: Microservices Architecture is like a team of specialists where each person (service) has a specific expertise (domain) and works independently - they communicate when needed (API calls) but can work on their own schedule (independent deployment) - just as a team of specialists can work faster and more flexibly than one person doing everything, microservices can develop and scale faster than monolithic applications.

4. **Inputs & Outputs**  
   - Input: Service definitions, API contracts, service boundaries, communication protocols, deployment units.  
   - Output: Independent services, service APIs, distributed system, scalable architecture, flexible deployment.

5. **Step-by-step description (5–10 lines max)**  
1. Identify boundaries: identify service boundaries (domain-driven design).
2. Design services: design small, focused services (single responsibility).
3. Define APIs: define APIs for service communication.
4. Implement: implement services independently.
5. Deploy: deploy services independently.
6. Communicate: services communicate via APIs (REST, gRPC, messaging).
7. Scale: scale services independently based on load.
8. Monitor: monitor services independently.
9. Update: update services independently without affecting others.
10. Orchestrate: orchestrate services for complex operations.

6. **Tiny example (hand-simulated)**  
   Microservices: user-service (user management) → order-service (orders) → payment-service (payments) → each service: independent, deployable, scalable → communicate: via REST APIs → scale: user-service scales for login spikes → update: update payment-service without affecting others → Microservices Architecture operational.

7. **Time & Space Complexity**  
   - Time: O(1) per service operation, O(n) for orchestration where n is number of services.  
   - Space: O(s) where s is total service storage (distributed across services).

8. **Strengths**  
- Independence: services can be developed and deployed independently.
- Scalability: scale services independently based on needs.
- Technology diversity: use different technologies per service.

9. **Weaknesses / limitations**  
- Complexity: distributed system complexity (networking, coordination).
- Data consistency: maintaining consistency across services is challenging.
- Operational overhead: more services to manage and monitor.

10. **Compare with alternatives**  
    Alternatives: Monolithic Architecture, Service-Oriented Architecture, Modular Monolith, Serverless

11. **30-second explanation (your own words)**  
    Structures applications as a collection of small, independent services that communicate over well-defined APIs, enabling independent development, deployment, and scaling of services.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
