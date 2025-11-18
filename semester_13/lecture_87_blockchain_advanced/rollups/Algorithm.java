import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Rollups implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Add raw data.
     */
    public Object add_data(Object timestamp, Object value) {
        logger.info("Executing add_data");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Create rollup.
     */
    public Map<String, Object> create_rollup(String interval, List<Object> data) {
        logger.info("Executing create_rollup");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Rollups");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.add_data(null, null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
