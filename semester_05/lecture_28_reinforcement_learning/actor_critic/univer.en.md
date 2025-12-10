# Actor Critic

# Univer

## 📋 Quick Summary

- **Purpose:** Actor Critic processes data according to Reinforcement Learning principles to achieve specific computational goals.
- **Complexity:** Varies time, Varies space
- **Category:** Reinforcement Learning
- **Key Idea:** Uses systematic approach to transform input data into desired output format.

> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.

The algorithm works by applying systematic transformations to input data based on Reinforcement Learning principles.

**ACTOR_CRITIC** = Remember: Understand the problem → Apply Reinforcement Learning principles → Process systematically → Verify results


## Complexity Analysis

**Time Complexity:** O(n) to O(n²) depending on implementation
- Analysis based on algorithm structure and data operations
- Best, average, and worst cases depend on input characteristics
- Consider input size and data distribution

**Space Complexity:** O(1) to O(n) depending on approach
- Additional memory for data structures and recursion
- Auxiliary space for temporary variables
- Consider in-place vs. extra space implementations

**Key Data Structures:** 
- Based on algorithm type: arrays, trees, graphs, hash tables, etc.


## Real-World Applications

Actor Critic is used in:
- **Reinforcement Learning Applications:** Core functionality in Reinforcement Learning systems
- **System Design:** Fundamental building blocks for larger systems
- **Performance Optimization:** Efficient solutions to common problems
- **Framework Integration:** Used in various software frameworks


## Conceptual Similarities

Actor Critic is conceptually similar to:
- Other algorithms in the Reinforcement Learning category
- Algorithms that use similar data structures and techniques
- Related algorithms that solve similar problems


## Related Algorithms

Actor Critic is often used in combination with:
- Related algorithms in the Reinforcement Learning category
- Complementary data structures that optimize performance
- Algorithms that solve related problems


## Key Implementation Details

```python
class ActorCritic:
    """Actor-Critic reinforcement learning algorithm."""

    def __init__(self, state_size: int, action_size: int, lr: float = 0.01):
        self.state_size = state_size
        self.action_size = action_size
        self.lr = lr
        # Simplified: using simple weight matrices
        self.actor_weights = [[0.0] * action_size for _ in range(state_size)]
        self.critic_weights = [0.0] * state_size

    def actor_forward(self, state: List[float]) -> List[float]:
        """Actor forward pass."""
        action_probs = [0.0] * self.action_size
        for a in range(self.action_size):
            action_probs[a] = sum(
                state[i] * self.actor_weights[i][a] for i in range(self.state_size)
            )
        # Softmax
        max_prob = max(action_probs)
        exp_probs = [math.exp(p - max_prob) for p in action_probs]
        sum_exp = sum(exp_probs)
        return [exp / sum_exp for exp in exp_probs]

    def critic_forward(self, state: List[float]) -> float:
        """Critic forward pass."""
        return sum(state[i] * self.critic_weights[i] for i in range(self.state_size))

    def update(
        self,
        state: List[float],
        action: int,
        reward: float,
        next_state: List[float],
        done: bool,
    ) -> None:
        """Update actor and critic."""
        import math

        # Critic update
        value = self.critic_forward(state)
        next_value = 0.0 if done else self.critic_forward(next_state)
        td_error = reward + 0.99 * next_value - value

        for i in range(self.state_size):
            self.critic_weights[i] += self.lr * td_error * state[i]

        # Actor update
        action_probs = self.actor_forward(state)
        for i in range(self.state_size):
            self.actor_weights[i][action] += (
                self.lr * td_error * action_probs[action] * state[i]
            )
```


## Common Application Errors

- **Incorrect handling of edge cases:** Solution: Test with empty input, single element, and boundary values.
- **Misunderstanding complexity implications:** Solution: Analyze time and space complexity for your use case.
- **Suboptimal implementation:** Solution: Profile and optimize based on actual usage patterns.
- **Incorrect assumptions about input:** Solution: Validate input format and constraints before processing.


## Recommended Literature

- "Introduction to Algorithms" (CLRS) - Comprehensive algorithm analysis
- "Algorithm Design Manual" by Steven Skiena
- "Algorithms" by Sedgewick and Wayne
- Research papers on algorithm optimization and analysis
- Framework documentation and implementation guides



---

## 🎯 Try It Yourself

**Try this example:**
```
Input: [example data]

Step 1: Initialize algorithm state
Step 2: Process input data
Step 3: Generate result

Output: [algorithm result]
```



## Common Mistakes

### ❌ Mistake 1: Not handling edge cases
**Solution:** Always check for empty input, single element, or boundary values before processing.

### ❌ Mistake 2: Incorrect initialization
**Solution:** Ensure all variables and data structures are properly initialized before the main algorithm loop.

### ❌ Mistake 3: Off-by-one errors in loops
**Solution:** Carefully verify loop bounds and termination conditions. Test with small examples to catch boundary issues.

### ❌ Mistake 4: Not validating input
**Solution:** Add input validation to ensure data is in expected format and within valid ranges.

### 💡 How to Avoid
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify variable values
- Review algorithm's key steps before implementing
- Test with edge cases (empty input, single element, boundary values)
- Trace through examples step-by-step
- Use debugging tools to verify your logic
- Review the algorithm's key steps before implementing