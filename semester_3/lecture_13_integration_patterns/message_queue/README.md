# Message Queue Pattern

**Category**: Integration

**Time Complexity**: O(1)

**Space Complexity**: O(n)

## Implementation

## Introduction

Message Queue is a fundamental algorithm.

This algorithm is widely used in computer science and software engineering for solving a specific class of problems efficiently. Understanding Message Queue is essential for building performant and scalable applications.

### Short Description

Message Queue is a fundamental algorithm.

**Key Characteristics:**
- **Time Complexity**: Varies
- **Space Complexity**: Varies
- **Stability**: N/A
- **Best Use Case**: General purpose


See algorithm.py and Algorithm.java


## Often Used Together With

Message Queue is commonly used in combination with:

- **Factory**: Often combined for comprehensive solutions
- **Singleton**: Often combined for comprehensive solutions
- **Observer**: Often combined for comprehensive solutions
- **Strategy**: Often combined for comprehensive solutions

**Common Combinations:**
- Used together in production systems for optimal performance
- Complementary algorithms that solve related problems
- Often part of larger algorithmic frameworks




## Do Not Confuse With

- **Pub-Sub**: Message queue is point-to-point, pub-sub is one-to-many messaging
- **Event Bus**: Message queue stores messages, event bus broadcasts events immediately
- **Stream Processing**: Message queue is messaging, stream processing is continuous data processing

## Examples of Implementation

This algorithm/pattern is implemented in the following frameworks:

### Spring Framework

```java
// Spring JMS Message Queue
@JmsListener(destination = "orders.queue")
public void receiveMessage(Order order) {
    orderService.process(order);
}
```

### Apache Kafka

```java
// Kafka Producer
@Autowired
private KafkaTemplate<String, String> kafkaTemplate;

public void sendMessage(String topic, String message) {
    kafkaTemplate.send(topic, message);
}

// Kafka Consumer
@KafkaListener(topics = "orders")
public void consume(String message) {
    // Process message
}
```