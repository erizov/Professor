        
                    AuthorizationService authz = new AuthorizationService();
        
                    Role adminRole = authz.createRole("admin", EnumSet.of(
                        Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN));
                    Role editorRole = authz.createRole("editor", EnumSet.of(
                        Permission.READ, Permission.WRITE));
                    Role viewerRole = authz.createRole("viewer", EnumSet.of(Permission.READ));
        
                    logger.info("Created roles:");
                    System.out.printf("  Admin: %s%n", adminRole.permissions);
                    System.out.printf("  Editor: %s%n", editorRole.permissions);
                    System.out.printf("  Viewer: %s%n", viewerRole.permissions);
                    logger.info("");
        
                    User adminUser = authz.createUser("u1", "alice", Arrays.asList("admin"));
                    User editorUser = authz.createUser("u2", "bob", Arrays.asList("editor"));
                    User viewerUser = authz.createUser("u3", "charlie", Arrays.asList("viewer"));
        
                    logger.info("Permission checks:");
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
                    logger.info("");
        
                    // Example 2: RBAC
                    logger.info("Example 2: RBAC (Role-Based Access Control)");
                    logger.info(dash);
        
                    RBAC rbac = new RBAC();
        
                    rbac.addRole("admin", Arrays.asList("read", "write", "delete", "manage"));
                    rbac.addRole("user", Arrays.asList("read", "write"));
                    rbac.addRole("guest", Arrays.asList("read"));
        
                    rbac.assignRole("user1", "admin");
                    rbac.assignRole("user2", "user");
                    rbac.assignRole("user3", "guest");
        
                    logger.info("Permission checks:");
                    System.out.printf("User1 (admin) can delete: %s%n",
                                     rbac.hasPermission("user1", "delete"));
                    System.out.printf("User2 (user) can write: %s%n",
                                     rbac.hasPermission("user2", "write"));
                    System.out.printf("User2 (user) can delete: %s%n",
                                     rbac.hasPermission("user2", "delete"));
                    System.out.printf("User3 (guest) can read: %s%n",
                                     rbac.hasPermission("user3", "read"));
                    logger.info("");
        
                    long endTime = System.nanoTime();
        
                    logger.info(separator);
                    logger.info("\nPattern Summary:");
                    logger.info("\nIntent:");
                    logger.info("  Determines what actions a user is allowed to perform");
                    logger.info("  after authentication. Controls access to resources.");
                    logger.info("\nKey Advantages:");
                    logger.info("  - Fine-grained access control");
                    logger.info("  - Role-based management");
                    logger.info("  - Centralized authorization");
                    logger.info("  - Scalable permissions");
                    logger.info("\nWhen to Use:");
                    logger.info("  - Multi-user systems");
                    logger.info("  - Need fine-grained permissions");
                    logger.info("  - Role-based access");
                    logger.info(separator);
                    System.out.printf("\nTotal time: %.3f ms%n",
                                    (endTime - startTime) / 1_000_000.0);
                }
        private final Map<String, Role> roles = new HashMap<>();
    
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
                    logger.info(dash);
                    logger.info("Example 1: Role-based Authorization");
                    // Example 1: Role-based Authorization
        
                    logger.info("");
                    logger.info(separator);
                    logger.info("AUTHORIZATION PATTERN DEMONSTRATION");
                    logger.info(separator);
        
                    long startTime = System.nanoTime();
                    String dash = "-".repeat(70);
                    String separator = "=".repeat(70);
            private final Map<String, User> users = new HashMap<>();
    class AuthorizationService {
                public static void main(String[] args) {
/**
package semester_04.lecture_14_security_patterns.authorization;
 * Authorization Pattern.
 * 
 * Determines what actions a user is allowed to perform after authentication.
 * Controls access to resources based on user roles and permissions.
 */
import java.util.*;

enum Permission {
    READ, WRITE, DELETE, ADMIN
}

import java.util.logging.Logger;
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
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    
}