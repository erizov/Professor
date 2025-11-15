import java.util.*;

/**
 * CQRS (Command Query Responsibility Segregation) Pattern.
 * 
 * Separates read and write operations.
 */
public class Algorithm {
    
    static class User {
        private int userId;
        private String name;
        private String email;
        
        User(int userId, String name, String email) {
            this.userId = userId;
            this.name = name;
            this.email = email;
        }
        
        int getUserId() { return userId; }
        String getName() { return name; }
        String getEmail() { return email; }
    }
    
    static class CreateUserCommand {
        String name;
        String email;
        
        CreateUserCommand(String name, String email) {
            this.name = name;
            this.email = email;
        }
    }
    
    static class CommandHandler {
        private Map<Integer, User> writeStore;
        private int nextId;
        
        CommandHandler() {
            writeStore = new HashMap<>();
            nextId = 1;
        }
        
        int handleCreateUser(CreateUserCommand command) {
            User user = new User(nextId++, command.name, command.email);
            writeStore.put(user.getUserId(), user);
            System.out.println("[Command] Created user: " + user.getName());
            return user.getUserId();
        }
    }
    
    static class QueryHandler {
        private Map<Integer, User> readStore;
        
        QueryHandler(Map<Integer, User> store) {
            this.readStore = store;
        }
        
        User handleGetUser(int userId) {
            User user = readStore.get(userId);
            if (user != null) {
                System.out.println("[Query] Retrieved user: " + user.getName());
            }
            return user;
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("CQRS PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        CommandHandler commandHandler = new CommandHandler();
        QueryHandler queryHandler = new QueryHandler(commandHandler.writeStore);
        
        int userId = commandHandler.handleCreateUser(
            new CreateUserCommand("Alice", "alice@example.com")
        );
        System.out.println();
        
        queryHandler.handleGetUser(userId);
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Separates commands and queries");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
