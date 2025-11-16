# Strategy Pattern

**Category**: Behavioral Pattern

**Time Complexity**: O(1)

**Space Complexity**: O(1)

## Implementation

## Introduction

Strategy is strategy is a fundamental algorithm.

This algorithm is widely used in computer science and software engineering for solving a specific class of problems efficiently. Understanding Strategy is essential for building performant and scalable applications.

### Short Description

Strategy is a fundamental algorithm.

**Key Characteristics:**
- **Time Complexity**: Varies
- **Space Complexity**: Varies
- **Stability**: N/A
- **Best Use Case**: General purpose


See algorithm.py and Algorithm.java


## Often Used Together With

Strategy is commonly used in combination with:

- **Factory**: Often combined for comprehensive solutions
- **Singleton**: Often combined for comprehensive solutions
- **Observer**: Often combined for comprehensive solutions

**Common Combinations:**
- Used together in production systems for optimal performance
- Complementary algorithms that solve related problems
- Often part of larger algorithmic frameworks


## Do Not Confuse With

- **Template Method**: Strategy uses composition, template method uses inheritance
- **State Pattern**: Strategy chooses algorithm, state pattern changes behavior based on state
- **Command Pattern**: Strategy encapsulates algorithm, command encapsulates request


## Examples of Implementation

This algorithm/pattern is implemented in the following frameworks:

### Spring Framework

```java
// Spring Strategy Pattern
public interface PaymentStrategy {
    void pay(BigDecimal amount);
}

@Component("creditCard")
public class CreditCardStrategy implements PaymentStrategy {
    public void pay(BigDecimal amount) {
        // Credit card payment logic
    }
}
```

### .NET Framework

```csharp
// .NET Strategy Pattern
public interface IPaymentStrategy {
    void ProcessPayment(decimal amount);
}

public class CreditCardStrategy : IPaymentStrategy {
    public void ProcessPayment(decimal amount) {
        // Credit card payment logic
    }
}
```