# Rate Limiting

1. **Name of Algorithm**  
   Rate Limiting

2. **What problem does it solve? (1 sentence)**  
Controls the rate of requests from clients to prevent abuse, ensure fair resource usage, and protect services from overload.

3. **Intuition (plain-language explanation)**  
Like a bouncer at a club: limit how many people (requests) can enter per hour to prevent overcrowding and ensure everyone gets served.

4. **Inputs & Outputs**  
   - Input: Client requests, rate limit rules (requests per time window), client identifier.  
   - Output: Allowed requests or rate limit exceeded errors (429).

5. **Step-by-step description (5–10 lines max)**  
1. Identify client (IP address, API key, user ID).
2. Check current request count for client in time window.
3. If under limit: allow request and increment counter.
4. If at limit: reject request with 429 (Too Many Requests) error.
5. Reset counters when time window expires.
6. Optionally implement different limits per client tier.

6. **Tiny example (hand-simulated)**  
   API limit: 100 requests/hour per API key. Key 'abc123' makes 50 requests → allowed. Makes 60 more → 110 total → 51st request in hour returns 429 error.

7. **Time & Space Complexity**  
   - Time: O(1) for limit check (hash table lookup and counter increment).  
   - Space: O(n) for n unique clients (counter storage per client).

8. **Strengths**  
- Prevents abuse and ensures fair resource allocation.
- Protects services from overload and DDoS attacks.

9. **Weaknesses / limitations**  
- May block legitimate users during traffic spikes.
- Requires distributed state for multi-server deployments.

10. **Compare with alternatives**  
Alternatives: Throttling, Quotas, Token Bucket Algorithm

11. **30-second explanation (your own words)**  
    Limits the number of requests a client can make within a time window, preventing abuse and ensuring fair resource usage across all clients.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
