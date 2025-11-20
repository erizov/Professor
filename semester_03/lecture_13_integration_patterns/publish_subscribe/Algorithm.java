/**
package semester_03.lecture_13_integration_patterns.publish_subscribe;
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

import java.util.logging.Logger;
class Publisher {
    private final MessageBroker broker;
    
    Publisher(MessageBroker broker) {
        this.broker = broker;
    }
    
    void publish(String topic, Object message) {
        broker.publish(topic, message);
                        public static void main(String[] args) {
    }
    }
        
                        public void update(String topic, Object message) {
                                            logger.info("PUBLISH-SUBSCRIBE (PUB-SUB) PATTERN DEMONSTRATION");
                    System.out.printf("[Email to %s] Topic: %s, Message: %s%n",
                                        }
                                        logger.info("  - Microservices communication");
                                    logger.info("");
                        @Override
                                                    logger.info(dash);
                                            logger.info("Example 2: Event-driven Pub-Sub");
                                            System.out.printf("Order handler: %s%n", event.data));
                                    broker.subscribe("notifications", notifSub);
        
                                        logger.info("  - Dynamic subscription");
                                                logger.info("  - Event-driven architecture");
                                    void publish(String topic, Object message) {
                                    for (Subscriber subscriber : subscribers.get(topic)) {
                    }
                                            logger.info("  - Multiple subscribers per topic");
                EmailSubscriber(String email) {
        
                    @Override
            class EmailSubscriber implements Subscriber {
                                    logger.info("\nKey Advantages:");
                                    LogSubscriber logSub = new LogSubscriber();
                            }
                class Event {
    
                                        eventBus.subscribe("user.registered", event ->
                                        logger.info(separator);
    
                        if (subscribers.containsKey(topic)) {
                                eventBus.publish(new Event("user.registered", "User: alice"));
        
                    notifications.add(new String[]{topic, message.toString()});
    
                        @Override
                            subscribers.get(topic).add(subscriber);
                                    MessageBroker broker = new MessageBroker();
            public void update(String topic, Object message) {
                                logger.info("  Decouples publishers from subscribers.");
                    System.out.printf("[LOG] %s: %s%n", topic, message);
                                    broker.subscribe("orders", logSub);
                                logger.info("Publishing messages:");
                    }
            class LogSubscriber implements Subscriber {
                                    logger.info(separator);
                messages.add(new String[]{topic, message.toString()});
                this.userId = userId;
            private final Object lock = new Object();
                synchronized (lock) {
        
                            logger.info("\nWhen to Use:");
                                Object data;
                                        logger.info("\nPattern Summary:");
                                    Publisher publisher = new Publisher(broker);
                                        broker.subscribe("orders", emailSub);
                                    NotificationSubscriber notifSub = new NotificationSubscriber("user123");

                private final String email;
        
                        }
                    void subscribe(String eventType, java.util.function.Consumer<Event> handler) {
                    synchronized (lock) {
                                    EmailSubscriber emailSub = new EmailSubscriber("user@example.com");
                private final List<String[]> logs = new ArrayList<>();
        
                    }
            }
                        }
                                long endTime = System.nanoTime();
                                logger.info("\nIntent:");
                                logger.info("  Publishers send messages to topics without knowing subscribers.");
    
                            logger.info(dash);
                            logger.info(separator);
                        }
        
                                        long startTime = System.nanoTime();
                            subscribers.computeIfAbsent(topic, k -> new ArrayList<>());

                                    eventBus.subscribe("order.created", event ->
            private final List<String[]> messages = new ArrayList<>();
                }
                                            publisher.publish("notifications", "User logged in");
                                        String separator = "=".repeat(70);
                }
                                    System.out.printf("User handler: %s%n", event.data));
                this.email = email;
                        handlers.get(eventType).add(handler);
                                // Example 1: Basic Pub-Sub

        
                            logger.info("  - Real-time notifications");
                                     email, topic, message);
            public void update(String topic, Object message) {
                    logs.add(new String[]{topic, message.toString()});
        
                                    logger.info("");
                    if (subscribers.containsKey(topic)) {
            }
                                broker.subscribe("notifications", logSub);
                                publisher.publish("orders", "New order #1001");
                            logger.info(separator);
                            logger.info("  - Scalable");
                handlers.computeIfAbsent(eventType, k -> new ArrayList<>());
                            subscriber.update(topic, message);
                                logger.info("Publishing events:");
                            }
            void unsubscribe(String topic, Subscriber subscriber) {
            synchronized (lock) {
                            String dash = "-".repeat(70);
        void subscribe(String topic, Subscriber subscriber) {
                            logger.info("Example 1: Basic Publish-Subscribe");
        
                            logger.info("");
                            // Example 2: Event-driven Pub-Sub
                            EventBus eventBus = new EventBus();
                            eventBus.publish(new Event("order.created", "Order #2001"));
                            logger.info("  - Loose coupling");
                         handlers.get(event.eventType)) {
                        handler.accept(event);
}
class MessageBroker {
    private final Map<String, List<Subscriber>> subscribers = new ConcurrentHashMap<>();
    private final Object lock = new Object();
        synchronized (lock) {
            if (!subscribers.get(topic).contains(subscriber)) {
            }
    
                subscribers.get(topic).remove(subscriber);
    
    }
    
}
        
                        publisher.publish("orders", "Order #1001 shipped");
                        System.out.printf("\nTotal time: %.3f ms%n",
                                        (endTime - startTime) / 1_000_000.0);
                    }
        String eventType;
        LocalDateTime timestamp;
        Event(String eventType, Object data) {
            this.eventType = eventType;
            this.data = data;
            this.timestamp = LocalDateTime.now();
        }
    }

class NotificationSubscriber implements Subscriber {
    private final String userId;
    private final List<String[]> notifications = new ArrayList<>();
    
    NotificationSubscriber(String userId) {
    }
    
        System.out.printf("[Notification to User %s] %s: %s%n",
                         userId, topic, message);
    }
}


class EventBus {
    private final Map<String, List<java.util.function.Consumer<Event>>> handlers =
        new ConcurrentHashMap<>();
    
            if (!handlers.get(eventType).contains(handler)) {
            }
        }
    }
    
    void publish(Event event) {
        synchronized (lock) {
            if (handlers.containsKey(event.eventType)) {
                for (java.util.function.Consumer<Event> handler :
            }
        }
    }
    public class Algorithm {
}

import java.time.LocalDateTime;

    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
}