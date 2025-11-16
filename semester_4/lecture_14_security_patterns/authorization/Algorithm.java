/**
 * Authorization Pattern.
 * 
 * Determines what actions a user is allowed to perform after authentication.
 * Controls access to resources based on user roles and permissions.
 */
import java.util.*;

enum Permission {
    READ, WRITE, DELETE, ADMIN
}

class Role {
    String name;
    Set<Permission> permissions;
    
    Role(String name, Set<Permission> permissions) {
        this.name = name;
        this.permissions = permissions;
    }
    
    boolean hasPermission(Permission permission) {
        return permissions.contains(permission);
    }
}

class User {
    String userId;
    String username;
    List<Role> roles;
    
    User(String userId, String username, List<Role> roles) {
        this.userId = userId;
        this.username = username;
        this.roles = roles;
    }
    
    boolean hasPermission(Permission permission) {
        return roles.stream().anyMatch(role -> role.hasPermission(permission));
    }
    
    boolean hasRole(String roleName) {
        return roles.stream().anyMatch(role -> role.name.equals(roleName));
    }
}

class AuthorizationService {
    private final Map<String, Role> roles = new HashMap<>();
    private final Map<String, User> users = new HashMap<>();
    
    Role createRole(String name, Set<Permission> permissions) {
        Role role = new Role(name, permissions);
        roles.put(name, role);
        return role;
    }
    
    User createUser(String userId, String username, List<String> roleNames) {
        List<Role> userRoles = new ArrayList<>();
        for (String roleName : roleNames) {
            if (roles.containsKey(roleName)) {
                userRoles.add(roles.get(roleName));
            }
        }
        User user = new User(userId, username, userRoles);
        users.put(userId, user);
        return user;
    }
    
    boolean authorize(String userId, Permission permission) {
        if (!users.containsKey(userId)) {
            return false;
        }
        return users.get(userId).hasPermission(permission);
    }
    
    boolean checkAccess(String userId, String resource, Permission action) {
        return authorize(userId, action);
    }
}

class RBAC {
    private final Map<String, Set<String>> roles = new HashMap<>();
    private final Map<String, Set<String>> userRoles = new HashMap<>();
    
    void addRole(String role, List<String> permissions) {
        this.roles.put(role, new HashSet<>(permissions));
    }
    
    void assignRole(String userId, String role) {
        userRoles.computeIfAbsent(userId, k -> new HashSet<>()).add(role);
    }
    
    boolean hasPermission(String userId, String permission) {
        if (!userRoles.containsKey(userId)) {
            return false;
        }
        
        for (String role : userRoles.get(userId)) {
            if (roles.containsKey(role) && roles.get(role).contains(permission)) {
                return true;
            }
        }
        return false;
    }
}

public class Algorithm {
    
    public static void main(String[] args) {
        long startTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("AUTHORIZATION PATTERN DEMONSTRATION");
        System.out.println("=".repeat(70));
        System.out.println();
        
        // Example 1: Role-based Authorization
        System.out.println("Example 1: Role-based Authorization");
        System.out.println("-".repeat(70));
        
        AuthorizationService authz = new AuthorizationService();
        
        Role adminRole = authz.createRole("admin", EnumSet.of(
            Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN));
        Role editorRole = authz.createRole("editor", EnumSet.of(
            Permission.READ, Permission.WRITE));
        Role viewerRole = authz.createRole("viewer", EnumSet.of(Permission.READ));
        
        System.out.println("Created roles:");
        System.out.printf("  Admin: %s%n", adminRole.permissions);
        System.out.printf("  Editor: %s%n", editorRole.permissions);
        System.out.printf("  Viewer: %s%n", viewerRole.permissions);
        System.out.println();
        
        User adminUser = authz.createUser("u1", "alice", Arrays.asList("admin"));
        User editorUser = authz.createUser("u2", "bob", Arrays.asList("editor"));
        User viewerUser = authz.createUser("u3", "charlie", Arrays.asList("viewer"));
        
        System.out.println("Permission checks:");
        System.out.printf("Alice (admin) can delete: %s%n",
                         authz.authorize("u1", Permission.DELETE));
        System.out.printf("Bob (editor) can write: %s%n",
                         authz.authorize("u2", Permission.WRITE));
        System.out.printf("Bob (editor) can delete: %s%n",
                         authz.authorize("u2", Permission.DELETE));
        System.out.printf("Charlie (viewer) can read: %s%n",
                         authz.authorize("u3", Permission.READ));
        System.out.printf("Charlie (viewer) can write: %s%n",
                         authz.authorize("u3", Permission.WRITE));
        System.out.println();
        
        // Example 2: RBAC
        System.out.println("Example 2: RBAC (Role-Based Access Control)");
        System.out.println("-".repeat(70));
        
        RBAC rbac = new RBAC();
        
        rbac.addRole("admin", Arrays.asList("read", "write", "delete", "manage"));
        rbac.addRole("user", Arrays.asList("read", "write"));
        rbac.addRole("guest", Arrays.asList("read"));
        
        rbac.assignRole("user1", "admin");
        rbac.assignRole("user2", "user");
        rbac.assignRole("user3", "guest");
        
        System.out.println("Permission checks:");
        System.out.printf("User1 (admin) can delete: %s%n",
                         rbac.hasPermission("user1", "delete"));
        System.out.printf("User2 (user) can write: %s%n",
                         rbac.hasPermission("user2", "write"));
        System.out.printf("User2 (user) can delete: %s%n",
                         rbac.hasPermission("user2", "delete"));
        System.out.printf("User3 (guest) can read: %s%n",
                         rbac.hasPermission("user3", "read"));
        System.out.println();
        
        long endTime = System.nanoTime();
        
        System.out.println("=".repeat(70));
        System.out.println("\nPattern Summary:");
        System.out.println("\nIntent:");
        System.out.println("  Determines what actions a user is allowed to perform");
        System.out.println("  after authentication. Controls access to resources.");
        System.out.println("\nKey Advantages:");
        System.out.println("  - Fine-grained access control");
        System.out.println("  - Role-based management");
        System.out.println("  - Centralized authorization");
        System.out.println("  - Scalable permissions");
        System.out.println("\nWhen to Use:");
        System.out.println("  - Multi-user systems");
        System.out.println("  - Need fine-grained permissions");
        System.out.println("  - Role-based access");
        System.out.println("=".repeat(70));
        System.out.printf("\nTotal time: %.3f ms%n",
                        (endTime - startTime) / 1_000_000.0);
    }
}
