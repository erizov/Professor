# OS Security Models

1. **Name of Algorithm**  
   OS Security Models

2. **What problem does it solve? (1 sentence)**  
   Defines security policies and mechanisms for controlling access to system resources, protecting against unauthorized access, and ensuring system integrity and confidentiality.

3. **Intuition (plain-language explanation)**  
   Like a building's security system: OS security models are like a building's comprehensive security system - you have access control (who can enter which rooms), authentication (checking IDs at the entrance), authorization (what each person is allowed to do), and monitoring (security cameras) - the security model defines the rules (like 'only employees can access the server room') and the mechanisms (like keycards and cameras) that enforce those rules to protect the building (operating system).

4. **Inputs & Outputs**  
   - Input: User credentials, access requests, security policies, system resources, audit logs.  
   - Output: Access control decisions, security enforcement, audit trails, protected system.

5. **Step-by-step description (5–10 lines max)**  
1. Define model: choose security model (DAC, MAC, RBAC, etc.).
2. Authenticate: verify user identity (passwords, certificates, biometrics).
3. Authorize: determine user permissions based on security model.
4. Enforce: enforce access control on resource access requests.
5. Audit: log security events and access attempts.
6. Monitor: continuously monitor for security violations and threats.
7. Update: update security policies and permissions as needed.
8. Protect: protect system integrity and prevent unauthorized modifications.
9. Isolate: isolate processes and users to prevent interference.
10. Encrypt: encrypt sensitive data at rest and in transit.

6. **Tiny example (hand-simulated)**  
   OS security model: RBAC (Role-Based Access Control) → roles: admin, user, guest → permissions: admin (full access), user (read/write own files), guest (read only) → authenticate: user logs in → authorize: check user role → enforce: user tries to delete system file → denied (not admin) → audit: log access attempt → security enforced.

7. **Time & Space Complexity**  
   - Time: O(1) for access control checks, O(u) for authentication where u is user database size.  
   - Space: O(p + a) where p is policy size, a is audit log size.

8. **Strengths**  
- Protection: protects system from unauthorized access and attacks.
- Flexibility: supports various security models (DAC, MAC, RBAC).
- Auditability: provides audit trails for security monitoring.

9. **Weaknesses / limitations**  
- Complexity: implementing comprehensive security can be complex.
- Performance: security checks add overhead to system operations.
- Usability: strict security may impact user experience.

10. **Compare with alternatives**  
    Alternatives: Discretionary Access Control (DAC), Mandatory Access Control (MAC), Role-Based Access Control (RBAC), Capability-Based Security

11. **30-second explanation (your own words)**  
    Defines security policies and mechanisms for controlling access to system resources, protecting against unauthorized access, and ensuring system integrity and confidentiality.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
