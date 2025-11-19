# Human Evaluation for LLMs

1. **Name of Algorithm**  
   Human Evaluation for LLMs

2. **What problem does it solve? (1 sentence)**  
   Assesses LLM outputs using human judges to evaluate quality, relevance, fluency, and other subjective aspects that automated metrics may miss, providing comprehensive quality assessment.

3. **Intuition (plain-language explanation)**  
Like peer review: human evaluation is like having experts review work - while automated tests (metrics) can check some things (like grammar), humans can judge quality, relevance, and appropriateness that machines can't - just as peer reviewers evaluate research papers for quality and contribution, human evaluators assess LLM outputs for quality, making sure they're not just technically correct but actually good and useful.

4. **Inputs & Outputs**  
   - Input: LLM outputs, evaluation criteria, human judges, rating scales, evaluation tasks.  
   - Output: Human ratings, quality scores, evaluation reports, inter-annotator agreement, qualitative feedback.

5. **Step-by-step description (5–10 lines max)**  
1. Design: design evaluation task and criteria (quality, relevance, fluency, etc.).
2. Recruit: recruit human evaluators (experts or crowd workers).
3. Train: train evaluators on criteria and rating scales.
4. Present: present LLM outputs to evaluators for assessment.
5. Rate: evaluators rate outputs on defined criteria.
6. Collect: collect ratings and qualitative feedback.
7. Analyze: analyze ratings for consistency and patterns.
8. Compute: compute inter-annotator agreement (reliability).
9. Aggregate: aggregate ratings across evaluators and outputs.
10. Report: report human evaluation results with insights.

6. **Tiny example (hand-simulated)**  
   Human evaluation: task: evaluate chatbot responses → criteria: helpfulness (1-5), relevance (1-5), fluency (1-5) → evaluators: 3 human judges → rate: 100 responses → aggregate: average helpfulness = 4.2, relevance = 4.0, fluency = 4.5 → agreement: 0.85 (high) → report: LLM performs well on human evaluation → human evaluation complete.

7. **Time & Space Complexity**  
   - Time: O(n·e·r) where n is outputs, e is evaluators, r is rating time per output (human time).  
   - Space: O(n + f) where n is outputs, f is feedback storage.

8. **Strengths**  
- Quality: captures subjective aspects of quality.
- Comprehensive: evaluates multiple dimensions of output quality.
- Insights: provides qualitative insights and feedback.

9. **Weaknesses / limitations**  
- Cost: human evaluation is expensive and time-consuming.
- Scalability: difficult to scale to large numbers of outputs.
- Consistency: requires careful design to ensure consistency.

10. **Compare with alternatives**  
    Alternatives: Automated Metrics, Hybrid Evaluation, Crowdsourcing, Expert Evaluation

11. **30-second explanation (your own words)**  
    Assesses LLM outputs using human judges to evaluate quality, relevance, fluency, and other subjective aspects that automated metrics may miss, providing comprehensive quality assessment.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
