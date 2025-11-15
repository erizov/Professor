import java.util.*;

/**
 * Event Sourcing Pattern.
 * 
 * Stores state changes as events.
 */
public class Algorithm {
    
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
            System.out.println("[EventStore] Stored: " + event.getEventType());
        }
        
        List<Event> getEvents(int aggregateId) {
            return aggregateEvents.getOrDefault(aggregateId, new ArrayList<>());
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("EVENT SOURCING PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        EventStore store = new EventStore();
        int userId = 1;
        
        store.append(userId, new UserCreatedEvent(userId, "Alice", "alice@example.com"));
        System.out.println();
        
        User user = new User();
        for (Event event : store.getEvents(userId)) {
            user.applyEvent(event);
        }
        
        System.out.println("Reconstructed user: " + user.getName());
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Stores state as events");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
