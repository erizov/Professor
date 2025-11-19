# Security Scanning

1. **Name of Algorithm**  
   Security Scanning

2. **What problem does it solve? (1 sentence)**  
   Automatically scans code, dependencies, containers, and infrastructure for security vulnerabilities, misconfigurations, and threats, enabling proactive security management.

3. **Intuition (plain-language explanation)**  
   Like security inspections: Security Scanning is like security inspections at airports - automated systems scan everything (code, containers) for threats (vulnerabilities, malware) before they cause problems - just as airport scanners find threats before they enter, security scanning finds vulnerabilities before they're deployed.

4. **Inputs & Outputs**  
   - Input: Code repositories, container images, dependencies, infrastructure configs, vulnerability databases.  
   - Output: Vulnerability reports, security findings, risk assessments, remediation guidance, scan results.

5. **Step-by-step description (5–10 lines max)**  
1. Configure: configure scanning tools and policies.
2. Scan code: scan source code for vulnerabilities and secrets.
3. Scan dependencies: scan dependencies for known vulnerabilities.
4. Scan containers: scan container images for vulnerabilities.
5. Scan infrastructure: scan infrastructure for misconfigurations.
6. Analyze: analyze scan results and prioritize findings.
7. Report: generate security reports with findings.
8. Alert: alert on critical vulnerabilities.
9. Track: track vulnerabilities through remediation.
10. Integrate: integrate scanning into CI/CD pipeline.

6. **Tiny example (hand-simulated)**  
   Security Scanning: code: scan repository → dependencies: check for CVEs → containers: scan Docker images → infrastructure: check configs → findings: 5 high, 10 medium vulnerabilities → report: security report generated → alert: critical vulnerabilities flagged → Security Scanning operational.

7. **Time & Space Complexity**  
   - Time: O(s + a) where s is scan time, a is analysis time (varies by scope).  
   - Space: O(d + r) where d is database size, r is result storage (vulnerability data).

8. **Strengths**  
- Proactive: identifies vulnerabilities before deployment.
- Comprehensive: scans multiple layers (code, dependencies, infrastructure).
- Automation: automates security checks in CI/CD.

9. **Weaknesses / limitations**  
- False positives: may generate false positive findings.
- Coverage: may not detect all vulnerabilities.
- Noise: too many findings can cause alert fatigue.

10. **Compare with alternatives**  
    Alternatives: Manual Security Review, Penetration Testing, Security Audits, Vulnerability Assessment

11. **30-second explanation (your own words)**  
    Automatically scans code, dependencies, containers, and infrastructure for security vulnerabilities, misconfigurations, and threats, enabling proactive security management.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
