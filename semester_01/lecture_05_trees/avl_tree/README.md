# AVL Tree

1. **Name of Algorithm**  

## Code Files


## Algorithm Visualization

### Flowchart (ASCII)


```
AVL Tree Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Initialize │
│    root     │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Node       ├──────┐
│  exists?    │      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│  Process    │      │
│   node      │      │
└──────┬──────┘      │
       │             │
       ▼             │
┌─────────────┐      │
│  Traverse   │      │
│  children   │      │
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
AVL Tree Step-by-Step Execution:

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
- [Python Implementation](semester_01/lecture_05_trees/avl_tree/algorithm.py)
- [Java Implementation](semester_01/lecture_05_trees/avl_tree/Algorithm.java)
- [Python Tests](semester_01/lecture_05_trees/avl_tree/test_algorithm.py)

