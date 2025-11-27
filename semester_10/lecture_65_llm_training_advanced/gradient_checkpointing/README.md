# Gradient Checkpointing

## Учебные материалы

- [Школьный уровень](school.ru.md)
- [Университетский уровень](univer.ru.md)

## Algorithm Visualization

### Flowchart (ASCII)

```
Gradient Checkpointing Flowchart:

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
Gradient Checkpointing Step-by-Step Execution:

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

- [Python Implementation](/code/semester_10/lecture_65_llm_training_advanced/gradient_checkpointing/algorithm.py)
- [Java Implementation](/code/semester_10/lecture_65_llm_training_advanced/gradient_checkpointing/Algorithm.java)
- [Python Tests](/code/semester_10/lecture_65_llm_training_advanced/gradient_checkpointing/test_algorithm.py)

What problem does it solve? (1 sentence)  
   Reduces memory usage during backpropagation by trading computation for memory - storing only selected activations and recomputing others during backward pass, enabling training of larger models with limited GPU memory.

Intuition (plain-language explanation)  
   Like taking notes selectively: gradient checkpointing is like taking notes during a lecture - instead of writing down everything (storing all activations, uses lots of memory), you only write down key points (checkpoint activations) and reconstruct the details later when needed (recompute activations during backward pass) - you use more time (recomputation) but save space (memory), allowing you to handle longer lectures (larger models) with the same notebook (GPU memory).

Inputs & Outputs  

  - Input: Neural network, forward activations, memory budget, checkpoint strategy, recomputation schedule.  
  - Output: Memory-efficient training, reduced memory usage, larger model capacity, gradient computation.

Step-by-step description (5–10 lines max)  
Forward pass: perform forward pass through network.
Checkpoint: store activations only at selected checkpoints (every N layers).
Discard: discard non-checkpoint activations to save memory.
Backward pass: start backward pass from output.
Recompute: when needed, recompute activations from nearest checkpoint.
Compute gradients: compute gradients using recomputed activations.
Continue: continue backward pass, recomputing as needed.
Optimize: optimize checkpoint placement for memory-compute trade-off.
Validate: validate that gradients are computed correctly.
Train: train model with reduced memory footprint.

Tiny example (hand-simulated)  
   Gradient checkpointing: 100-layer transformer → memory: store all activations = 40GB → checkpointing: checkpoint every 10 layers → store: 10 checkpoints (4GB) → backward: recompute activations between checkpoints → memory: 4GB + recomputation overhead → result: 10x memory reduction, 30% compute increase → larger models trainable.

Time & Space Complexity  

  - Time: O(n + r) where n is forward pass time, r is recomputation time (typically 30-50% overhead).  
  - Space: O(m/c) where m is total activation memory, c is checkpoint frequency (reduced from O(m)).

Strengths  

- Memory efficiency: dramatically reduces memory usage (5-10x reduction).
- Larger models: enables training models that don't fit in memory otherwise.
- Flexibility: can adjust checkpoint frequency for memory-compute trade-off.

Weaknesses / limitations  

- Compute overhead: recomputation adds 30-50% training time.
- Complexity: requires careful checkpoint placement.
- Trade-off: must balance memory savings vs compute cost.

Compare with alternatives  
    Alternatives: Full Activation Storage, CPU Offloading, Model Parallelism, Reduced Batch Size

30-second explanation (your own words)  
    Reduces memory usage during backpropagation by trading computation for memory - storing only selected activations and recomputing others during backward pass, enabling training of larger models with limited GPU memory.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*


## References

- [Gradient Checkpointing - Wikipedia](https://en.wikipedia.org/wiki/Gradient%20Checkpointing)
