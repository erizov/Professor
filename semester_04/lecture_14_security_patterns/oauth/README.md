# OAuth 2.0

1. **Name of Algorithm**  
   OAuth 2.0

2. **What problem does it solve? (1 sentence)**  
   Enables third-party applications to obtain limited access to user resources without exposing user credentials, using authorization tokens.

3. **Intuition (plain-language explanation)**  
   Like a hotel key card: instead of giving your master key (password) to every service, issue temporary access cards (tokens) with specific permissions.

4. **Inputs & Outputs**  
   - Input: Client application, resource owner (user), authorization server, resource server, scopes (permissions).  
   - Output: Access token and optionally refresh token for accessing protected resources.

5. **Step-by-step description (5–10 lines max)**  
1. Client redirects user to authorization server with client ID and requested scopes.
2. User authenticates and grants/denies permission.
3. Authorization server redirects back to client with authorization code.
4. Client exchanges authorization code for access token (with client secret).
5. Client uses access token to access protected resources from resource server.
6. Optionally refresh token to obtain new access token when expired.

6. **Tiny example (hand-simulated)**  
   Photo app wants access to user's Google photos: user authorizes → Google issues token → app uses token to fetch photos without user's password.

7. **Time & Space Complexity**  
   - Time: O(1) for token validation; O(n) for authorization flow (multiple HTTP requests).  
   - Space: O(1) for token storage; O(n) for client and user registrations.

8. **Strengths**  
- No password sharing: users don't expose credentials to third parties.
- Fine-grained permissions through scopes.

9. **Weaknesses / limitations**  
- Complex flow with multiple parties and security considerations.
- Token management complexity (expiration, refresh, revocation).

10. **Compare with alternatives**  
    Alternatives: SAML, OpenID Connect, API Keys, JWT Bearer Tokens

11. **30-second explanation (your own words)**  
    Delegates authorization to a trusted server that issues tokens to third-party applications, allowing resource access without password sharing.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
