# Load Balancing

1. **Name of Algorithm**  
   Load Balancing

2. **What problem does it solve? (1 sentence)**  
Distributes incoming requests across multiple servers to optimize resource utilization, maximize throughput, and ensure high availability.

3. **Intuition (plain-language explanation)**  
   Like a restaurant host: when multiple tables (servers) are available, distribute customers (requests) evenly so no table is overloaded while others sit idle.

4. **Inputs & Outputs**  
- Input: Incoming requests, pool of backend servers, load balancing algorithm.
   - Output: Requests routed to appropriate servers with balanced load distribution.

5. **Step-by-step description (5–10 lines max)**  
1. Receive incoming request at load balancer.
2. Select server using algorithm (round-robin, least connections, weighted, etc.).
3. Route request to selected server.
4. Monitor server health and response times.
5. Remove unhealthy servers from pool.
6. Re-add servers when they recover.

6. **Tiny example (hand-simulated)**  
   3 servers: A, B, C. Requests 1,2,3 → round-robin routes to A,B,C. Request 4 → routes to A again. If B fails, route only to A and C.

7. **Time & Space Complexity**  
   - Time: O(1) to O(log n) for server selection depending on algorithm.  
   - Space: O(n) for server pool and health status tracking.

8. **Strengths**  
- Improves throughput and resource utilization.
- Provides high availability through redundancy.

9. **Weaknesses / limitations**  
- Requires session affinity for stateful applications.
- Adds latency and complexity.

10. **Compare with alternatives**  
    Alternatives: DNS Load Balancing, Client-Side Load Balancing, Service Mesh

11. **30-second explanation (your own words)**  
Distributes incoming requests across multiple servers using algorithms to balance load, optimize performance, and ensure high availability.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
