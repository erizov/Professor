# Conditional Execution in CI/CD

1. **Name of Algorithm**  

## Code Files


## Algorithm Visualization

### Flowchart (ASCII)


```
Conditional Execution in CI/CD Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Initialize │
│   data      │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Process   ├──────┐
│  condition?│      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│  Execute   │      │
│  operation │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│    End      │
└─────────────┘
```


### Step-by-Step Execution


```
Conditional Execution in CI/CD Step-by-Step Execution:

Input: [example data]

Step 1: Initialize
State: [initial state]

Step 2: Process
State: [intermediate state]

Step 3: Finalize
State: [final state]

Result: [output]
```


### Interactive Flowchart (Mermaid)


```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize data]
    Init --> Process{Process condition}
    Process -->|True| Execute[Execute operation]
    Execute --> Done{Complete?}
    Done -->|No| Process
    Done -->|Yes| End([End])
    Process -->|False| End
```


> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.
- [Python Implementation](semester_11/lecture_71_cicd_advanced/conditional_execution/algorithm.py)
- [Java Implementation](semester_11/lecture_71_cicd_advanced/conditional_execution/Algorithm.java)
- [Python Tests](semester_11/lecture_71_cicd_advanced/conditional_execution/test_algorithm.py)


   Conditional Execution in CI/CD

2. **What problem does it solve? (1 sentence)**  
Enables CI/CD pipelines to execute steps conditionally based on conditions like branch, file changes, environment, or custom logic, making pipelines more efficient and flexible.

3. **Intuition (plain-language explanation)**  
Like conditional statements: Conditional Execution in CI/CD is like if-else statements in code - you only run certain steps if conditions are met (like 'only run tests on main branch' or 'only deploy if tests pass') - this makes pipelines smarter and more efficient, skipping unnecessary steps and adapting to different scenarios.

4. **Inputs & Outputs**  
   - Input: Pipeline steps, conditions, branch information, file changes, environment variables, custom logic.  
- Output: Conditionally executed steps, efficient pipelines, flexible workflows, optimized builds.

5. **Step-by-step description (5–10 lines max)**  
1. Define conditions: define conditions for step execution (branch, file paths, environment).
2. Evaluate: evaluate conditions before each step.
3. Check: check if condition is met (true/false).
4. Execute: execute step if condition is true.
5. Skip: skip step if condition is false.
6. Chain: chain conditions for complex logic (AND, OR, NOT).
7. Optimize: optimize pipeline by skipping unnecessary steps.
8. Log: log which steps were executed and why.
9. Validate: validate conditional logic for correctness.
10. Iterate: iterate to improve conditional execution.

6. **Tiny example (hand-simulated)**  
   Conditional Execution: branch: feature-branch → condition: only run tests if Python files changed → check: Python files changed? → yes: run tests → condition: only deploy if on main branch → check: main branch? → no: skip deployment → result: efficient pipeline → Conditional Execution successful.

7. **Time & Space Complexity**  
   - Time: O(c + s) where c is condition evaluation time, s is step execution time (only executed steps).  
   - Space: O(p + v) where p is pipeline definition, v is variable storage.

8. **Strengths**  
- Efficiency: skips unnecessary steps, saving time and resources.
- Flexibility: adapts pipeline behavior to different scenarios.
- Cost: reduces CI/CD costs by avoiding unnecessary executions.

9. **Weaknesses / limitations**  
- Complexity: conditional logic can become complex.
- Debugging: conditional execution can make debugging harder.
- Testing: requires testing all conditional paths.

10. **Compare with alternatives**  
    Alternatives: Always Execute, Manual Triggers, Separate Pipelines, Matrix Builds

11. **30-second explanation (your own words)**  
Enables CI/CD pipelines to execute steps conditionally based on conditions like branch, file changes, environment, or custom logic, making pipelines more efficient and flexible.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
