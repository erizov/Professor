# Build Automation

1. **Name of Algorithm**  
   Build Automation

2. **What problem does it solve? (1 sentence)**  
   Automates the process of compiling source code, running tests, packaging artifacts, and preparing software for deployment, reducing manual effort and ensuring consistent, reproducible builds.

3. **Intuition (plain-language explanation)**  
   Like an automated factory assembly line: instead of manually compiling code, running tests, and packaging (tedious, error-prone), build automation does it all automatically when you push code - just like a factory that automatically assembles products when materials arrive.

4. **Inputs & Outputs**  
   - Input: Source code, build configuration files (Makefile, build.gradle, package.json, etc.), dependencies, build tools.  
   - Output: Compiled binaries, packaged artifacts, test reports, deployment-ready software packages.

5. **Step-by-step description (5–10 lines max)**  
1. Detect changes: monitor source code repository for commits or changes.
2. Fetch dependencies: download required libraries, packages, or modules.
3. Compile code: transform source code into executable binaries or bytecode.
4. Run unit tests: execute automated tests to verify code correctness.
5. Package artifacts: bundle compiled code, dependencies, and resources into deployable packages (JAR, Docker image, etc.).
6. Run integration tests: test packaged artifacts in integrated environment.
7. Generate reports: create build reports, test results, and artifact metadata.
8. Store artifacts: save build outputs to artifact repository for deployment.

6. **Tiny example (hand-simulated)**  
   Java project: git push → build automation triggers → Maven downloads dependencies → compiles Java files → runs JUnit tests → packages JAR file → runs integration tests → uploads JAR to Nexus repository → build complete in 5 minutes (vs 30 minutes manual).

7. **Time & Space Complexity**  
   - Time: O(C + T + P) where C is compilation time, T is test execution time, P is packaging time (typically minutes for most projects).  
   - Space: O(S + D + A) where S is source code size, D is dependencies size, A is artifact size.

8. **Strengths**  
- Consistency: ensures reproducible builds across environments.
- Efficiency: reduces manual effort and human error.
- Fast feedback: provides quick validation of code changes.

9. **Weaknesses / limitations**  
- Setup overhead: requires initial configuration and maintenance.
- Build time: may take time for large projects.
- Dependency on tools: requires build tools and infrastructure.

10. **Compare with alternatives**  
    Alternatives: Manual Builds, Script-based Builds, Container Builds, Cloud Build Services

11. **30-second explanation (your own words)**  
    Automates the process of compiling source code, running tests, and packaging artifacts, reducing manual effort and ensuring consistent, reproducible builds.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
