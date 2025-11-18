import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Caching implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Get value from cache.
     */
    public Object get(String key) {
        logger.info("Executing get");
        return null;
    }

    /**
     * Put value in cache.
     */
    public Object put(String key, Object value) {
        logger.info("Executing put");
        return null;
    }

    /**
     * Clear cache.
     */
    public Object clear() {
        logger.info("Executing clear");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Caching");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Optional[any] result = algo.get("");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
