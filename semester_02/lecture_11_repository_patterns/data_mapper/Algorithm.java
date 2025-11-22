import java.util.*;

/**
 * Data Mapper Design Pattern.
 * 
 * Maps between domain objects and database.
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
    
    static class UserDTO {
        private int userId;
        private String name;
        private String email;
        private String createdAt;
        
        UserDTO(int userId, String name, String email, String createdAt) {
            this.userId = userId;
            this.name = name;
            this.email = email;
            this.createdAt = createdAt;
        }
        
        int getUserId() { return userId; }
        String getName() { return name; }
        String getEmail() { return email; }
    }
    
    static class UserMapper {
        static UserDTO toDTO(User user) {
            return new UserDTO(user.getUserId(), user.getName(), 
                             user.getEmail(), "2024-01-01");
        }
        
        static User toDomain(UserDTO dto) {
            return new User(dto.getUserId(), dto.getName(), dto.getEmail());
        }
    }
    
    static class UserDataAccess {
        private Map<Integer, UserDTO> storage;
        private int nextId;
        
        UserDataAccess() {
            storage = new HashMap<>();
            nextId = 1;
        }
        
        int insert(UserDTO dto) {
            if (dto.getUserId() == 0) {
                dto = new UserDTO(nextId++, dto.getName(), 
                                dto.getEmail(), dto.createdAt);
            }
            storage.put(dto.getUserId(), dto);
            return dto.getUserId();
        }
        
        UserDTO findById(int userId) {
            return storage.get(userId);
        }
    }
    
    static class UserRepository {
        private UserDataAccess dataAccess;
        
        UserRepository(UserDataAccess dataAccess) {
            this.dataAccess = dataAccess;
        }
        
        User save(User user) {
            UserDTO dto = UserMapper.toDTO(user);
            int id = dataAccess.insert(dto);
            return new User(id, user.getName(), user.getEmail());
        }
        
        User findById(int userId) {
            UserDTO dto = dataAccess.findById(userId);
            return dto != null ? UserMapper.toDomain(dto) : null;
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("DATA MAPPER DESIGN PATTERN");
        logger.info(separator);
        logger.info("");
        
        UserDataAccess dataAccess = new UserDataAccess();
        UserRepository repository = new UserRepository(dataAccess);
        
        User user = new User(0, "Alice", "alice@example.com");
        User saved = repository.save(user);
        
        logger.info("Saved: " + saved.getName());
        
        User found = repository.findById(saved.getUserId());
        logger.info("Found: " + found.getName());
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern: Maps between domain and database");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
