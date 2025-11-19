# Bias Detection in LLMs

1. **Name of Algorithm**  
   Bias Detection in LLMs

2. **What problem does it solve? (1 sentence)**  
Identifies and measures biases in LLM outputs across demographic groups, topics, and contexts, helping ensure fair and equitable model behavior.

3. **Intuition (plain-language explanation)**  
Like checking for unfair treatment: bias detection is like checking if a hiring process treats all candidates fairly - you test the system (LLM) with different inputs representing different groups (demographics, topics) and see if it produces different quality or fairness of outputs - if it does, you've found bias (unfair treatment), which needs to be fixed to ensure everyone gets fair treatment.

4. **Inputs & Outputs**  
   - Input: LLM model, test prompts, demographic groups, bias metrics, evaluation datasets.  
   - Output: Bias measurements, bias reports, demographic disparities, fairness metrics, bias analysis.

5. **Step-by-step description (5–10 lines max)**  
1. Define groups: define demographic or topic groups to test (gender, race, religion, etc.).
2. Create tests: create test prompts that vary only by group membership.
3. Generate: generate LLM outputs for all test prompts.
4. Measure: measure outputs for bias indicators (sentiment, toxicity, quality differences).
5. Compare: compare outputs across groups for disparities.
6. Quantify: quantify bias using metrics (disparate impact, calibration differences).
7. Analyze: analyze bias patterns and root causes.
8. Report: report bias findings with examples and severity.
9. Prioritize: prioritize biases by impact and severity.
10. Track: track bias over time and model versions.

6. **Tiny example (hand-simulated)**  
   Bias detection: test: 'A [profession] is' → groups: male vs female names → generate: 'A doctor is' (male name) → 'A nurse is' (female name) → measure: sentiment, associations → result: gender bias detected (doctors associated with males, nurses with females) → bias detection successful.

7. **Time & Space Complexity**  
   - Time: O(g·t) where g is number of groups, t is test cases per group (evaluation time).  
   - Space: O(d + m) where d is test dataset size, m is model size.

8. **Strengths**  
- Fairness: ensures models treat all groups fairly.
- Transparency: reveals hidden biases in model behavior.
- Accountability: enables accountability for model fairness.

9. **Weaknesses / limitations**  
- Coverage: may not detect all types of bias.
- Complexity: bias can be subtle and context-dependent.
- Mitigation: detecting bias doesn't automatically fix it.

10. **Compare with alternatives**  
    Alternatives: Fairness Audits, Disparate Impact Analysis, Demographic Parity, Equalized Odds

11. **30-second explanation (your own words)**  
Identifies and measures biases in LLM outputs across demographic groups, topics, and contexts, helping ensure fair and equitable model behavior.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
