# Factory Method Pattern

**Category**: Creational Pattern

**Time Complexity**: O(1)

**Space Complexity**: O(1)

## Implementation

## Introduction

Factory addresses specific computational challenges.

This technique is applied in various domains to solve specific problems efficiently. Understanding this approach enables developers to solve related problems effectively.

## TL;DR

**One Sentence**: A creational design pattern that provides an interface for creating objects without specifying their exact classes.

**Time Complexity**: See complexity analysis below
**Space Complexity**: See complexity analysis below
**When to Use**: See 'Best Use Case' section
**When NOT to Employ**: See 'Do Not Confuse With' section

## Learning Objectives

## Prerequisites

- Completed Semester 1 algorithms course
- Understanding of object-oriented programming concepts
- Familiarity with design principles (SOLID)
- Knowledge of interfaces, inheritance, and polymorphism

By the end of this lecture, students will be able to:

1. Implement Factory from scratch
2. Analyze time and space complexity using Big O notation
3. Identify when to employ this algorithm vs. alternative approaches
4. Recognize common implementation pitfalls and how to avoid them
5. Apply this algorithm to tackle real-world problems
6. Recognize when this pattern is appropriate in system design

### Short Description

A creational design pattern that provides an interface for creating objects without specifying their exact classes. Addresses object creation complexity, dependency management, and runtime object selection. Example: Creating different payment processors (CreditCard, PayPal) based on user selection without exposing deployment details. Operates by delegating object instantiation to factory methods that return appropriate concrete implementations.

**Key Characteristics:**
- **Time Complexity**: Varies
- **Space Complexity**: Varies
- **Stability**: N/A

## Often Used Together With

Factory is used in combination with:

- **Singleton**: Often combined for comprehensive solutions

**Common Combinations:**
- Employed together in production systems for optimal performance
- Complementary algorithms that tackle related problems
- Often part of larger algorithmic frameworks

## Do Not Confuse With

- **Abstract Factory**: Factory creates single product type, abstract factory creates families of products
- **Builder Pattern**: Factory creates objects directly, builder constructs complex objects step by step
- **Singleton**: Factory creates multiple instances, singleton ensures single instance

## Self-Assessment Questions

Test your understanding with these questions:

### Comprehension

1. Can you explain how Factory works in your own words?
2. What is the key insight or technique that makes Factory efficient?

### Analysis

3. What are the best-case, average-case, and worst-case time complexities?
4. When would you choose Factory over alternative algorithms?

### Application

5. Can you implement Factory from memory without looking at the code?
6. What real-world problem could youaddresse using Factory?

### Debugging

7. What are the most common mistakes when implementing Factory?
8. How would you test your Factory deployment?

**Scoring**: If you can answer 6+ questions confidently, you've mastered this approach!

## Strategy Visualization

*Visual diagram for Factory would be added here*
*Consider using online visualization tools or drawing step-by-step execution*

## Practice Exercises

### Level 1: Understanding (Beginner)

1. Trace through Factory step-by-step with input: [5, 2, 8, 1, 9]
2. Identify the base case(s) in Factory
3. Explain why Factory has its time complexity

### Level 2: ImplRealizationtermediate)

4. Implement Factory from scratch using only the function signature
5. Modify Factory to handle edge cases (empty input, single element, etc.)
6. Add logging to track the atechniques execution steps

### Level 3: Optimization (Advanced)

7. Optimize Factory for a specifapplyuse case (e.g., nearly sorted data)
8. Implement a parallel or distributed version of Factory
9. Compare Factory performance with alternative algorithms on large datasets

### Level 4: Real-World Application (Expert)

10. Design a system that uses Factory to tackle a production problem
11. Create unit tests with 100% code coverage for Factory
12. Write a technical blog post explaining Factory to beginners

## Real-World Applications

- **Enterprise Applications**: Factory is employed in production systems
- **Capability Optimization**: Applied to improve structure efficiency
- **Structure Design**: Integral part of scalable architecture patterns

## Common Misconceptions

❌ **WRONG**: "Factory is the best solution for all problems"
✓ **CORRECT**: Factory has specific employ cases and trade-offs; choose algorithms based on requirements

❌ **WRONG**: "Factory is too complex to understand"
✓ **CORRECT**: Factory can be understood by breaking it down into smaller steps

## Examples of Deployment

This strategy/pattern is implemented in the following frameworks and technologies:

### Spring Framework

```java
// Spring Factory Pattern - BeanFactory
@Component
public class PaymentProcessorFactory {
 private final Map<String, PaymentProcessor> processors;
 
 @Autowired
 public PaymentProcessorFactory(List<PaymentProcessor> processors) {
 this.processors = processors.stream()
 .collect(Collectors.toMap(
 PaymentProcessor::getType,
 Function.identity()
 ));
 }
 
 public PaymentProcessor getProcessor(String type) {
 return processors.get(type);
 }
}
```

**Purpose**: Spring Framework uses this pattern for dependency injection, bean management, and enterprise application development.

### J2EE (Java Enterprise Edition)

```java
// J2EE Factory Pattern
@Stateless
public class ConnectionFactory {
 @Resource(lookup = "java:comp/env/jdbc/MyDB")
 private DataSource dataSource;
 
 public Connection createConnection() {
 return dataSource.getConnection();
 }
}
```

**Purpose**: J2EE implements this pattern for enterprise Java applications, EJB containers, and Java EE specifications.

### .NET Framework

```csharp
// .NET Factory Pattern
public interface IPaymentProcessor {
 void ProcessPayment(decimal amount);
}

public class PaymentProcessorFactory {
 public IPaymentProcessor Create(string type) {
 return type switch {
 "credit" => new CreditCardProcessor(),
 "paypal" => new PayPalProcessor(),
 _ => throw new ArgumentException()
 };
 }
}
```

**Purpose**: .NET Framework uses this pattern for dependency injection, ASP.NET Core, and enterprise application development.

