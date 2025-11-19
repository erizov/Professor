# JWT (JSON Web Token)

1. **Name of Algorithm**  
   JWT (JSON Web Token)

2. **What problem does it solve? (1 sentence)**  
   Provides a compact, URL-safe token format for securely transmitting claims between parties, commonly used for stateless authentication and authorization.

3. **Intuition (plain-language explanation)**  
   Like a tamper-proof ticket: contains user info and permissions, signed so server can verify it wasn't altered, eliminating need to store sessions.

4. **Inputs & Outputs**  
   - Input: Header (algorithm, type), payload (claims like user ID, roles, expiration), secret key or private key.  
   - Output: JWT token string (header.payload.signature) in base64url encoding.

5. **Step-by-step description (5–10 lines max)**  
1. Create header: algorithm (HS256, RS256) and token type (JWT).
2. Create payload: claims (iss, sub, exp, iat, custom claims).
3. Base64url encode header and payload separately.
4. Create signature: HMAC or RSA signature of encoded header + '.' + encoded payload.
5. Combine: header.payload.signature.
6. Client stores token, sends in Authorization header; server validates signature and claims.

6. **Tiny example (hand-simulated)**  
   Token: eyJhbGc... (header).eyJzdWI... (payload: {sub: 'user123', exp: 1234567890}).SflKxwRJ... (signature). Server validates signature and checks expiration.

7. **Time & Space Complexity**  
   - Time: Generate: O(1); Validate: O(1) for signature verification.  
   - Space: O(1) for token size (typically 100-500 bytes).

8. **Strengths**  
- Stateless: no server-side session storage needed.
- Self-contained: includes all necessary claims.

9. **Weaknesses / limitations**  
- Cannot revoke tokens before expiration (requires blacklist or short expiry).
- Larger than session IDs (sent with every request).

10. **Compare with alternatives**  
    Alternatives: Session-based Authentication, OAuth 2.0 Access Tokens, SAML Assertions

11. **30-second explanation (your own words)**  
    Encodes authentication/authorization claims as a signed JSON token, enabling stateless, scalable authentication without server-side session storage.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
