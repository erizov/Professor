# Root Cause Analysis (RCA)

1. **Name of Algorithm**  
   Root Cause Analysis (RCA)

2. **What problem does it solve? (1 sentence)**  
   Systematically identifies the underlying root cause of incidents and problems, enabling permanent fixes rather than temporary workarounds and preventing recurrence.

3. **Intuition (plain-language explanation)**  
   Like detective work: Root Cause Analysis is like detective work for incidents - you investigate clues (logs, metrics), trace back to find the real cause (root cause), not just the symptoms - just as detectives solve crimes by finding the real culprit, RCA solves incidents by finding the real cause.

4. **Inputs & Outputs**  
   - Input: Incident data, logs, metrics, traces, system state, timeline, team knowledge.  
   - Output: Root cause identification, incident analysis, improvement recommendations, permanent fixes, prevention measures.

5. **Step-by-step description (5–10 lines max)**  
1. Gather data: gather all relevant data (logs, metrics, traces).
2. Timeline: create timeline of events leading to incident.
3. Analyze: analyze data and timeline.
4. Hypothesize: form hypotheses about root cause.
5. Investigate: investigate hypotheses.
6. Identify: identify root cause.
7. Verify: verify root cause through testing or evidence.
8. Document: document root cause and analysis.
9. Fix: implement permanent fix for root cause.
10. Prevent: implement measures to prevent recurrence.

6. **Tiny example (hand-simulated)**  
   Root Cause Analysis: incident: service outage → gather: logs, metrics, traces → timeline: database connection pool exhausted → analyze: connection leak in code → identify: root cause: missing connection cleanup → fix: add connection cleanup → prevent: add monitoring → RCA successful.

7. **Time & Space Complexity**  
   - Time: O(g + a + i) where g is data gathering time, a is analysis time, i is investigation time (hours to days).  
   - Space: O(d + a) where d is data storage, a is analysis storage (RCA documents).

8. **Strengths**  
- Permanent fixes: enables permanent fixes rather than workarounds.
- Prevention: prevents recurrence of incidents.
- Learning: provides deep learning about system behavior.

9. **Weaknesses / limitations**  
- Time: thorough RCA takes significant time.
- Complexity: complex incidents may have multiple root causes.
- Skills: requires analytical and investigative skills.

10. **Compare with alternatives**  
    Alternatives: Symptom Fixing, Quick Fixes, Blame Assignment, No Analysis

11. **30-second explanation (your own words)**  
    Systematically identifies the underlying root cause of incidents and problems, enabling permanent fixes rather than temporary workarounds and preventing recurrence.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
