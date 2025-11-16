/**
 * Publish-Subscribe (Pub-Sub) Pattern.
 * 
 * Decouples publishers from subscribers. Publishers send messages to
 * topics/channels without knowing who subscribes. Subscribers listen to
 * topics they're interested in.
 */
import java.util.*;
import java.util.concurrent.*;

interface Subscriber {
    void update(String topic, Object message);
}

class Publisher {
    private final MessageBroker broker;
    
    Publisher(MessageBroker broker) {
        this.broker = broker;
    }
    
    void publish(String topic, Object message) {
        broker.publish(topic, message);
    }
}

class MessageBroker {
    private final Map<String, List<Subscriber>> subscribers = new ConcurrentHashMap<>();
    private final Object lock = new Object();
    
    void subscribe(String topic, Subscriber subscriber) {
        synchronized (lock) {
            subscribers.computeIfAbsent(topic, k -> new ArrayList<>());
            if (!subscribers.get(topic).contains(subscriber)) {
                subscribers.get(topic).add(subscriber);
            }
        }
    }
    
    void unsubscribe(String topic, Subscriber subscriber) {
        synchronized (lock) {
            if (subscribers.containsKey(topic)) {
                subscribers.get(topic).remove(subscriber);
            }
        }
    }
    
    void publish(String topic, Object message) {
        synchronized (lock) {
            if (subscribers.containsKey(topic)) {
                for (Subscriber subscriber : subscribers.get(topic)) {
                    subscriber.update(topic, message);
                }
            }
        }
    }
}

class EmailSubscriber implements Subscriber {
    private final String email;
    private final List<String[]> messages = new ArrayList<>();
    
    EmailSubscriber(String email) {
        this.email = email;
    }
    
    @Override
    public void update(String topic, Object message) {
        messages.add(new String[]{topic, message.toString()});
        System.out.printf("[Email to %s] Topic: %s, Message: %s%n",
                         email, topic, message);
    }
}

class LogSubscriber implements Subscriber {
    private final List<String[]> logs = new ArrayList<>();
    
    @Override
    public void update(String topic, Object message) {
        logs.add(new String[]{topic, message.toString()});
        System.out.printf("[LOG] %s: %s%n", topic, message);
    }
}

class NotificationSubscriber implements Subscriber {
    private final String userId;
    private final List<String[]> notifications = new ArrayList<>();
    
    NotificationSubscriber(String userId) {
        this.userId = userId;
    }
    
    @Override
    public void update(String topic, Object message) {
        notifications.add(new String[]{topic, message.toString()});
        System.out.printf("[Notification to User %s] %s: %s%n",
                         userId, topic, message);
    }
}

class Event {
    String eventType;
    Object data;
    LocalDateTime timestamp;
    
    Event(String eventType, Object data) {
        this.eventType = eventType;
        this.data = data;
        this.timestamp = LocalDateTime.now();
    }
}

class EventBus {
    private final Map<String, List<java.util.function.Consumer<Event>>> handlers =
        new ConcurrentHashMap<>();
    private final Object lock = new Object();
    
    void subscribe(String eventType, java.util.function.Consumer<Event> handler) {
        synchronized (lock) {
            handlers.computeIfAbsent(eventType, k -> new ArrayList<>());
            if (!handlers.get(eventType).contains(handler)) {
                handlers.get(eventType).add(handler);
            }
        }
    }
    
    void publish(Event event) {
        synchronized (lock) {
            if (handlers.containsKey(event.eventType)) {
                for (java.util.function.Consumer<Event> handler :
                     handlers.get(event.eventType)) {
                    handler.accept(event);
                }
            }
        }
    }
}

import java.time.LocalDateTime;

public class Algorithm {
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("PUBLISH-SUBSCRIBE (PUB-SUB) PATTERN DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Basic Pub-Sub
        System.out.println("Example 1: Basic Publish-Subscribe");
        System.out.println("-".repeat(70));
        
        MessageBroker broker = new MessageBroker();
        Publisher publisher = new Publisher(broker);
        
        EmailSubscriber emailSub = new EmailSubscriber("user@example.com");
        LogSubscriber logSub = new LogSubscriber();
        NotificationSubscriber notifSub = new NotificationSubscriber("user123");
        
        broker.subscribe("orders", emailSub);
        broker.subscribe("orders", logSub);
        broker.subscribe("notifications", notifSub);
        broker.subscribe("notifications", logSub);
        
        System.out.println("Publishing messages:");
        publisher.publish("orders", "New order #1001");
        publisher.publish("notifications", "User logged in");
        publisher.publish("orders", "Order #1001 shipped");
        System.out.println();
        
        // Example 2: Event-driven Pub-Sub
        System.out.println("Example 2: Event-driven Pub-Sub");
        System.out.println("-".repeat(70));
        
        EventBus eventBus = new EventBus();
        
        eventBus.subscribe("order.created", event ->
            System.out.printf("Order handler: %s%n", event.data));
        eventBus.subscribe("user.registered", event ->
            System.out.printf("User handler: %s%n", event.data));
        
        System.out.println("Publishing events:");
        eventBus.publish(new Event("order.created", "Order #2001"));
        eventBus.publish(new Event("user.registered", "User: alice"));
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern Summary:");
        System.out.println("\nIntent:");
        System.out.println("  Decouples publishers from subscribers.");
        System.out.println("  Publishers send messages to topics without knowing subscribers.");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Loose coupling");
        System.out.println("  - Scalable");
        System.out.println("  - Dynamic subscription");
        System.out.println("  - Multiple subscribers per topic");
        System.out.println("\nWhen to Use:");
        System.out.println("  - Event-driven architecture");
        System.out.println("  - Microservices communication");
        System.out.println("  - Real-time notifications");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
