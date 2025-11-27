# Recursive Queries

## Учебные материалы

- [Школьный уровень](school.ru.md)
- [Университетский уровень](univer.ru.md)

## Algorithm Visualization

### Flowchart (ASCII)

```
Recursive Queries Flowchart:

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
Recursive Queries Step-by-Step Execution:

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

- [Python Implementation](/code/semester_15/lecture_103_sql_advanced_topics/recursive_queries/algorithm.py)
- [Java Implementation](/code/semester_15/lecture_103_sql_advanced_topics/recursive_queries/Algorithm.java)
- [Python Tests](/code/semester_15/lecture_103_sql_advanced_topics/recursive_queries/test_algorithm.py)

What problem does it solve? (1 sentence)  
Implements recursive queries algorithm.

Intuition (plain-language explanation)  
Recursive Queries is a fundamental algorithm in computer science.

Inputs & Outputs  

  - Input: Algorithm-specific inputs  
  - Output: Algorithm-specific outputs

Step-by-step description (5–10 lines max)  
Initialize data structures
Process input according to algorithm logic
Return computed result

Tiny example (hand-simulated)  
   Example: Recursive Queries applied to sample data.

Time & Space Complexity  

  - Time: Varies  
  - Space: Varies

Strengths  

- Efficient for specific use cases

Weaknesses / limitations  

- May have limitations in certain scenarios

Compare with alternatives  
    Alternatives: Related algorithms

30-second explanation (your own words)  
    Recursive Queries solves computational problems efficiently.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*


## References

- [Recursive Queries - Wikipedia](https://en.wikipedia.org/wiki/Recursive%20Queries)
