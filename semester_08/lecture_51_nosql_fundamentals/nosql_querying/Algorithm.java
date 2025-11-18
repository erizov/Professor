import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Nosql Querying implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Query collection.
     */
    public List<Object> query(String collection, Object filter_dict) {
        logger.info("Executing query");
        return null;
    }

    /**
     * Find one document.
     */
    public Map<String, Object> find_one(String collection, Object filter_dict) {
        logger.info("Executing find_one");
        return null;
    }

    /**
     * Count documents.
     */
    public int count(String collection, Object filter_dict) {
        logger.info("Executing count");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Nosql Querying");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        List<Object> result = algo.query("", null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
