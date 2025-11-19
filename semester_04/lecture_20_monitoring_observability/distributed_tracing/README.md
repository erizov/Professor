# Distributed Tracing

1. **Name of Algorithm**  
   Distributed Tracing

2. **What problem does it solve? (1 sentence)**  
   Tracks requests across multiple services in a distributed system to understand request flow, identify bottlenecks, and debug performance issues.

3. **Intuition (plain-language explanation)**  
   Like a package tracking number: follow a request's journey through multiple services, recording each step to see where it goes and how long it takes.

4. **Inputs & Outputs**  
   - Input: Request headers (trace ID, span ID), service calls, instrumentation points.  
   - Output: Complete trace showing request path through services with timing and metadata.

5. **Step-by-step description (5–10 lines max)**  
1. Generate or extract trace ID at request entry point.
2. Create root span for initial service.
3. Propagate trace context (trace ID, span ID) in request headers.
4. Each service creates child spans for operations.
5. Spans record start time, end time, tags, and logs.
6. Send spans to tracing backend for aggregation and visualization.

6. **Tiny example (hand-simulated)**  
   User request → API Gateway (span 1) → Auth Service (span 2) → Order Service (span 3) → Payment Service (span 4). Trace shows full path and 2.3s total latency.

7. **Time & Space Complexity**  
   - Time: O(1) for span creation; O(n) for trace collection where n is number of services.  
   - Space: O(n) for trace data where n is number of spans in trace.

8. **Strengths**  
- End-to-end visibility across distributed systems.
- Identifies performance bottlenecks and dependencies.

9. **Weaknesses / limitations**  
- Overhead from instrumentation and data collection.
- Requires consistent trace context propagation.

10. **Compare with alternatives**  
    Alternatives: Log Correlation, APM Tools, Service Mesh Observability

11. **30-second explanation (your own words)**  
    Instruments services to create spans that form traces, enabling visualization of request flows and performance analysis across distributed systems.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
