import java.util.*;

/**
 * Repository Design Pattern.
 * 
 * Abstracts data access layer.
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
        void setEmail(String email) { this.email = email; }
        
        public String toString() {
            return String.format("User(id=%d, name='%s', email='%s')",
                               userId, name, email);
        }
    }
    
    interface IUserRepository {
        void add(User user);
        User getById(int userId);
        List<User> getAll();
        boolean update(User user);
        boolean delete(int userId);
    }
    
    static class InMemoryUserRepository implements IUserRepository {
        private Map<Integer, User> users;
        private int nextId;
        
        InMemoryUserRepository() {
            users = new HashMap<>();
            nextId = 1;
        }
        
        public void add(User user) {
            if (user.getUserId() == 0) {
                user = new User(nextId++, user.getName(), user.getEmail());
            }
            users.put(user.getUserId(), user);
        }
        
        public User getById(int userId) {
            return users.get(userId);
        }
        
        public List<User> getAll() {
            return new ArrayList<>(users.values());
        }
        
        public boolean update(User user) {
            if (users.containsKey(user.getUserId())) {
                users.put(user.getUserId(), user);
                return true;
            }
            return false;
        }
        
        public boolean delete(int userId) {
            return users.remove(userId) != null;
        }
    }
    
    static class UserService {
        private IUserRepository repository;
        
        UserService(IUserRepository repository) {
            this.repository = repository;
        }
        
        User createUser(String name, String email) {
            User user = new User(0, name, email);
            repository.add(user);
            return user;
        }
        
        List<User> getAllUsers() {
            return repository.getAll();
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("REPOSITORY DESIGN PATTERN");
        logger.info(separator);
        logger.info("");
        
        IUserRepository repository = new InMemoryUserRepository();
        UserService service = new UserService(repository);
        
        service.createUser("Alice", "alice@example.com");
        service.createUser("Bob", "bob@example.com");
        
        logger.info("Users:");
        service.getAllUsers().forEach(u -> logger.info("  " + u));
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern: Abstracts data access");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
