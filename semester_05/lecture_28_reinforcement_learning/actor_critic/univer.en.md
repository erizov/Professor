# Actor Critic

# Univer

## 📋 Quick Summary

- **Purpose:** Actor Critic solves [algorithm purpose] by [key approach].
- **Complexity:** Varies
- **Category:** Reinforcement Learning
- **Key Idea:** Actor Critic uses [key technique] to [achieve goal].

Actor Critic is an algorithm that [brief description of what it does and why it's important].

The algorithm works by [key steps in the process].

**ACTOR_CRITIC** = Remember: [key steps]


## Complexity Analysis

**Time Complexity:** O(episodes*steps)
- The algorithm's performance scales according to this complexity class
- Best, average, and worst cases may vary based on input characteristics

**Space Complexity:** O(2*network_params)
- Indicates the amount of additional memory required during execution

**Key Data Structures:** hash table/dictionary

## Real-World Applications

Actor Critic is used in:
- Software development frameworks
- System optimization
- Data processing pipelines
- Algorithm libraries

## Conceptual Similarities

This algorithm shares conceptual similarities with other algorithms in the Reinforcement Learning category, following similar design patterns and optimization strategies.

## Related Algorithms

Actor Critic is often used in combination with:
- Complementary algorithms for preprocessing or post-processing
- Data structures that optimize its performance
- Other algorithms in the same complexity class

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

- **Incorrect handling of edge cases:** [Algorithm-specific edge case]. Solution: [Specific solution].

- **Misunderstanding complexity implications:** [Algorithm-specific complexity issue]. Solution: [Specific solution].

- **Suboptimal implementation:** [Algorithm-specific performance issue]. Solution: [Specific solution].

- **Incorrect assumptions about input:** [Algorithm-specific input assumption]. Solution: [Specific solution].

- **Not considering alternatives:** [Algorithm-specific alternative consideration]. Solution: [Specific solution].


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