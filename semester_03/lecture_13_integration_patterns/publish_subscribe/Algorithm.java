package semester_03.lecture_13_integration_patterns.publish_subscribe;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.logging.Logger;

/**
 * Publish-Subscribe (Pub-Sub) Pattern demonstration.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Publish-Subscribe");
        System.out.println("=".repeat(70));

        MessageBroker broker = new MessageBroker();
        Publisher publisher = new Publisher(broker);

        broker.subscribe("orders", new EmailSubscriber("orders@example.com"));
        broker.subscribe("orders", new LogSubscriber("order-log"));
        broker.subscribe("notifications", new EmailSubscriber("notifications@example.com"));

        publisher.publish("orders", "Order #1024 received");
        publisher.publish("notifications", "Deployment complete");

        System.out.println("=".repeat(70));
    }
}

interface Subscriber {
    void update(String topic, Object message);
}

class MessageBroker {
    private final Logger logger = Logger.getLogger(MessageBroker.class.getName());
    private final Map<String, List<Subscriber>> subscribers = new ConcurrentHashMap<>();

    void subscribe(String topic, Subscriber subscriber) {
        subscribers.computeIfAbsent(topic, key -> new ArrayList<>()).add(subscriber);
        logger.fine(() -> "Subscriber added for topic: " + topic);
    }

    void publish(String topic, Object message) {
        logger.fine(() -> "Publishing to topic: " + topic);
        List<Subscriber> topicSubscribers = subscribers.get(topic);
        if (topicSubscribers == null) {
            return;
        }
        for (Subscriber subscriber : topicSubscribers) {
            subscriber.update(topic, message);
        }
    }
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

class EmailSubscriber implements Subscriber {
    private final String address;

    EmailSubscriber(String address) {
        this.address = address;
    }

    @Override
    public void update(String topic, Object message) {
        System.out.printf("[Email to %s] Topic: %s, Message: %s%n", address, topic, message);
    }
}

class LogSubscriber implements Subscriber {
    private final String loggerName;

    LogSubscriber(String loggerName) {
        this.loggerName = loggerName;
    }

    @Override
    public void update(String topic, Object message) {
        System.out.printf("[Log %s] Topic: %s, Message: %s%n", loggerName, topic, message);
    }
}

