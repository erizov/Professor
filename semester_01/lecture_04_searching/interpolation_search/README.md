# Interpolation Search

Name of Algorithm  

## Code Files


## Algorithm Visualization

### Flowchart (ASCII)


```
Interpolation Search Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Get search │
│    target   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Check     ├──────┐
│  current   │      │
│  element?  │      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│   Move to   │      │
│   next      │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│   Found?    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    End      │
└─────────────┘
```


### Step-by-Step Execution


```
Interpolation Search Step-by-Step Execution:

Array: [1, 3, 5, 7, 9, 11]
Target: 7

Step 1: Check middle (index 2, value 5)
[1, 3, 5, 7, 9, 11]
         ↑
5 < 7, search right

Step 2: Check middle of right half (index 4, value 9)
[7, 9, 11]
    ↑
9 > 7, search left

Step 3: Check remaining (index 3, value 7)
[7]
 ↑
Found! Index 3
```


### Interactive Flowchart (Mermaid)


```mermaid
flowchart TD
    Start([Start]) --> Init[Get search target]
    Init --> Check{Check current element}
    Check -->|Match| Found([Found])
    Check -->|No match| Next[Move to next]
    Next --> More{More elements?}
    More -->|Yes| Check
    More -->|No| NotFound([Not Found])
```


> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.
- [Python Implementation](/code/semester_01/lecture_04_searching/interpolation_search/algorithm.py)
- [Java Implementation](/code/semester_01/lecture_04_searching/interpolation_search/Algorithm.java)
- [Python Tests](/code/semester_01/lecture_04_searching/interpolation_search/test_algorithm.py)

