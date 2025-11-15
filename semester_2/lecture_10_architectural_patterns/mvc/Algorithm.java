import java.util.*;

/**
 * Model-View-Controller (MVC) Pattern.
 * 
 * Separates application into Model, View, and Controller.
 */
public class Algorithm {
    
    // Model
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
        
        public String toString() {
            return String.format("User(id=%d, name='%s', email='%s')",
                               userId, name, email);
        }
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
        
        User getUser(int userId) {
            return users.stream()
                       .filter(u -> u.getUserId() == userId)
                       .findFirst()
                       .orElse(null);
        }
        
        List<User> getAllUsers() {
            return new ArrayList<>(users);
        }
        
        boolean updateUser(int userId, String name, String email) {
            User user = getUser(userId);
            if (user != null) {
                if (name != null) user.setName(name);
                if (email != null) user.setEmail(email);
                return true;
            }
            return false;
        }
    }
    
    // View
    static class UserView {
        void displayUser(User user) {
            System.out.println("User Details:");
            System.out.println("  ID: " + user.getUserId());
            System.out.println("  Name: " + user.getName());
            System.out.println("  Email: " + user.getEmail());
            System.out.println();
        }
        
        void displayUsers(List<User> users) {
            System.out.println("Users List:");
            users.forEach(u -> System.out.println("  " + u));
            System.out.println();
        }
        
        void displayMessage(String message) {
            System.out.println("Message: " + message);
            System.out.println();
        }
    }
    
    // Controller
    static class UserController {
        private UserModel model;
        private UserView view;
        
        UserController(UserModel model, UserView view) {
            this.model = model;
            this.view = view;
        }
        
        void createUser(String name, String email) {
            model.createUser(name, email);
            view.displayMessage("User created: " + name);
        }
        
        void showUser(int userId) {
            User user = model.getUser(userId);
            if (user != null) {
                view.displayUser(user);
            } else {
                view.displayMessage("User " + userId + " not found");
            }
        }
        
        void showAllUsers() {
            view.displayUsers(model.getAllUsers());
        }
    }
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("MODEL-VIEW-CONTROLLER (MVC) PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        UserModel model = new UserModel();
        UserView view = new UserView();
        UserController controller = new UserController(model, view);
        
        controller.createUser("Alice", "alice@example.com");
        controller.createUser("Bob", "bob@example.com");
        controller.showAllUsers();
        controller.showUser(1);
        
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Separates Model, View, and Controller");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
