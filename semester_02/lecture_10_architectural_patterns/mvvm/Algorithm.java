import java.util.*;

/**
 * Model-View-ViewModel (MVVM) Pattern.
 * 
 * Separates View from Model using ViewModel.
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
    
    static class UserModel {
        private List<User> users;
        private int nextId;
        
        UserModel() {
            users = new ArrayList<>();
            nextId = 1;
        }
        
        User createUser(String name, String email) {
            User user = new User(nextId++, name, email);
            users.add(user);
            return user;
        }
        
        List<User> getAllUsers() {
            return new ArrayList<>(users);
        }
    }
    
    static class UserViewModel {
        private UserModel model;
        private List<User> users;
        private String errorMessage;
        
        UserViewModel(UserModel model) {
            this.model = model;
            this.users = new ArrayList<>();
        }
        
        void loadUsers() {
            users = model.getAllUsers();
            errorMessage = "";
        }
        
        boolean createUser(String name, String email) {
            if (name == null || email == null || !email.contains("@")) {
                errorMessage = "Invalid input";
                return false;
            }
            model.createUser(name, email);
            loadUsers();
            return true;
        }
        
        int getUserCount() {
            return users.size();
        }
    }
    
    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        long startTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("MODEL-VIEW-VIEWMODEL (MVVM) PATTERN");
        logger.info(separator);
        logger.info("");
        
        UserModel model = new UserModel();
        UserViewModel viewModel = new UserViewModel(model);
        
        viewModel.createUser("Alice", "alice@example.com");
        viewModel.createUser("Bob", "bob@example.com");
        viewModel.loadUsers();
        
        logger.info("Users: " + viewModel.getUserCount());
        logger.info("");
        
        long endTime = System.nanoTime();
        
        logger.info(separator);
        logger.info("\nPattern: Separates View from Model");
        logger.info(separator);
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
