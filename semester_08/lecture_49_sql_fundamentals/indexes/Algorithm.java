import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Indexes implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Create index on column.
     */
    public Object create_index(List<Object> column_values) {
        logger.info("Executing create_index");
        return null;
    }

    /**
     * Search using index.
     */
    public int search(Object value) {
        logger.info("Executing search");
        return null;
    }

    /**
     * Range search.
     */
    public int range_search(Object min_value, Object max_value) {
        logger.info("Executing range_search");
        return null;
    }

    /**
     * Insert into index.
     */
    public Object insert(Object value, Object position) {
        logger.info("Executing insert");
        return null;
    }

    /**
     * Delete from index.
     */
    public Object delete(Object value, Object position) {
        logger.info("Executing delete");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Indexes");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.create_index(new ArrayList<>());
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
