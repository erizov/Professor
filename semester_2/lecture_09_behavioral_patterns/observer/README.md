# Observer Pattern

**Category**: Behavioral Pattern

**Time Complexity**: O(n)

**Space Complexity**: O(n)

## Implementation

## Introduction

Observer is a fundamental algorithm.

This algorithm is widely used in computer science and software engineering for solving a specific class of problems efficiently. Understanding Observer is essential for building performant and scalable applications.

### Short Description

Observer is a fundamental algorithm.

**Key Characteristics:**
- **Time Complexity**: Varies
- **Space Complexity**: Varies
- **Stability**: N/A
- **Best Use Case**: General purpose


See algorithm.py and Algorithm.java


## Often Used Together With

Observer is commonly used in combination with:

- **Factory**: Often combined for comprehensive solutions
- **Singleton**: Often combined for comprehensive solutions
- **Strategy**: Often combined for comprehensive solutions

**Common Combinations:**
- Used together in production systems for optimal performance
- Complementary algorithms that solve related problems
- Often part of larger algorithmic frameworks


## Do Not Confuse With

- **Pub-Sub Pattern**: Observer is synchronous push model, pub-sub is asynchronous message-based
- **Mediator Pattern**: Observer has direct subject-observer relationship, mediator centralizes communication
- **Chain of Responsibility**: Observer notifies all, chain of responsibility passes request along chain


## Examples of Implementation

This algorithm/pattern is implemented in the following frameworks:

### Spring Framework

```java
// Spring Event Listener (Observer Pattern)
@Component
public class OrderEventListener {
    @EventListener
    public void handleOrderCreated(OrderCreatedEvent event) {
        // Handle order creation
        sendNotification(event.getOrder());
    }
}
```

### .NET Framework

```csharp
// .NET Event Handler (Observer Pattern)
public class OrderService {
    public event EventHandler<OrderCreatedEventArgs> OrderCreated;
    
    public void CreateOrder(Order order) {
        // Create order logic
        OrderCreated?.Invoke(this, new OrderCreatedEventArgs(order));
    }
}
```