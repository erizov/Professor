# Circuit Breaker Pattern

**Category**: Deployment

**Time Complexity**: O(1)

**Space Complexity**: O(1)

## Implementation

## Introduction

Circuit Breaker is circuit breaker is a fundamental algorithm.

This algorithm is widely used in computer science and software engineering for solving a specific class of problems efficiently. Understanding Circuit Breaker is essential for building performant and scalable applications.

### Short Description

Circuit Breaker is a fundamental algorithm.

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

## Examples of Implementation

This algorithm/pattern is implemented in the following frameworks:

### Spring Framework

```java
// Spring Cloud Circuit Breaker
@CircuitBreaker(name = "payment-service", fallbackMethod = "fallback")
public PaymentResult processPayment(PaymentRequest request) {
    return paymentClient.process(request);
}

public PaymentResult fallback(PaymentRequest request, Exception e) {
    return PaymentResult.failed("Service unavailable");
}
```