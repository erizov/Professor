# Chain of Thought (CoT)

1. **Name of Algorithm**  
   Chain of Thought (CoT)

2. **What problem does it solve? (1 sentence)**  
Improves LLM reasoning by prompting the model to generate intermediate reasoning steps before producing the final answer, enabling better performance on complex reasoning tasks that require multi-step problem solving.

3. **Intuition (plain-language explanation)**  
   Like showing your work in math class: instead of just giving the answer, the model is prompted to think step-by-step (show reasoning) before answering - this helps it solve complex problems by breaking them into smaller steps, just like humans do.

4. **Inputs & Outputs**  
   - Input: Problem/question, few-shot examples with step-by-step reasoning, CoT prompt template.  
   - Output: Step-by-step reasoning process, final answer derived from reasoning steps.

5. **Step-by-step description (5–10 lines max)**  
1. Provide examples: include few-shot examples in prompt showing step-by-step reasoning (e.g., 'Step 1: ... Step 2: ... Answer: ...').
2. Format prompt: structure prompt to encourage reasoning (e.g., 'Let's think step by step' or 'First, we need to...').
3. Model generates reasoning: LLM produces intermediate reasoning steps before final answer.
4. Extract answer: parse final answer from model's reasoning chain.
5. Validate reasoning: optionally check if reasoning steps are logical and lead to answer.
6. Use for complex tasks: apply to tasks requiring multi-step reasoning (math, logic, planning).

6. **Tiny example (hand-simulated)**  
   Math problem: 'A store has 15 apples. They sell 3, then buy 8 more. How many apples do they have?' → CoT prompt: 'Let's think step by step. Step 1: Start with 15 apples. Step 2: After selling 3, we have 15 - 3 = 12 apples. Step 3: After buying 8 more, we have 12 + 8 = 20 apples. Answer: 20.'

7. **Time & Space Complexity**  
   - Time: O(n) where n is length of reasoning chain (longer output than direct answer, but improves accuracy).  
   - Space: O(n) for storing reasoning steps where n is number of steps and tokens per step.

8. **Strengths**  
- Improves reasoning: significantly better performance on complex reasoning tasks.
- Interpretable: reasoning steps make model's thinking process visible.
- No training required: works with pre-trained models through prompting.

9. **Weaknesses / limitations**  
- Longer outputs: generates more tokens, increasing latency and cost.
- May hallucinate: model may generate plausible-sounding but incorrect reasoning.
- Requires careful prompting: effectiveness depends on prompt design.

10. **Compare with alternatives**  
    Alternatives: Direct Answering, Zero-shot Learning, Fine-tuning, Self-Consistency

11. **30-second explanation (your own words)**  
    Improves LLM reasoning by prompting the model to generate intermediate reasoning steps before producing the final answer, enabling better performance on complex multi-step reasoning tasks.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
