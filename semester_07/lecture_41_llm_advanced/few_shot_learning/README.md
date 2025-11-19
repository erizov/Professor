# Few-Shot Learning

1. **Name of Algorithm**  
   Few-Shot Learning

2. **What problem does it solve? (1 sentence)**  
   Enables LLMs to learn new tasks from just a few examples provided in the prompt, allowing task adaptation without fine-tuning by leveraging in-context learning capabilities.

3. **Intuition (plain-language explanation)**  
   Like learning from examples: show the model a few examples of what you want (input-output pairs) in the prompt, and it learns the pattern - just like showing someone 3 examples of how to format dates, they can then format new dates correctly.

4. **Inputs & Outputs**  
   - Input: Task examples (input-output pairs), test input, prompt template, number of examples (typically 1-10).  
   - Output: Task-specific output following the pattern shown in examples.

5. **Step-by-step description (5–10 lines max)**  
1. Select examples: choose representative examples that demonstrate the task clearly.
2. Format examples: structure examples as input-output pairs (e.g., 'Input: X, Output: Y').
3. Construct prompt: combine examples with test input in prompt (few-shot examples + test input).
4. Order examples: arrange examples logically (may affect performance).
5. Pass to model: send prompt to LLM for inference.
6. Model learns pattern: LLM identifies pattern from examples and applies to test input.
7. Generate output: model produces output following the pattern from examples.
8. Evaluate: check if output matches expected format and quality.

6. **Tiny example (hand-simulated)**  
   Sentiment classification: prompt: 'Examples: Text: Great movie! Sentiment: positive. Text: Boring film. Sentiment: negative. Text: It was okay. Sentiment: neutral. Text: Amazing experience! Sentiment:' → model outputs 'positive' (learned pattern from examples).

7. **Time & Space Complexity**  
   - Time: O(n) where n is prompt length (includes examples + test input), inference time depends on model size.  
   - Space: O(k·s) where k is number of examples, s is average example size (consumes context window).

8. **Strengths**  
- No training: works with pre-trained models without fine-tuning.
- Fast adaptation: can adapt to new tasks quickly with just examples.
- Flexible: easy to update by changing examples in prompt.

9. **Weaknesses / limitations**  
- Limited examples: performance may degrade with very few or poor examples.
- Context limits: examples consume context window, limiting available space.
- Example sensitivity: quality and order of examples affect performance.

10. **Compare with alternatives**  
    Alternatives: Zero-shot Learning, Fine-tuning, Prompt Engineering, In-context Learning

11. **30-second explanation (your own words)**  
    Enables LLMs to learn new tasks from just a few examples provided in the prompt, allowing task adaptation without fine-tuning through in-context learning.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
