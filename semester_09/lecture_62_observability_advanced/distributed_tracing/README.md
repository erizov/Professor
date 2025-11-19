# Distributed Tracing

1. **Name of Algorithm**  
   Distributed Tracing

2. **What problem does it solve? (1 sentence)**  
   Tracks requests as they flow through distributed systems, creating end-to-end traces that show the complete path of a request across multiple services, enabling debugging and performance optimization.

3. **Intuition (plain-language explanation)**  
   Like a package tracking system: distributed tracing is like tracking a package as it moves through a shipping network - you get a tracking number (trace ID) that follows the package (request) as it goes through different facilities (services) - you can see exactly where it is at each step (spans), how long it spends at each facility (timing), and if there are any delays (bottlenecks) - this helps you understand the complete journey and find where things slow down or fail.

4. **Inputs & Outputs**  
   - Input: Requests, trace IDs, span data, service interactions, timing information.  
   - Output: Distributed traces, request flows, performance insights, debugging information.

5. **Step-by-step description (5–10 lines max)**  
1. Generate trace: generate unique trace ID for incoming request.
2. Create span: create span for each service operation (start time, operation name).
3. Propagate: propagate trace ID through service calls (HTTP headers, message metadata).
4. Record spans: each service records spans for its operations.
5. Add context: add context to spans (tags, logs, timing).
6. Correlate: correlate spans by trace ID to build complete trace.
7. Collect: collect spans from all services.
8. Assemble: assemble spans into complete trace (tree structure).
9. Visualize: visualize trace showing request flow and timing.
10. Analyze: analyze traces to identify bottlenecks and errors.

6. **Tiny example (hand-simulated)**  
   Distributed tracing: user request → trace ID: abc123 → frontend: span 1 (10ms) → API gateway: span 2 (5ms) → user-service: span 3 (50ms) → database: span 4 (30ms) → order-service: span 5 (200ms) → payment-service: span 6 (150ms) → trace: shows complete flow → identify: order-service is slow → optimize: add caching → trace: order-service 200ms → 50ms → distributed tracing guides optimization.

7. **Time & Space Complexity**  
   - Time: O(1) per span creation, O(s) for trace assembly where s is number of spans.  
   - Space: O(t·s) where t is number of traces, s is average spans per trace (trace storage).

8. **Strengths**  
- Visibility: provides complete visibility into request flows.
- Debugging: enables debugging of complex distributed systems.
- Performance: identifies performance bottlenecks across services.

9. **Weaknesses / limitations**  
- Overhead: tracing adds overhead to application performance.
- Storage: storing traces requires significant storage.
- Sampling: may need to sample traces to manage volume.

10. **Compare with alternatives**  
    Alternatives: Logging, APM, Custom Instrumentation, Request IDs

11. **30-second explanation (your own words)**  
    Tracks requests as they flow through distributed systems, creating end-to-end traces that show the complete path of a request across multiple services, enabling debugging and performance optimization.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
