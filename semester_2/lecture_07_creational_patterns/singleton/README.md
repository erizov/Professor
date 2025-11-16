# Singleton Pattern

**Category**: Creational Pattern

**Time Complexity**: O(1)

**Space Complexity**: O(1)

## Implementation

## Introduction

Singleton addresses specific computational challenges.

This technique is applied in various domains to solve specific problems efficiently. Understanding this approach enables developers to solve related problems effectively.

## TL;DR

**One Sentence**: A creational design pattern that ensures a class has only one instance and provides global access to that instance.

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

1. Implement Singleton from scratch
2. Analyze time and space complexity using Big O notation
3. Identify when to employ this algorithm vs. alternative approaches
4. Recognize common implementation pitfalls and how to avoid them
5. Apply this algorithm to tackle real-world problems
6. Recognize when this pattern is appropriate in system design

### Short Description

A creational design pattern that ensures a class has only one instance and provides global access to that instance. Addresses database connection management, logging systems, and configuration managers. Example: A single database connection pool shared across an application to avoid resource exhaustion. Operates by making the constructor private and providing a static method that returns the same instance.

**Key Characteristics:**
- **Time Complexity**: Varies
- **Space Complexity**: Varies
- **Stability**: N/A

## Often Used Together With

Singleton is used in combination with:

- **Factory**: Often combined for comprehensive solutions

**Common Combinations:**
- Employed together in production systems for optimal performance
- Complementary algorithms that tackle related problems
- Often part of larger algorithmic frameworks

## Do Not Confuse With

- **Factory Pattern**: Singleton ensures single instance, factory creates objects
- **Static Class**: Singleton allows inheritance and interfaces, static class cannot
- **Global Variable**: Singleton is object-oriented pattern, global variable is procedural approach

## Self-Assessment Questions

Test your understanding with these questions:

### Comprehension

1. Can you explain how Singleton works in your own words?
2. What is the key insight or technique that makes Singleton efficient?

### Analysis

3. What are the best-case, average-case, and worst-case time complexities?
4. When would you choose Singleton over alternative algorithms?

### Application

5. Can you implement Singleton from memory without looking at the code?
6. What real-world problem could youaddresse using Singleton?

### Debugging

7. What are the most common mistakes when implementing Singleton?
8. How would you test your Singleton deployment?

**Scoring**: If you can answer 6+ questions confidently, you've mastered this strategy!

## Strategy Visualization

*Visual diagram for Singleton would be added here*
*Consider using online visualization tools or drawing step-by-step execution*

## Practice Exercises

### Level 1: Understanding (Beginner)

1. Trace through Singleton step-by-step with input: [5, 2, 8, 1, 9]
2. Identify the base case(s) in Singleton
3. Explain why Singleton has its time complexity

### Level 2: Deployment (Intermediate)

4. Implement Singleton from scratch using only the function signature
5. Modify Singleton to handle edge cases (empty input, single element, etc.)
6. Add logging to track the atechniques execution steps

### Level 3: Optimization (Advanced)

7. Optimize Singleton for a specifapplyuse case (e.g., nearly sorted data)
8. Implement a parallel or distributed version of Singleton
9. Compare Singleton performance with alternative algorithms on large datasets

### Level 4: Real-World Application (Expert)

10. Design a system that uses Singleton to tackle a production problem
11. Create unit tests with 100% code coverage for Singleton
12. Write a technical blog post explaining Singleton to beginners

## Real-World Applications

- **Database Connections**: Managing single connection pool instance
- **Logging Systems**: Centralized logger instance
- **Configuration Managers**: Single source of truth for application settings

## Common Misconceptions

❌ **WRONG**: "Singleton is the best solution for all problems"
✓ **CORRECT**: Singleton has specific employ cases and trade-offs; choose algorithms based on requirements

❌ **WRONG**: "Singleton is too complex to understand"
✓ **CORRECT**: Singleton can be understood by breaking it down into smaller steps

## Examples of ImplRealizationis strategy/pattern is implemented in the following frameworks and technologies:

### Spring Framework

```java
// Spring Singleton Bean (default scope)
@Component // Singleton by default
public class DatabaseConnectionManager {
 @Autowired
 private DataSource dataSource;
 
 // Spring container ensures single instance per application context
 public Connection getConnection() throws SQLException {
 return dataSource.getConnection();
 }
}
```

**Purpose**: Spring Framework uses this pattern for dependency injection, bean management, and enterprise application development.

### J2EE (Java Enterprise Edition)

```java
// J2EE Singleton EJB
@Singleton
@Startup
@ConcurrencyManagement(ConcurrencyManagementType.CONTAINER)
public class ApplicationCache {
 private final Map<String, Object> cache = new ConcurrentHashMap<>();
 
 @PostConstruct
 public void init() {
 // Single instance initialized at startup
 }
 
 public void put(String key, Object value) {
 cache.put(key, value);
 }
}
```

**Purpose**: J2EE implements this pattern for enterprise Java applications, EJB containers, and Java EE specifications.

### .NET Framework

```csharp
// .NET Dependency Injection Singleton
public class CacheService {
 // Registered as singleton in Startup.cs
 public void Add(string key, object value) { }
}

// Startup.cs
services.AddSingleton<CacheService>();
```

**Purpose**: .NET Framework uses this pattern for dependency injection, ASP.NET Core, and enterprise application development.

