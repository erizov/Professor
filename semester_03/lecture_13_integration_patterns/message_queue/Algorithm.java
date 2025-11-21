package semester_03.lecture_13_integration_patterns.message_queue;

import java.util.*;
import java.util.concurrent.*;
import java.time.LocalDateTime;

import java.util.logging.Logger;
class Message {
    int id;
    String topic;
    Object payload;
    LocalDateTime timestamp;
    
    Message(int id, String topic, Object payload) {
        this.id = id;
        this.topic = topic;
        this.payload = payload;
        this.timestamp = LocalDateTime.now();
    }
    
    @Override
    public String toString() {
        return String.format("Message(id=%d, topic='%s', payload='%s')",
                           id, topic, payload);
    }
}

class MessageQueue {
    private final BlockingQueue<Message> queue;
    private int messageId = 0;
    private final Object lock = new Object();
    
    MessageQueue(int maxSize) {
        this.queue = new LinkedBlockingQueue<>(maxSize);
    }
    
    int publish(String topic, Object payload) {
        synchronized (lock) {
            messageId++;
            Message message = new Message(messageId, topic, payload);
            try {
                queue.put(message);
                return message.id;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return -1;
            }
        }
    }
    
    Message consume(Long timeoutMs) throws InterruptedException {
        if (timeoutMs == null) {
            return queue.take();
        }
        return queue.poll(timeoutMs, TimeUnit.MILLISECONDS);
    }
    
    int size() {
        return queue.size();
    }
}

class Producer {
    private final String name;
    private final MessageQueue queue;
    
    Producer(String name, MessageQueue queue) {
        this.name = name;
        this.queue = queue;
    }
    
    int send(String topic, Object payload) {
        int msgId = queue.publish(topic, payload);
        System.out.printf("[%s] Published: %s - %s%n", name, topic, payload);
        return msgId;
    }
}

class Consumer implements Runnable {
    private final String name;
    private final MessageQueue queue;
    private final List<String> topics;
    private volatile boolean running = false;
    private Thread thread;
    
    Consumer(String name, MessageQueue queue, List<String> topics) {
        this.name = name;
        this.queue = queue;
        this.topics = topics != null ? topics : new ArrayList<>();
    }
    
    void start() {
        running = true;
        thread = new Thread(this);
        thread.setDaemon(true);
        thread.start();
    }
    
    void stop() {
        running = false;
        if (thread != null) {
            try {
                thread.join(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    @Override
    public void run() {
        while (running) {
            try {
                Message message = queue.consume(1000L);
                if (message != null) {
                    if (topics.isEmpty() || topics.contains(message.topic)) {
                        process(message);
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    void process(Message message) {
        System.out.printf("[%s] Consumed: %s%n", name, message);
    }
}

class TopicQueue {
    private final Map<String, BlockingQueue<Object>> queues = new ConcurrentHashMap<>();
    
    void createTopic(String topic, int maxSize) {
        queues.putIfAbsent(topic, new LinkedBlockingQueue<>(maxSize));
    }
    
    boolean publish(String topic, Object payload) {
        createTopic(topic, 100);
        try {
            queues.get(topic).put(payload);
            return true;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        }
    }
    
    void subscribe(String topic, java.util.function.BiConsumer<String, Object> callback) {
        createTopic(topic, 100);
        Thread thread = new Thread(() -> {
            while (true) {
                try {
                    Object payload = queues.get(topic).poll(1, TimeUnit.SECONDS);
                    if (payload != null) {
                        callback.accept(topic, payload);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        thread.setDaemon(true);  // Make daemon thread so it doesn't prevent program exit
        thread.start();
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    private static final String dash = "-".repeat(70);
    private static final String separator = "=".repeat(70);

    
    public static void main(String[] args) throws InterruptedException {
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("MESSAGE QUEUE PATTERN DEMONSTRATION");
        logger.info(separator);
        logger.info("");
        
        // Example 1: Basic Message Queue
        logger.info("Example 1: Basic Message Queue");
        logger.info(dash);
        
        MessageQueue mq = new MessageQueue(100);
        Producer producer = new Producer("Producer1", mq);
        Consumer consumer1 = new Consumer("Consumer1", mq, null);
        Consumer consumer2 = new Consumer("Consumer2", mq, null);
        
        consumer1.start();
        consumer2.start();
        
        producer.send("orders", "Order #1001");
        producer.send("orders", "Order #1002");
        producer.send("notifications", "User logged in");
        producer.send("orders", "Order #1003");
        
        Thread.sleep(500);
        
        consumer1.stop();
        consumer2.stop();
        logger.info("");
        
        // Example 2: Topic-based Queue
        logger.info("Example 2: Topic-based Message Queue");
        logger.info(dash);
        
        TopicQueue topicQueue = new TopicQueue();
        
        topicQueue.subscribe("orders", (topic, payload) -> 
            System.out.printf("Order handler received: %s%n", payload));
        topicQueue.subscribe("notifications", (topic, payload) -> 
            System.out.printf("Notification handler received: %s%n", payload));
        
        topicQueue.publish("orders", "Order #2001");
        topicQueue.publish("notifications", "Email sent");
        topicQueue.publish("orders", "Order #2002");
        
        Thread.sleep(500);
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern Summary:");
        logger.info("\nIntent:");
        logger.info("  Asynchronous communication pattern where messages are");
        logger.info("  sent to a queue and processed by consumers.");
        logger.info("\nKey Advantages:");
        logger.info("  - Decouples producers and consumers");
        logger.info("  - Asynchronous processing");
        logger.info("  - Load balancing");
        logger.info("  - Reliability (messages persist)");
        logger.info("\nWhen to Use:");
        logger.info("  - Asynchronous processing needed");
        logger.info("  - Decouple components");
        logger.info("  - Event-driven architecture");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
        
        // Give daemon threads a moment to finish processing
        Thread.sleep(100);
    }
}