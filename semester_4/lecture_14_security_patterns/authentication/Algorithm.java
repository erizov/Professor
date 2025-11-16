/**
 * Authentication Pattern.
 * 
 * Verifies the identity of a user, process, or device. Ensures that
 * entities are who they claim to be before granting access.
 */
import java.util.*;
import java.security.MessageDigest;
import java.security.SecureRandom;

class User {
    String userId;
    String username;
    String passwordHash;
    
    User(String userId, String username, String passwordHash) {
        this.userId = userId;
        this.username = username;
        this.passwordHash = passwordHash;
    }
}

class AuthenticationService {
    private final Map<String, User> users = new HashMap<>();
    private final Map<String, String> sessions = new HashMap<>();
    
    private String hashPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(password.getBytes());
            StringBuilder sb = new StringBuilder();
            for (byte b : hash) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
    
    User registerUser(String username, String password) {
        if (users.containsKey(username)) {
            throw new IllegalArgumentException("Username already exists");
        }
        
        String passwordHash = hashPassword(password);
        String userId = "user_" + (users.size() + 1);
        User user = new User(userId, username, passwordHash);
        users.put(username, user);
        return user;
    }
    
    String authenticate(String username, String password) {
        if (!users.containsKey(username)) {
            return null;
        }
        
        User user = users.get(username);
        String passwordHash = hashPassword(password);
        
        if (user.passwordHash.equals(passwordHash)) {
            String sessionId = generateSessionId();
            sessions.put(sessionId, user.userId);
            return sessionId;
        }
        
        return null;
    }
    
    User validateSession(String sessionId) {
        if (!sessions.containsKey(sessionId)) {
            return null;
        }
        
        String userId = sessions.get(sessionId);
        for (User user : users.values()) {
            if (user.userId.equals(userId)) {
                return user;
            }
        }
        return null;
    }
    
    boolean logout(String sessionId) {
        if (sessions.containsKey(sessionId)) {
            sessions.remove(sessionId);
            return true;
        }
        return false;
    }
    
    private String generateSessionId() {
        SecureRandom random = new SecureRandom();
        byte[] bytes = new byte[32];
        random.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }
}

class TokenAuth {
    private final Map<String, String> tokens = new HashMap<>();
    private final Map<String, String> users = new HashMap<>();
    
    private String hashPassword(String password) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hash = md.digest(password.getBytes());
            StringBuilder sb = new StringBuilder();
            for (byte b : hash) {
                sb.append(String.format("%02x", b));
            }
            return sb.toString();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
    
    void createUser(String userId, String password) {
        users.put(userId, hashPassword(password));
    }
    
    String login(String userId, String password) {
        if (!users.containsKey(userId)) {
            return null;
        }
        
        String passwordHash = hashPassword(password);
        if (users.get(userId).equals(passwordHash)) {
            String token = generateToken();
            tokens.put(token, userId);
            return token;
        }
        return null;
    }
    
    String validateToken(String token) {
        return tokens.get(token);
    }
    
    private String generateToken() {
        SecureRandom random = new SecureRandom();
        byte[] bytes = new byte[32];
        random.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }
}

import java.util.Base64;

public class Algorithm {
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("AUTHENTICATION PATTERN DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Session-based Authentication
        System.out.println("Example 1: Session-based Authentication");
        System.out.println("-".repeat(70));
        
        AuthenticationService authService = new AuthenticationService();
        
        User user1 = authService.registerUser("alice", "password123");
        User user2 = authService.registerUser("bob", "secret456");
        
        System.out.printf("Registered users: %s, %s%n", user1.username, user2.username);
        System.out.println();
        
        String session1 = authService.authenticate("alice", "password123");
        String session2 = authService.authenticate("bob", "wrong_password");
        
        System.out.printf("Alice login: %s%n", session1 != null ? "Success" : "Failed");
        System.out.printf("Bob login (wrong password): %s%n",
                         session2 != null ? "Success" : "Failed");
        System.out.println();
        
        if (session1 != null) {
            User user = authService.validateSession(session1);
            System.out.printf("Session validated: %s%n",
                            user != null ? user.username : "Invalid");
            authService.logout(session1);
            System.out.println("Logged out");
        }
        System.out.println();
        
        // Example 2: Token-based Authentication
        System.out.println("Example 2: Token-based Authentication");
        System.out.println("-".repeat(70));
        
        TokenAuth tokenAuth = new TokenAuth();
        tokenAuth.createUser("user1", "password123");
        tokenAuth.createUser("user2", "secret456");
        
        String token = tokenAuth.login("user1", "password123");
        System.out.printf("Login token: %s...%n",
                         token != null ? token.substring(0, Math.min(20, token.length())) : "Login failed");
        
        if (token != null) {
            String userId = tokenAuth.validateToken(token);
            System.out.printf("Token validated: %s%n", userId);
        }
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern Summary:");
        System.out.println("\nIntent:");
        System.out.println("  Verify the identity of a user, process, or device.");
        System.out.println("  Ensures entities are who they claim to be.");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Security and access control");
        System.out.println("  - User identification");
        System.out.println("  - Session management");
        System.out.println("  - Audit trail");
        System.out.println("\nWhen to Use:");
        System.out.println("  - User login systems");
        System.out.println("  - API authentication");
        System.out.println("  - Secure access control");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
