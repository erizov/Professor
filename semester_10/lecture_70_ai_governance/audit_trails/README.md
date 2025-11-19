# Audit Trails for AI Systems

1. **Name of Algorithm**  
   Audit Trails for AI Systems

2. **What problem does it solve? (1 sentence)**  
   Maintains comprehensive logs of all AI system activities, decisions, and data access, enabling accountability, compliance, and forensic analysis of AI operations.

3. **Intuition (plain-language explanation)**  
   Like a security camera system: Audit Trails for AI are like security cameras that record everything - they log who did what, when, and why (all AI activities, decisions, data access) - just as security cameras provide evidence and accountability, audit trails provide a complete record of AI operations, enabling you to trace decisions, prove compliance, and investigate issues.

4. **Inputs & Outputs**  
   - Input: AI operations, user actions, model decisions, data access, system events, metadata.  
   - Output: Audit logs, activity records, decision traces, compliance reports, forensic data.

5. **Step-by-step description (5–10 lines max)**  
1. Capture: capture all relevant activities (model invocations, data access, decisions).
2. Log: log activities with metadata (timestamp, user, context).
3. Store: store audit logs securely (immutable, tamper-proof).
4. Index: index logs for efficient querying.
5. Retain: retain logs according to retention policies.
6. Query: query logs for specific activities or time periods.
7. Analyze: analyze logs for patterns, anomalies, or compliance.
8. Report: generate audit reports for compliance.
9. Monitor: monitor audit log generation and storage.
10. Protect: protect audit logs from tampering or deletion.

6. **Tiny example (hand-simulated)**  
   Audit Trails: model: credit scoring → invoke: user applies for loan → log: timestamp, user ID, input data hash, model version, decision, confidence → store: immutable log → query: find all decisions by model version → analyze: compliance check → report: audit report generated → Audit Trails operational.

7. **Time & Space Complexity**  
   - Time: O(1) for logging per event, O(log n) for querying where n is number of log entries.  
   - Space: O(e) where e is total events logged (grows over time, requires retention policies).

8. **Strengths**  
- Accountability: enables accountability for AI decisions.
- Compliance: supports regulatory compliance requirements.
- Forensics: enables investigation of issues and incidents.

9. **Weaknesses / limitations**  
- Storage: audit logs require significant storage over time.
- Performance: logging can add overhead to operations.
- Privacy: logs may contain sensitive information.

10. **Compare with alternatives**  
    Alternatives: No Auditing, Selective Logging, Event Logging, Compliance Logging

11. **30-second explanation (your own words)**  

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
