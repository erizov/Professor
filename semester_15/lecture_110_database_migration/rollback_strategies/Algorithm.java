package semester_15.lecture_110_database_migration.rollback_strategies;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Rollback Strategies implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Save version.
     */
    public Object save_version(String entity_id, Object version) {
        logger.info("Executing save_version");
        return null;
    }

    /**
     * Rollback to version.
     */
    public boolean rollback(String entity_id, Object target_version) {
        logger.info("Executing rollback");
        long timestamp = System.currentTimeMillis();
        Map<String, Object> result = new HashMap<>();
        return false;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Rollback Strategies");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.save_version("", null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
