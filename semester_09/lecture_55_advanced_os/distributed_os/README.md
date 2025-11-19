# Distributed Operating Systems

1. **Name of Algorithm**  
   Distributed Operating Systems

2. **What problem does it solve? (1 sentence)**  
   Manages resources and provides services across multiple networked computers, presenting them as a single unified system to users and applications.

3. **Intuition (plain-language explanation)**  
   Like a distributed company: distributed operating systems are like a company with offices in multiple cities - each office (computer) has its own resources (employees, equipment), but they all work together as one company (unified system) - you can access resources from any office (any computer), and the system handles coordination behind the scenes (like company-wide communication) - to users, it looks like one big system, even though it's actually many computers working together.

4. **Inputs & Outputs**  
   - Input: Networked computers, distributed resources, user requests, application processes.  
   - Output: Unified system view, distributed services, resource sharing, fault tolerance.

5. **Step-by-step description (5–10 lines max)**  
1. Network nodes: connect multiple computers via network.
2. Resource discovery: discover and catalog resources across nodes.
3. Distribute services: distribute OS services (file system, process management) across nodes.
4. Provide transparency: present distributed system as single unified system.
5. Handle communication: manage inter-node communication and coordination.
6. Manage resources: allocate and manage resources across distributed nodes.
7. Handle failures: detect and recover from node failures.
8. Load balance: distribute workload across available nodes.
9. Maintain consistency: ensure data consistency across distributed nodes.
10. Provide APIs: offer unified APIs for applications to access distributed resources.

6. **Tiny example (hand-simulated)**  
   Distributed OS: 5 computers connected → unified file system: files stored across nodes, accessed transparently → process migration: move processes between nodes for load balancing → resource sharing: CPU, memory, storage shared across network → fault tolerance: if node fails, services continue on other nodes → transparency: user sees single system → distributed OS operational.

7. **Time & Space Complexity**  
   - Time: O(n) for coordination where n is number of nodes, O(log n) for resource lookup with distributed algorithms.  
   - Space: O(n) where n is number of nodes (distributed state management).

8. **Strengths**  
- Scalability: can scale by adding more nodes.
- Fault tolerance: system continues operating if nodes fail.
- Resource sharing: enables efficient resource utilization across nodes.

9. **Weaknesses / limitations**  
- Complexity: managing distributed systems is complex.
- Network latency: communication between nodes introduces latency.
- Consistency: maintaining consistency across nodes is challenging.

10. **Compare with alternatives**  
    Alternatives: Centralized OS, Network OS, Cluster Computing, Cloud Computing

11. **30-second explanation (your own words)**  
    Manages resources and provides services across multiple networked computers, presenting them as a single unified system to users and applications.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
