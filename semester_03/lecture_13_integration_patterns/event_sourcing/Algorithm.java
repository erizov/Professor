import java.util.*;

/**
 * Event Sourcing Pattern.
 * 
 * Stores state changes as events.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
    interface Event {
        String getEventType();
    }
    
    static class UserCreatedEvent implements Event {
        private int userId;
        private String name;
        private String email;
        
        UserCreatedEvent(int userId, String name, String email) {
            this.userId = userId;
            this.name = name;
            this.email = email;
        }
        
        public String getEventType() {
            return "UserCreated";
        }
        
        int getUserId() { return userId; }
        String getName() { return name; }
        String getEmail() { return email; }
    }
    
    static class User {
        private int userId;
        private String name;
        private String email;
        
        User() {
            this.userId = 0;
            this.name = "";
            this.email = "";
        }
        
        void applyEvent(Event event) {
            if (event instanceof UserCreatedEvent) {
                UserCreatedEvent e = (UserCreatedEvent) event;
                this.userId = e.getUserId();
                this.name = e.getName();
                this.email = e.getEmail();
            }
        }
        
        int getUserId() { return userId; }
        String getName() { return name; }
    }
    
    static class EventStore {
        private List<Event> events;
        private Map<Integer, List<Event>> aggregateEvents;
        
        EventStore() {
            events = new ArrayList<>();
            aggregateEvents = new HashMap<>();
        }
        
        void append(int aggregateId, Event event) {
            events.add(event);
            aggregateEvents.computeIfAbsent(aggregateId, k -> new ArrayList<>())
                          .add(event);
            logger.info("[EventStore] Stored: " + event.getEventType());
        }
        
        List<Event> getEvents(int aggregateId) {
            return aggregateEvents.getOrDefault(aggregateId, new ArrayList<>());
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("EVENT SOURCING PATTERN");
        logger.info(separator);
        logger.info("");
        
        EventStore store = new EventStore();
        int userId = 1;
        
        store.append(userId, new UserCreatedEvent(userId, "Alice", "alice@example.com"));
        logger.info("");
        
        User user = new User();
        for (Event event : store.getEvents(userId)) {
            user.applyEvent(event);
        }
        
        logger.info("Reconstructed user: " + user.getName());
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern: Stores state as events");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}