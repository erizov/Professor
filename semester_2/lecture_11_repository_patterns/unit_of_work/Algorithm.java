import java.util.*;

/**
 * Unit of Work Design Pattern.
 * 
 * Tracks changes and commits atomically.
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
        void setName(String name) { this.name = name; }
        void setEmail(String email) { this.email = email; }
    }
    
    interface IUserRepository {
        void add(User user);
        void update(User user);
        void delete(User user);
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
            System.out.println("  Added: " + user.getName());
        }
        
        public void update(User user) {
            users.put(user.getUserId(), user);
            System.out.println("  Updated: " + user.getName());
        }
        
        public void delete(User user) {
            users.remove(user.getUserId());
            System.out.println("  Deleted: " + user.getName());
        }
    }
    
    static class UnitOfWork {
        private IUserRepository repository;
        private Set<User> newEntities;
        private Set<User> modifiedEntities;
        private Set<User> deletedEntities;
        
        UnitOfWork(IUserRepository repository) {
            this.repository = repository;
            this.newEntities = new HashSet<>();
            this.modifiedEntities = new HashSet<>();
            this.deletedEntities = new HashSet<>();
        }
        
        void registerNew(User entity) {
            deletedEntities.remove(entity);
            if (!modifiedEntities.contains(entity)) {
                newEntities.add(entity);
            }
        }
        
        void registerModified(User entity) {
            if (!newEntities.contains(entity) && 
                !deletedEntities.contains(entity)) {
                modifiedEntities.add(entity);
            }
        }
        
        void registerDeleted(User entity) {
            newEntities.remove(entity);
            modifiedEntities.remove(entity);
            deletedEntities.add(entity);
        }
        
        void commit() {
            newEntities.forEach(repository::add);
            modifiedEntities.forEach(repository::update);
            deletedEntities.forEach(repository::delete);
            
            newEntities.clear();
            modifiedEntities.clear();
            deletedEntities.clear();
            
            System.out.println("Unit of Work committed");
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("UNIT OF WORK DESIGN PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        IUserRepository repository = new InMemoryUserRepository();
        UnitOfWork uow = new UnitOfWork(repository);
        
        User user1 = new User(0, "Alice", "alice@example.com");
        User user2 = new User(0, "Bob", "bob@example.com");
        
        uow.registerNew(user1);
        uow.registerNew(user2);
        
        System.out.println("Committing changes:");
        uow.commit();
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Tracks changes atomically");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
