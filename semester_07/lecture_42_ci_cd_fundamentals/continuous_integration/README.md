# Continuous Integration (CI)

1. **Name of Algorithm**  
   Continuous Integration (CI)

2. **What problem does it solve? (1 sentence)**  
   Automatically builds and tests code changes whenever developers commit to version control, enabling early detection of integration issues and maintaining code quality.

3. **Intuition (plain-language explanation)**  
   Like a quality checkpoint on an assembly line: every time code is committed (like adding a part), CI automatically builds and tests it (checks if it fits) - if something breaks, you know immediately, not days later when everything is integrated.

4. **Inputs & Outputs**  
   - Input: Code commits, CI configuration (Jenkinsfile, .github/workflows, GitLab CI), test suites, build scripts.  
   - Output: Build status, test results, code quality reports, deployment artifacts (if tests pass).

5. **Step-by-step description (5–10 lines max)**  
1. Monitor repository: CI server watches version control for new commits.
2. Trigger build: automatically start build process when code is pushed.
3. Checkout code: retrieve latest code from repository.
4. Install dependencies: set up build environment and install required packages.
5. Run build: compile code, package artifacts.
6. Execute tests: run automated test suite (unit, integration, etc.).
7. Check quality: run code quality checks (linting, static analysis).
8. Report results: notify developers of build status (pass/fail) via email, Slack, etc.
9. Deploy (optional): if all checks pass, automatically deploy to staging environment.

6. **Tiny example (hand-simulated)**  
   Developer pushes code → CI triggers → checkout code → install dependencies → build → run 500 unit tests → run integration tests → code quality checks → all pass → deploy to staging → notify team: 'Build #1234 passed, deployed to staging'.

7. **Time & Space Complexity**  
   - Time: O(B + T) where B is build time, T is test execution time (typically 5-30 minutes depending on project size).  
   - Space: O(C + D + A) where C is code size, D is dependencies, A is artifacts (build workspace requirements).

8. **Strengths**  
- Early detection: catches integration issues immediately.
- Code quality: ensures all code passes tests before merging.
- Team confidence: provides fast feedback on code changes.

9. **Weaknesses / limitations**  
- False positives: may fail due to flaky tests or environment issues.
- Resource usage: requires CI infrastructure and compute resources.
- Maintenance: requires maintaining CI configuration and test suites.

10. **Compare with alternatives**  
    Alternatives: Manual Integration, Scheduled Builds, Pre-commit Hooks, Pull Request Checks

11. **30-second explanation (your own words)**  
    Automatically builds and tests code changes whenever developers commit to version control, enabling early detection of integration issues and maintaining code quality.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
