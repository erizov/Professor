# Circuit Breaker Pattern

**Category**: Deployment

**Time Complexity**: O(1)

**Space Complexity**: O(1)

## Implementation

## Introduction

Circuit Breaker is a fundamental algorithm.

This algorithm is widely used in computer science and software engineering for solving a specific class of problems efficiently. Understanding Circuit Breaker is essential for building performant and scalable applications.

## TL;DR (Too Long; Didn't Read)

**One Sentence**: A design pattern that prevents cascading failures by stopping requests to a failing service until it recovers.

**Time Complexity**: See complexity analysis below
**Space Complexity**: See complexity analysis below
**When to Use**: See 'Best Use Case' section
**When NOT to Use**: See 'Do Not Confuse With' section

## Learning Objectives
## Prerequisites

- Completed previous semesters
- Understanding of distributed systems concepts
- Knowledge of system design principles
- Familiarity with containerization (Docker)



By the end of this lecture, students will be able to:

1. Implement Circuit Breaker from scratch
2. Analyze time and space complexity using Big O notation
3. Identify when to use this algorithm vs. alternative approaches
4. Recognize common implementation pitfalls and how to avoid them
5. Apply this algorithm to solve real-world problems

### Short Description

A design pattern that prevents cascading failures by stopping requests to a failing service until it recovers.

**Key Characteristics:**
- **Time Complexity**: Varies
- **Space Complexity**: Varies
- **Stability**: N/A
- **Best Use Case**: General purpose


See algorithm.py and Algorithm.java


## Often Used Together With

Circuit Breaker is commonly used in combination with:

- **Factory**: Often combined for comprehensive solutions
- **Singleton**: Often combined for comprehensive solutions
- **Observer**: Often combined for comprehensive solutions
- **Strategy**: Often combined for comprehensive solutions

**Common Combinations:**
- Used together in production systems for optimal performance
- Complementary algorithms that solve related problems
- Often part of larger algorithmic frameworks




## Do Not Confuse With

- **Retry Pattern**: Circuit breaker stops requests on failure, retry pattern retries failed requests
- **Bulkhead**: Circuit breaker prevents cascading failures, bulkhead isolates resources
- **Timeout**: Circuit breaker opens on failures, timeout limits request duration

## Self-Assessment Questions

Test your understanding with these questions:

### Comprehension
1. Can you explain how Circuit Breaker works in your own words?
2. What is the key insight or technique that makes Circuit Breaker efficient?

### Analysis
3. What are the best-case, average-case, and worst-case time complexities?
4. When would you choose Circuit Breaker over alternative algorithms?

### Application
5. Can you implement Circuit Breaker from memory without looking at the code?
6. What real-world problem could you solve using Circuit Breaker?

### Debugging
7. What are the most common mistakes when implementing Circuit Breaker?
8. How would you test your Circuit Breaker implementation?

**Scoring**: If you can answer 6+ questions confidently, you've mastered this algorithm!


## Algorithm Visualization

*Visual diagram for Circuit Breaker would be added here*
*Consider using online visualization tools or drawing step-by-step execution*


## Practice Exercises

### Level 1: Understanding (Beginner)
1. Trace through Circuit Breaker step-by-step with input: [5, 2, 8, 1, 9]
2. Identify the base case(s) in Circuit Breaker
3. Explain why Circuit Breaker has its time complexity

### Level 2: Implementation (Intermediate)
4. Implement Circuit Breaker from scratch using only the function signature
5. Modify Circuit Breaker to handle edge cases (empty input, single element, etc.)
6. Add logging to track the algorithm's execution steps

### Level 3: Optimization (Advanced)
7. Optimize Circuit Breaker for a specific use case (e.g., nearly sorted data)
8. Implement a parallel or distributed version of Circuit Breaker
9. Compare Circuit Breaker performance with alternative algorithms on large datasets

### Level 4: Real-World Application (Expert)
10. Design a system that uses Circuit Breaker to solve a production problem
11. Create unit tests with 100% code coverage for Circuit Breaker
12. Write a technical blog post explaining Circuit Breaker to beginners


## Real-World Applications

- **Enterprise Applications**: Circuit Breaker is widely used in production systems
- **Performance Optimization**: Applied to improve system efficiency
- **System Design**: Integral part of scalable architecture patterns


## Common Misconceptions

❌ **WRONG**: "Circuit Breaker is the best solution for all problems"
✓ **CORRECT**: Circuit Breaker has specific use cases and trade-offs; choose algorithms based on requirements

❌ **WRONG**: "Circuit Breaker is too complex to understand"
✓ **CORRECT**: Circuit Breaker can be understood by breaking it down into smaller steps


## Examples of Implementation



This algorithm/pattern is implemented in the following frameworks and technologies:

### Spring Framework

```java
// Spring Cloud Circuit Breaker (Resilience4j)
@Service
public class ExternalServiceClient {
    private final CircuitBreaker circuitBreaker;
    
    public ExternalServiceClient() {
        circuitBreaker = CircuitBreaker.of("externalService", 
            CircuitBreakerConfig.custom()
                .failureRateThreshold(50)
                .waitDurationInOpenState(Duration.ofSeconds(30))
                .build());
    }
    
    public String callExternalService() {
        return circuitBreaker.executeSupplier(() -> {
            // Call external service
            return restTemplate.getForObject("http://external/api", String.class);
        });
    }
}
```

**Purpose**: Spring Framework uses this pattern for dependency injection, bean management, and enterprise application development.


