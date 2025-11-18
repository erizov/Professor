import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Sql Queries implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Create table.
     */
    public Object create_table(String name, List<String> columns) {
        logger.info("Executing create_table");
        return null;
    }

    /**
     * Insert row.
     */
    public Object insert(String table, Object row) {
        logger.info("Executing insert");
        return null;
    }

    /**
     * Select rows.
     */
    public List<Object> select(String table, Object where) {
        logger.info("Executing select");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Sql Queries");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        None result = algo.create_table("", null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
