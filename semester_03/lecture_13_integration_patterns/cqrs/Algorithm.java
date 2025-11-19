import java.util.*;

/**
 * CQRS (Command Query Responsibility Segregation) Pattern.
 * 
 * Separates read and write operations.
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
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
            logger.info("[Command] Created user: " + user.getName());
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
                logger.info("[Query] Retrieved user: " + user.getName());
            }
            return user;
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("CQRS PATTERN");
        logger.info(separator);
        logger.info("");
        
        CommandHandler commandHandler = new CommandHandler();
        QueryHandler queryHandler = new QueryHandler(commandHandler.writeStore);
        
        int userId = commandHandler.handleCreateUser(
            new CreateUserCommand("Alice", "alice@example.com")
        );
        logger.info("");
        
        queryHandler.handleGetUser(userId);
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern: Separates commands and queries");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}