# Edge Computing

1. **Name of Algorithm**  
   Edge Computing

2. **What problem does it solve? (1 sentence)**  
   Processes data and runs applications closer to data sources (at the edge) rather than in centralized cloud data centers, reducing latency, bandwidth usage, and enabling real-time processing.

3. **Intuition (plain-language explanation)**  
   Like local processing: Edge Computing is like processing things locally instead of sending everything to a central location - instead of sending all data to the cloud (like mailing everything to headquarters), you process it locally (at the edge, like local offices) - just as local processing is faster, edge computing reduces latency and bandwidth.

4. **Inputs & Outputs**  
   - Input: Data sources, edge devices, applications, processing requirements, network conditions, latency constraints.  
   - Output: Edge-processed data, reduced latency, lower bandwidth usage, real-time responses, distributed processing, edge deployments.

5. **Step-by-step description (5–10 lines max)**  
1. Identify: identify workloads suitable for edge.
2. Deploy: deploy applications to edge devices.
3. Process: process data at the edge.
4. Filter: filter and aggregate data locally.
5. Sync: sync with cloud when needed.
6. Cache: cache frequently used data at edge.
7. Optimize: optimize for edge constraints.
8. Monitor: monitor edge deployments.
9. Manage: manage edge infrastructure.
10. Scale: scale edge deployments.

6. **Tiny example (hand-simulated)**  
   Edge Computing: workload: video analytics → deploy: deploy to edge cameras → process: analyze video locally → filter: send only alerts to cloud → result: 10ms latency (vs 200ms cloud), 90% bandwidth reduction → Edge Computing successful.

7. **Time & Space Complexity**  
   - Time: O(p) where p is processing time (reduced due to local processing).  
   - Space: O(e + c) where e is edge storage, c is cache storage (distributed storage).

8. **Strengths**  
- Latency: significantly reduces latency.
- Bandwidth: reduces bandwidth usage.
- Real-time: enables real-time processing.

9. **Weaknesses / limitations**  
- Management: managing edge infrastructure is complex.
- Resources: edge devices have limited resources.
- Security: edge devices may be less secure.

10. **Compare with alternatives**  
    Alternatives: Cloud Computing, Fog Computing, Hybrid Cloud-Edge, Centralized Processing

11. **30-second explanation (your own words)**  
    Processes data and runs applications closer to data sources (at the edge) rather than in centralized cloud data centers, reducing latency, bandwidth usage, and enabling real-time processing.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
