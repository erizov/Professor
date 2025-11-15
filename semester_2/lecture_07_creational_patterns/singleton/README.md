# Singleton Pattern

**Category**: Creational Pattern

**Time Complexity**: O(1)

**Space Complexity**: O(1)

## Implementation

## Introduction

Singleton is singleton is a fundamental algorithm.

This algorithm is widely used in computer science and software engineering for solving a specific class of problems efficiently. Understanding Singleton is essential for building performant and scalable applications.

### Short Description

Singleton is a fundamental algorithm.

**Key Characteristics:**
- **Time Complexity**: Varies
- **Space Complexity**: Varies
- **Stability**: N/A
- **Best Use Case**: General purpose


See algorithm.py and Algorithm.java


## Often Used Together With

Singleton is commonly used in combination with:

- **Factory**: Often combined for comprehensive solutions
- **Observer**: Often combined for comprehensive solutions
- **Strategy**: Often combined for comprehensive solutions

**Common Combinations:**
- Used together in production systems for optimal performance
- Complementary algorithms that solve related problems
- Often part of larger algorithmic frameworks


## Do Not Confuse With

**Singleton** should not be confused with:

- **Factory**: Different approach/use case, though related
- **Builder**: Different approach/use case, though related

**Key Differences:**
- Each algorithm has distinct characteristics and use cases
- Understanding the differences is crucial for correct application
- Similar names don't imply similar implementations


## Examples of Implementation

This algorithm/pattern is implemented in the following frameworks:

### Spring Framework

```java
// Spring Singleton Bean (default scope)
@Component
public class DatabaseConnection {
    @Autowired
    private DataSource dataSource;
    
    // Spring container manages singleton instance
    public Connection getConnection() {
        return dataSource.getConnection();
    }
}
```

### J2EE (Java Enterprise Edition)

```java
// J2EE Singleton EJB
@Singleton
@Startup
public class CacheManager {
    private Map<String, Object> cache = new ConcurrentHashMap<>();
    
    @PostConstruct
    public void init() {
        // Initialize cache
    }
}
```