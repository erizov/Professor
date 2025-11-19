# Authorization

1. **Name of Algorithm**  
   Authorization

2. **What problem does it solve? (1 sentence)**  
   Determines what actions an authenticated user or system is permitted to perform on specific resources.

3. **Intuition (plain-language explanation)**  
   After authentication confirms who you are, authorization checks what you're allowed to do: like a bouncer checking if you have VIP access.

4. **Inputs & Outputs**  
   - Input: Authenticated user identity, requested action, target resource, access control policies.  
   - Output: Authorization decision (allow/deny) with optional reason.

5. **Step-by-step description (5–10 lines max)**  
1. Extract user identity and requested action from request.
2. Retrieve user roles/permissions from identity store.
3. Evaluate access control policies (RBAC, ABAC, ACL).
4. Check if user has required permission for action on resource.
5. Return allow or deny decision.

6. **Tiny example (hand-simulated)**  
   User requests DELETE /api/users/123. System checks: user is admin? → allow. User is owner of user 123? → allow. Otherwise → deny.

7. **Time & Space Complexity**  
   - Time: O(1) to O(r) where r is number of roles/permissions to check.  
   - Space: O(u·p) for u users with p permissions each.

8. **Strengths**  
- Enforces least privilege principle.
- Flexible models: RBAC, ABAC, ACL support different needs.

9. **Weaknesses / limitations**  
- Complex policy management in large systems.
- Performance overhead of permission checks on every request.

10. **Compare with alternatives**  
    Alternatives: Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC), Access Control Lists (ACL)

11. **30-second explanation (your own words)**  
    Evaluates whether an authenticated user has permission to perform a specific action on a resource based on access control policies.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
