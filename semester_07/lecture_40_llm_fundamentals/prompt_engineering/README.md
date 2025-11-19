# Prompt Engineering

1. **Name of Algorithm**  
   Prompt Engineering

2. **What problem does it solve? (1 sentence)**  
   Designs and optimizes input prompts (instructions, examples, context) to guide LLM behavior and improve output quality without modifying model weights, enabling task-specific performance through careful prompt design.

3. **Intuition (plain-language explanation)**  
   Like giving clear instructions to a smart assistant: instead of retraining the model, you craft the perfect prompt (instructions, examples, format) - the model reads your prompt and follows it to produce better results, like a chef following a detailed recipe.

4. **Inputs & Outputs**  
   - Input: Task description, example inputs/outputs, desired output format, model constraints, few-shot examples.  
   - Output: Optimized prompts, improved model outputs, task-specific performance without fine-tuning.

5. **Step-by-step description (5–10 lines max)**  
1. Define task: clearly specify what you want the model to do (classification, generation, extraction, etc.).
2. Write base prompt: create initial prompt with task description and instructions.
3. Add examples: include few-shot examples showing desired input-output pairs.
4. Specify format: clearly indicate desired output format (JSON, list, paragraph, etc.).
5. Add constraints: specify constraints (length limits, style, tone, domain-specific rules).
6. Test prompt: run prompt on sample inputs and evaluate outputs.
7. Iterate: refine prompt based on results (add examples, clarify instructions, adjust format).
8. Optimize: experiment with prompt variations (order of examples, wording, structure) to improve performance.
9. Deploy: use optimized prompt in production for consistent results.

6. **Tiny example (hand-simulated)**  
   Sentiment analysis: prompt: 'Classify the sentiment of the following review as positive or negative. Examples: Review: Great product! Sentiment: positive. Review: Terrible quality. Sentiment: negative. Review: The movie was okay. Sentiment:' → model outputs 'neutral' (or 'negative' depending on training).

7. **Time & Space Complexity**  
   - Time: O(1) for prompt design (one-time effort), O(n) for inference where n is prompt + input length.  
   - Space: O(P) for prompt storage where P is prompt length, O(n) for input/output sequences.

8. **Strengths**  
- No training required: works with pre-trained models without fine-tuning.
- Fast iteration: can quickly test and refine prompts.
- Interpretable: prompts are human-readable and explainable.

9. **Weaknesses / limitations**  
- Limited control: cannot fundamentally change model behavior.
- Prompt sensitivity: small changes can significantly affect outputs.
- Token limits: long prompts consume context window.

10. **Compare with alternatives**  
    Alternatives: Fine-tuning, Few-shot Learning, In-context Learning, Prompt Tuning

11. **30-second explanation (your own words)**  
    Designs and optimizes input prompts to guide LLM behavior and improve output quality without modifying model weights, enabling task-specific performance through careful prompt design and few-shot examples.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
