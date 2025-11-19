# Retry Pattern

1. **Name of Algorithm**  
   Retry Pattern

2. **What problem does it solve? (1 sentence)**  
   Automatically retries failed operations with exponential backoff to handle transient failures and improve system reliability.

3. **Intuition (plain-language explanation)**  
   Like retrying a phone call: if it fails, wait a bit longer each time before trying again, giving the system time to recover from temporary issues.

4. **Inputs & Outputs**  
   - Input: Operation to retry, retry policy (max attempts, backoff strategy), failure conditions.  
   - Output: Successful operation result or final failure after retries exhausted.

5. **Step-by-step description (5–10 lines max)**  
1. Execute operation (API call, database query, etc.).
2. If operation fails with retryable error, wait (exponential backoff).
3. Retry operation up to maximum attempts.
4. If all retries fail, return error or fallback.
5. If operation succeeds, return result immediately.
6. Optionally log retry attempts for monitoring.

6. **Tiny example (hand-simulated)**  
   API call fails with 503 error → wait 1s → retry → fails → wait 2s → retry → fails → wait 4s → retry → succeeds. Total: 3 retries, 7s elapsed.

7. **Time & Space Complexity**  
   - Time: O(k) where k is number of retry attempts (depends on backoff strategy).  
   - Space: O(1) for retry state (minimal memory).

8. **Strengths**  
- Handles transient failures automatically.
- Improves system resilience and user experience.

9. **Weaknesses / limitations**  
- May delay failure detection for permanent errors.
- Can increase load on failing services.

10. **Compare with alternatives**  
    Alternatives: Circuit Breaker, Exponential Backoff, Jittered Retry

11. **30-second explanation (your own words)**  
    Automatically retries failed operations with increasing delays between attempts, handling transient failures and improving system reliability.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
