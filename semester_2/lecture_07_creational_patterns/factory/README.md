# Factory Method Pattern

**Category**: Creational Pattern

**Time Complexity**: O(1)

**Space Complexity**: O(1)

## Implementation

## Introduction

Factory is a fundamental algorithm.

This algorithm is widely used in computer science and software engineering for solving a specific class of problems efficiently. Understanding Factory is essential for building performant and scalable applications.

### Short Description

Factory is a fundamental algorithm.

**Key Characteristics:**
- **Time Complexity**: Varies
- **Space Complexity**: Varies
- **Stability**: N/A
- **Best Use Case**: General purpose


See algorithm.py and Algorithm.java


## Often Used Together With

Factory is commonly used in combination with:

- **Singleton**: Often combined for comprehensive solutions
- **Observer**: Often combined for comprehensive solutions
- **Strategy**: Often combined for comprehensive solutions

**Common Combinations:**
- Used together in production systems for optimal performance
- Complementary algorithms that solve related problems
- Often part of larger algorithmic frameworks


## Do Not Confuse With

- **Abstract Factory**: Factory creates single product type, abstract factory creates families of products
- **Builder Pattern**: Factory creates objects directly, builder constructs complex objects step by step
- **Singleton**: Factory creates multiple instances, singleton ensures single instance


## Examples of Implementation

This algorithm/pattern is implemented in the following frameworks:

### Spring Framework

```java
// Spring Factory Pattern
@Component
public class PaymentProcessorFactory {
    @Autowired
    private List<PaymentProcessor> processors;
    
    public PaymentProcessor getProcessor(String type) {
        return processors.stream()
            .filter(p -> p.supports(type))
            .findFirst()
            .orElseThrow();
    }
}
```

### .NET Framework

```csharp
// .NET Factory Pattern
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