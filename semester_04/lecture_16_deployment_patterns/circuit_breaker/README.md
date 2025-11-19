# Circuit Breaker

1. **Name of Algorithm**  
   Circuit Breaker

2. **What problem does it solve? (1 sentence)**  
   Prevents cascading failures by detecting service failures and temporarily stopping requests to failing services, allowing recovery time.

3. **Intuition (plain-language explanation)**  
   Like electrical circuit breakers: when a circuit (service) fails repeatedly, trip the breaker to stop current (requests) and prevent damage (cascading failures).

4. **Inputs & Outputs**  
   - Input: Service calls, failure thresholds, timeout configurations.  
   - Output: Circuit state (closed, open, half-open) and request handling decisions.

5. **Step-by-step description (5–10 lines max)**  
1. Monitor service call failures and response times.
2. If failure count exceeds threshold, open circuit (stop requests).
3. Return fallback response or error immediately (fast failure).
4. After timeout period, transition to half-open state.
5. Allow test request through; if successful, close circuit; if fails, reopen.
6. Continue monitoring and adjusting circuit state.

6. **Tiny example (hand-simulated)**  
   Payment service fails 5 times in 10 seconds → circuit opens → subsequent requests fail fast with fallback → after 30s, test request → if succeeds, close circuit.

7. **Time & Space Complexity**  
   - Time: O(1) for circuit state check and request handling.  
   - Space: O(1) for circuit state storage (minimal overhead).

8. **Strengths**  
- Prevents cascading failures and resource exhaustion.
- Fast failure improves user experience.

9. **Weaknesses / limitations**  
- Requires fallback strategies.
- May delay recovery if timeout too long.

10. **Compare with alternatives**  
    Alternatives: Retry Pattern, Bulkhead Pattern, Timeout Pattern

11. **30-second explanation (your own words)**  
    Detects service failures and temporarily stops requests to failing services, preventing cascading failures and allowing time for recovery.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
