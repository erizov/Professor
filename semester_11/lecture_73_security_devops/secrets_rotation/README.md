# Secrets Rotation

1. **Name of Algorithm**  
   Secrets Rotation

2. **What problem does it solve? (1 sentence)**  
   Automatically rotates secrets (passwords, API keys, certificates) on a regular schedule or when compromised, reducing security risk and ensuring secrets remain secure.

3. **Intuition (plain-language explanation)**  
   Like changing locks: Secrets Rotation is like changing locks on your doors regularly - even if someone had a key, it won't work after you change the lock - rotating secrets regularly (changing passwords, keys) ensures that even if a secret is compromised, it becomes useless after rotation, keeping your systems secure.

4. **Inputs & Outputs**  
   - Input: Secrets, rotation policies, rotation schedules, secret stores, applications using secrets.  
   - Output: Rotated secrets, updated configurations, rotation logs, security improvements, reduced risk.

5. **Step-by-step description (5–10 lines max)**  
1. Identify: identify all secrets that need rotation.
2. Define policy: define rotation policy (schedule, triggers).
3. Generate: generate new secrets.
4. Update: update secrets in secret store.
5. Notify: notify applications of secret changes.
6. Update apps: update applications to use new secrets.
7. Validate: validate that applications work with new secrets.
8. Revoke: revoke old secrets after successful rotation.
9. Log: log rotation events for audit.
10. Monitor: monitor rotation success and failures.

6. **Tiny example (hand-simulated)**  
   Secrets Rotation: secret: database password → policy: rotate every 90 days → generate: new password → update: update in secret store → notify: notify database service → update: service uses new password → validate: connection successful → revoke: old password invalidated → Secrets Rotation successful.

7. **Time & Space Complexity**  
   - Time: O(n·r) where n is number of secrets, r is rotation time per secret (automated, scheduled).  
   - Space: O(s + l) where s is secret storage, l is log storage (rotation history).

8. **Strengths**  
- Security: reduces risk from compromised secrets.
- Automation: automates secret management tasks.
- Compliance: supports compliance requirements for secret rotation.

9. **Weaknesses / limitations**  
- Complexity: coordinating rotation across services can be complex.
- Downtime: rotation may cause brief service interruptions.
- Coordination: requires coordination with all services using secrets.

10. **Compare with alternatives**  
    Alternatives: Manual Rotation, No Rotation, On-Demand Rotation, Secret Management

11. **30-second explanation (your own words)**  
    Automatically rotates secrets (passwords, API keys, certificates) on a regular schedule or when compromised, reducing security risk and ensuring secrets remain secure.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
