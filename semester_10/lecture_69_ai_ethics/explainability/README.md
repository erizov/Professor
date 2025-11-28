# Explainability

## Учебные материалы

- [Школьный уровень](school.ru.md)
- [Университетский уровень](univer.ru.md)

## Algorithm Visualization

### Flowchart (ASCII)

```
Explainability Flowchart:

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
Explainability Step-by-Step Execution:

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

- [Python Implementation](/code/semester_10/lecture_69_ai_ethics/explainability/algorithm.py)
- [Java Implementation](/code/semester_10/lecture_69_ai_ethics/explainability/Algorithm.java)
- [Python Tests](/code/semester_10/lecture_69_ai_ethics/explainability/test_algorithm.py)

What problem does it solve? (1 sentence)  
   Makes AI model decisions understandable and interpretable to humans, providing explanations for predictions and enabling users to understand, trust, and debug AI systems.

Intuition (plain-language explanation)  
   Like explaining decisions: Explainability is like explaining your decisions to someone - instead of just saying 'I decided X' (black box), you explain why (reasons, factors) so they understand - just as people explain their decisions, AI systems should explain their predictions so users can understand and trust them.

Inputs & Outputs  

  - Input: AI models, predictions, input data, explanation methods, user queries, explanation requirements.  
  - Output: Explanations, interpretable predictions, feature importance, decision rationales, explanation reports.

Step-by-step description (5–10 lines max)  
Predict: make model prediction.
Extract: extract relevant information for explanation.
Explain: generate explanation using explanation method (LIME, SHAP, etc.).
Format: format explanation for users.
Present: present explanation clearly.
Validate: validate explanation accuracy.
Iterate: iterate to improve explanations.
Customize: customize explanations for different users.
Monitor: monitor explanation quality.
Improve: continuously improve explainability.

Tiny example (hand-simulated)  
   Explainability: model: loan approval → predict: loan denied → explain: 'Denied due to: low credit score (600), high debt-to-income ratio (45%), recent late payments' → result: user understands decision → Explainability successful.

Time & Space Complexity  

  - Time: O(m + e) where m is model inference time, e is explanation generation time (varies by method).  
  - Space: O(m + e) where m is model storage, e is explanation storage (explanation data).

Strengths  

- Trust: increases trust in AI systems through transparency.
- Debugging: enables debugging of AI models.
- Compliance: helps meet explainability requirements.

Weaknesses / limitations  

- Accuracy: explanations may not always be perfectly accurate.
- Complexity: explaining complex models is challenging.
- Trade-offs: may require trade-offs with model performance.

Compare with alternatives  
    Alternatives: Black Box Models, Interpretable Models, Post-Hoc Explanations, Inherently Explainable

30-second explanation (your own words)  
    Makes AI model decisions understandable and interpretable to humans, providing explanations for predictions and enabling users to understand, trust, and debug AI systems.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*


## References

- [Explainable artificial intelligence](https://en.wikipedia.org/wiki/Explainable_artificial_intelligence) - Wikipedia


## Real-World Applications

- Search engines and indexing
- Database lookups

- Search engines and indexing
- Database lookups

- Search engines and indexing
- Database lookups
## Historical Context

The main focus is on the reasoning behind the decisions or predictions made by the AI algorithms, to make them more understandable and transparent
