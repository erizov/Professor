# Fault Injection

1. **Name of Algorithm**  
   Fault Injection

2. **What problem does it solve? (1 sentence)**  
   Intentionally injects faults (failures, errors, delays) into systems to test resilience, validate error handling, and identify failure modes.

3. **Intuition (plain-language explanation)**  
   Like stress testing: Fault Injection is like stress testing for systems - you intentionally create problems (inject faults) to see how the system handles them - just as stress tests reveal weaknesses, fault injection reveals how systems handle failures.

4. **Inputs & Outputs**  
   - Input: System components, fault types, injection points, fault parameters, monitoring tools, safety rules.  
   - Output: Injected faults, system behavior, error handling validation, failure modes, resilience insights.

5. **Step-by-step description (5–10 lines max)**  
1. Identify targets: identify components to inject faults into.
2. Select faults: select fault types (crash, delay, error, resource exhaustion).
3. Configure: configure fault injection parameters.
4. Inject: inject fault into target component.
5. Observe: observe system behavior and error handling.
6. Measure: measure impact and recovery.
7. Analyze: analyze how system handles fault.
8. Document: document fault injection results.
9. Improve: improve error handling based on findings.
10. Iterate: iterate with different fault types.

6. **Tiny example (hand-simulated)**  
   Fault Injection: target: database service → fault: network delay 5s → inject: delay database requests → observe: system times out, retries, uses cache → measure: 5s delay, graceful degradation → analyze: good error handling → Fault Injection successful.

7. **Time & Space Complexity**  
   - Time: O(i + o + a) where i is injection time, o is observation time, a is analysis time (varies by fault type).  
   - Space: O(f + d) where f is fault configuration storage, d is data storage (injection logs).

8. **Strengths**  
- Testing: enables testing of error handling and recovery.
- Discovery: discovers failure modes before production.
- Validation: validates system resilience under faults.

9. **Weaknesses / limitations**  
- Risk: fault injection can cause production issues.
- Coverage: may not cover all fault types.
- Complexity: requires understanding of system architecture.

10. **Compare with alternatives**  
    Alternatives: No Testing, Manual Testing, Simulation, Chaos Engineering

11. **30-second explanation (your own words)**  
    Intentionally injects faults (failures, errors, delays) into systems to test resilience, validate error handling, and identify failure modes.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
