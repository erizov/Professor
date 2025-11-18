import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Nosql Indexing implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Create index.
     */
    public Object create_index(String collection, String field) {
        logger.info("Executing create_index");
        return null;
    }

    /**
     * Build index.
     */
    public Object build_index(String collection, String field) {
        logger.info("Executing build_index");
        return null;
    }

    /**
     * Query using index.
     */
    public List<Object> query_with_index(String collection, String field, Object value) {
        logger.info("Executing query_with_index");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Nosql Indexing");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.create_index("", "");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
