import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Joins implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Create table.
     */
    public Object create_table(String table_name, List<Object> data) {
        logger.info("Executing create_table");
        return null;
    }

    /**
     * Inner join.
     */
    public List<Object> inner_join(String table1, String table2, String on) {
        logger.info("Executing inner_join");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Left join.
     */
    public List<Object> left_join(String table1, String table2, String on) {
        logger.info("Executing left_join");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Joins");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        None result = algo.create_table("", null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
