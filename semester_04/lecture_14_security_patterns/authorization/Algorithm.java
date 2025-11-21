package semester_04.lecture_14_security_patterns.authorization;

import java.util.ArrayList;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.logging.Logger;

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Authorization");
        System.out.println("=".repeat(70));

        AuthorizationService authz = new AuthorizationService();

        Role adminRole = authz.createRole("admin", EnumSet.of(Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN));
        Role editorRole = authz.createRole("editor", EnumSet.of(Permission.READ, Permission.WRITE));
        Role viewerRole = authz.createRole("viewer", EnumSet.of(Permission.READ));

        authz.createUser("u1", "alice", List.of(adminRole));
        authz.createUser("u2", "bob", List.of(editorRole));
        authz.createUser("u3", "charlie", List.of(viewerRole));

        System.out.printf("Alice can delete: %s%n", authz.authorize("u1", Permission.DELETE));
        System.out.printf("Bob can delete: %s%n", authz.authorize("u2", Permission.DELETE));
        System.out.printf("Charlie can read: %s%n", authz.authorize("u3", Permission.READ));

        System.out.println("=".repeat(70));
    }
}

enum Permission {
    READ, WRITE, DELETE, ADMIN
}

class Role {
    private final String name;
    private final Set<Permission> permissions;

    Role(String name, Set<Permission> permissions) {
        this.name = name;
        this.permissions = permissions;
    }

    boolean hasPermission(Permission permission) {
        return permissions.contains(permission);
    }

    String getName() {
        return name;
    }
}

class User {
    private final String id;
    private final String username;
    private final List<Role> roles;

    User(String id, String username, List<Role> roles) {
        this.id = id;
        this.username = username;
        this.roles = roles;
    }

    boolean hasPermission(Permission permission) {
        return roles.stream().anyMatch(role -> role.hasPermission(permission));
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

    User createUser(String id, String username, List<Role> roleList) {
        User user = new User(id, username, new ArrayList<>(roleList));
        users.put(id, user);
        return user;
    }

    boolean authorize(String userId, Permission permission) {
        User user = users.get(userId);
        return user != null && user.hasPermission(permission);
    }
}

