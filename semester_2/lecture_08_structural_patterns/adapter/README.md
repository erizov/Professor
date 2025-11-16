# Adapter Pattern

**Category**: Structural Pattern

**Time Complexity**: O(1)

**Space Complexity**: O(1)

## Implementation

## Introduction

Adapter is a fundamental algorithm.

This algorithm is widely used in computer science and software engineering for solving a specific class of problems efficiently. Understanding Adapter is essential for building performant and scalable applications.

### Short Description

Adapter is a fundamental algorithm.

**Key Characteristics:**
- **Time Complexity**: Varies
- **Space Complexity**: Varies
- **Stability**: N/A
- **Best Use Case**: General purpose


See algorithm.py and Algorithm.java


## Often Used Together With

Adapter is commonly used in combination with:

- **Factory**: Often combined for comprehensive solutions
- **Singleton**: Often combined for comprehensive solutions
- **Observer**: Often combined for comprehensive solutions
- **Strategy**: Often combined for comprehensive solutions

**Common Combinations:**
- Used together in production systems for optimal performance
- Complementary algorithms that solve related problems
- Often part of larger algorithmic frameworks




## Do Not Confuse With

- Creational vs structural vs behavioral patterns
- Design patterns vs architectural patterns
- Patterns vs principles (SOLID)

## Examples of Implementation

This algorithm/pattern is implemented in the following frameworks:

### Spring Framework

```java
// Spring Adapter Pattern
@Component
public class LegacyPaymentAdapter implements PaymentService {
    private LegacyPaymentSystem legacySystem;
    
    public void processPayment(PaymentRequest request) {
        LegacyPayment legacy = convert(request);
        legacySystem.process(legacy);
    }
}
```