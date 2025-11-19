# Service Discovery

1. **Name of Algorithm**  
   Service Discovery

2. **What problem does it solve? (1 sentence)**  
   Automatically locates and connects to service instances in a distributed system, handling dynamic service registration, health checking, and load balancing without hardcoded service addresses.

3. **Intuition (plain-language explanation)**  
   Like a phone directory service: service discovery is like a phone directory service for microservices - when a service wants to call another service, instead of knowing the exact phone number (IP address) which might change, it looks up the service name in the directory (service registry) and gets the current phone number (service instance address) - the directory automatically updates when services start, stop, or move (dynamic registration), and only lists services that are currently available (health checks).

4. **Inputs & Outputs**  
   - Input: Service registrations, service queries, health checks, service metadata, network topology.  
   - Output: Service locations, healthy service instances, load-balanced connections, dynamic routing.

5. **Step-by-step description (5–10 lines max)**  
1. Register: services register themselves with service registry on startup.
2. Store: registry stores service information (name, address, port, metadata).
3. Health check: registry periodically checks service health.
4. Update: registry updates service status (healthy, unhealthy, removed).
5. Query: client queries registry for service by name.
6. Resolve: registry returns available service instances.
7. Select: client selects service instance (round-robin, random, least connections).
8. Connect: client connects to selected service instance.
9. Cache: client may cache service locations for performance.
10. Update cache: client updates cache when service instances change.

6. **Tiny example (hand-simulated)**  
   Service discovery: user-service starts → registers: name='user-service', address='10.0.1.5:8080' → registry: stores registration → health check: user-service healthy → order-service: queries registry for 'user-service' → registry: returns ['10.0.1.5:8080', '10.0.1.6:8080'] → order-service: selects instance → connects → user-service fails → registry: removes from list → order-service: gets updated list → service discovery operational.

7. **Time & Space Complexity**  
   - Time: O(1) for service lookup, O(n) for health checks where n is number of services.  
   - Space: O(s) where s is number of service instances (registry storage).

8. **Strengths**  
- Dynamic: handles dynamic service instances (start, stop, scale).
- Resilience: automatically handles service failures and recovery.
- Decoupling: decouples services from specific network addresses.

9. **Weaknesses / limitations**  
- Dependency: services depend on service registry availability.
- Latency: service lookup adds latency (can be cached).
- Complexity: managing service registry adds operational complexity.

10. **Compare with alternatives**  
    Alternatives: Hardcoded Addresses, DNS, Load Balancer, Service Mesh

11. **30-second explanation (your own words)**  
    Automatically locates and connects to service instances in a distributed system, handling dynamic service registration, health checking, and load balancing without hardcoded service addresses.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
