# Bubble Sort

## Учебные материалы

- [Школьный уровень](school.ru.md)
- [Университетский уровень](univer.ru.md)

## Algorithm Visualization

### Flowchart (ASCII)

```
Bubble Sort Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Initialize  │
│   array     │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Compare    ├──────┐
│  elements?  │      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│   Swap if   │      │
│  needed     │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│   Sorted?   │
└──────┬──────┘
       │ No
       └──────┐
              │
       Yes    │
       │      │
       ▼      ▼
┌─────────────┐
│    End      │
└─────────────┘
```

### Flowchart (SVG)

![Bubble Sort Flowchart](semester_01/lecture_01_sorting_fundamentals/bubble_sort/visualizations/flowchart.svg)

### Step-by-Step Execution

```
Bubble Sort Step-by-Step Execution:

Input: [5, 3, 2, 8, 1]

Pass 1:
[5, 3, 2, 8, 1]
 ↑  ↑
Swap: 5 > 3
[3, 5, 2, 8, 1]
    ↑  ↑
Swap: 5 > 2
[3, 2, 5, 8, 1]
       ↑  ↑
No swap: 5 < 8
[3, 2, 5, 8, 1]
          ↑  ↑
Swap: 8 > 1
Result: [3, 2, 5, 1, 8]

Pass 2:
[3, 2, 5, 1, 8]
 ↑  ↑
Swap: 3 > 2
[2, 3, 5, 1, 8]
    ↑  ↑
No swap: 3 < 5
[2, 3, 5, 1, 8]
       ↑  ↑
Swap: 5 > 1
Result: [2, 3, 1, 5, 8]

Final: [1, 2, 3, 5, 8]
```

### Interactive Flowchart (Mermaid)

```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize array]
    Init --> Compare{Compare elements}
    Compare -->|Yes| Swap[Swap if needed]
    Swap --> Check{More elements?}
    Check -->|Yes| Compare
    Check -->|No| Sorted{Array sorted?}
    Sorted -->|No| Compare
    Sorted -->|Yes| End([End])
```

> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.

- [Python Implementation](/code/semester_01/lecture_01_sorting_fundamentals/bubble_sort/algorithm.py)
- [Java Implementation](/code/semester_01/lecture_01_sorting_fundamentals/bubble_sort/Algorithm.java)
- [Python Tests](/code/semester_01/lecture_01_sorting_fundamentals/bubble_sort/test_algorithm.py)


## References

- [Bubble sort](https://en.wikipedia.org/wiki/Bubble_sort) - Wikipedia


## Real-World Applications

- Database query optimization
- Operating system process scheduling

- Database query optimization
- Operating system process scheduling

- Database query optimization
- Operating system process scheduling
## Historical Context

Bubble sort, sometimes referred to as sinking sort, is a simple sorting algorithm that repeatedly steps through the input list element by element, comparing the current element with the one after it, swapping their values if needed
