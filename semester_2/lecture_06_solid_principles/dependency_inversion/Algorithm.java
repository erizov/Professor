/**
 * Dependency Inversion Principle (DIP) implementation.
 * 
 * High-level modules should not depend on low-level modules. Both should
 * depend on abstractions. Abstractions should not depend on details.
 * Details should depend on abstractions.
 */
interface DatabaseConnection {
    void connect();
    String[] query(String sql);
}

import java.util.logging.Logger;
class MySQLConnection implements DatabaseConnection {
    public void connect() {
        logger.info("Connecting to MySQL database...");
    }
    
    public String[] query(String sql) {
        logger.info("Executing MySQL query: " + sql);
        return new String[0];
    }
}

class PostgreSQLConnection implements DatabaseConnection {
    public void connect() {
        logger.info("Connecting to PostgreSQL database...");
    }
    
    public String[] query(String sql) {
        logger.info("Executing PostgreSQL query: " + sql);
        return new String[0];
    }
}

class UserService {
    private DatabaseConnection db;
    
    public UserService(DatabaseConnection db) {
        this.db = db;
        this.db.connect();
    }
    
    public String[] getUsers() {
        return db.query("SELECT * FROM users");
    }
}

public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("DEPENDENCY INVERSION PRINCIPLE DEMONSTRATION");
        logger.info("=".repeat(70));
        logger.info();
        
        // Example 1: Using MySQL
        logger.info("Example 1: UserService with MySQL");
        logger.info("-".repeat(70));
        DatabaseConnection mysql = new MySQLConnection();
        UserService service1 = new UserService(mysql);
        service1.getUsers();
        logger.info();
        
        // Example 2: Using PostgreSQL
        logger.info("Example 2: UserService with PostgreSQL");
        logger.info("-".repeat(70));
        DatabaseConnection postgres = new PostgreSQLConnection();
        UserService service2 = new UserService(postgres);
        service2.getUsers();
        logger.info();
        
        logger.info("=".repeat(70));
        logger.info("\nPrinciple Summary:");
        logger.info("\nIntent:");
        logger.info("  High-level modules should not depend on low-level");
        logger.info("  modules. Both should depend on abstractions.");
        logger.info("\nKey Benefits:");
        logger.info("  - Loose coupling");
        logger.info("  - Easy to test (dependency injection)");
        logger.info("  - Flexible and extensible");
        logger.info("  - Reusable components");
        logger.info("=".repeat(70));
    }
}