# Synthetic Monitoring

1. **Name of Algorithm**  
   Synthetic Monitoring

2. **What problem does it solve? (1 sentence)**  
   Proactively monitors application availability and performance by simulating user interactions and transactions, detecting issues before real users are affected.

3. **Intuition (plain-language explanation)**  
   Like a robot tester: synthetic monitoring is like having a robot that continuously tests your application - the robot performs the same actions real users would do (like logging in, browsing products, making purchases) from different locations around the world - if the robot finds a problem (like slow response or error), it alerts you immediately, even if no real users have encountered it yet - it's like having a 24/7 quality assurance tester that never sleeps.

4. **Inputs & Outputs**  
   - Input: Test scripts, monitoring locations, test scenarios, frequency, thresholds.  
   - Output: Synthetic test results, availability metrics, performance measurements, proactive alerts.

5. **Step-by-step description (5–10 lines max)**  
1. Define scenarios: define user interaction scenarios to test (login, checkout, search).
2. Create scripts: create test scripts that simulate user actions.
3. Deploy: deploy synthetic monitors in multiple locations.
4. Schedule: schedule tests to run at regular intervals (every 5 minutes).
5. Execute: synthetic monitors execute test scripts.
6. Measure: measure response times, availability, and functionality.
7. Validate: validate that application responds correctly.
8. Alert: alert if tests fail or performance degrades.
9. Report: generate reports on availability and performance trends.
10. Optimize: use insights to improve application reliability.

6. **Tiny example (hand-simulated)**  
   Synthetic monitoring: e-commerce site → scenario: user login → script: POST /login, check response → deploy: monitors in 5 regions → schedule: run every 5 min → execute: monitors test login → measure: response time 200ms, success rate 100% → alert: response time > 500ms → detect: login fails in Asia region → alert: proactive detection → synthetic monitoring operational.

7. **Time & Space Complexity**  
   - Time: O(s) where s is scenario execution time (varies by test complexity).  
   - Space: O(r) where r is number of test results (result storage).

8. **Strengths**  
- Proactive: detects issues before real users are affected.
- Coverage: tests from multiple geographic locations.
- Consistency: provides consistent monitoring regardless of user traffic.

9. **Weaknesses / limitations**  
- Cost: running synthetic tests continuously can be expensive.
- Limited: may not catch all real user scenarios.
- Maintenance: test scripts need maintenance as application changes.

10. **Compare with alternatives**  
    Alternatives: Real User Monitoring, Uptime Monitoring, Health Checks, Load Testing

11. **30-second explanation (your own words)**  
    Proactively monitors application availability and performance by simulating user interactions and transactions, detecting issues before real users are affected.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
