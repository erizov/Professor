import java.util.*;

/**
 * Model-View-ViewModel (MVVM) Pattern.
 * 
 * Separates View from Model using ViewModel.
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
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("MODEL-VIEW-VIEWMODEL (MVVM) PATTERN");
        System.out.println("=".repeat(70));
        System.out.println();
        
        UserModel model = new UserModel();
        UserViewModel viewModel = new UserViewModel(model);
        
        viewModel.createUser("Alice", "alice@example.com");
        viewModel.createUser("Bob", "bob@example.com");
        viewModel.loadUsers();
        
        System.out.println("Users: " + viewModel.getUserCount());
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern: Separates View from Model");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
