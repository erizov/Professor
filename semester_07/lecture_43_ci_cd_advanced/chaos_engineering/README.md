# Chaos Engineering

1. **Name of Algorithm**  
   Chaos Engineering

2. **What problem does it solve? (1 sentence)**  
   Proactively tests system resilience by intentionally injecting failures and disruptions in production-like environments, identifying weaknesses before they cause real outages.

3. **Intuition (plain-language explanation)**  
   Like stress-testing a bridge: instead of waiting for it to fail under real load, you intentionally create controlled failures (remove a cable, add weight) to see how it handles stress - chaos engineering does the same for software systems.

4. **Inputs & Outputs**  
   - Input: Production-like environment, chaos experiments (failure scenarios), monitoring tools, system under test.  
   - Output: Identified system weaknesses, improved resilience, validated failure handling, documented recovery procedures.

5. **Step-by-step description (5–10 lines max)**  
1. Define hypothesis: state expected system behavior under failure (e.g., 'system should handle server crash gracefully').
2. Design experiment: create controlled failure scenario (kill server, inject latency, network partition, etc.).
3. Run in production-like: execute experiment in staging or small production subset.
4. Monitor: observe system behavior, metrics, error rates, recovery time.
5. Analyze: compare actual behavior with expected behavior (hypothesis).
6. Fix issues: address weaknesses discovered during experiment.
7. Document: record findings, recovery procedures, and improvements.
8. Repeat: run regular chaos experiments to continuously improve resilience.

6. **Tiny example (hand-simulated)**  
   Hypothesis: 'system handles database failure gracefully' → inject: kill database server → observe: system switches to read-only mode, alerts team, recovers in 30 seconds → validate: system resilient → document findings → repeat with other failure scenarios.

7. **Time & Space Complexity**  
   - Time: O(E + M) where E is experiment execution time, M is monitoring/analysis time (typically minutes to hours per experiment).  
   - Space: O(S) where S is system size (experiments run on actual or production-like systems).

8. **Strengths**  
- Proactive: finds issues before they cause real outages.
- Real-world: tests actual system behavior under failure.
- Continuous improvement: builds more resilient systems over time.

9. **Weaknesses / limitations**  
- Risk: can cause real issues if not carefully controlled.
- Resource intensive: requires dedicated time and infrastructure.
- Complexity: requires expertise in system architecture and failure modes.

10. **Compare with alternatives**  
    Alternatives: Load Testing, Failure Testing, Disaster Recovery Drills, Resilience Testing

11. **30-second explanation (your own words)**  
    Proactively tests system resilience by intentionally injecting failures and disruptions in production-like environments, identifying weaknesses before they cause real outages.
*Sources: Adapted from standard university textbooks and Wikipedia summaries.*