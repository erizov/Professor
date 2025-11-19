# Authentication

1. **Name of Algorithm**  
   Authentication

2. **What problem does it solve? (1 sentence)**  
   Verifies the identity of users or systems attempting to access resources, ensuring only authorized entities can proceed.

3. **Intuition (plain-language explanation)**  
   Like showing ID at a checkpoint: prove who you are using credentials (password, token, biometric) before being allowed entry.

4. **Inputs & Outputs**  
   - Input: User credentials (username/password, tokens, certificates, biometrics).  
   - Output: Authentication result (success/failure) and session token or identity claim.

5. **Step-by-step description (5–10 lines max)**  
1. User provides credentials (e.g., username and password).
2. System validates credentials against stored identity store.
3. On success: generate session token or JWT, store session (if stateful).
4. Return token to client for subsequent requests.
5. On failure: return error, optionally implement rate limiting.

6. **Tiny example (hand-simulated)**  
   Login flow: user enters username/password → server hashes password, compares with stored hash → if match, issue JWT token → client uses token for API calls.

7. **Time & Space Complexity**  
   - Time: O(1) for token validation; O(n) for credential lookup in database.  
   - Space: O(1) for token storage; O(n) for user credential database.

8. **Strengths**  
- Foundation of security: verifies identity before authorization.
- Multiple methods available (password, OAuth, certificates).

9. **Weaknesses / limitations**  
- Password-based auth vulnerable to breaches and phishing.
- Session management complexity (tokens, refresh, revocation).

10. **Compare with alternatives**  
    Alternatives: OAuth 2.0, SAML, Certificate-based Authentication, Biometric Authentication

11. **30-second explanation (your own words)**  
    Verifies user identity through credentials, establishing trust before allowing access to protected resources.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
