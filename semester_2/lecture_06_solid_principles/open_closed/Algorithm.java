import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Open Closed implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Define base class.
     */
    public Object define_base(String base_name, List<String> methods) {
        logger.info("Executing define_base");
        return null;
    }

    /**
     * Extend base class.
     */
    public Object extend(String extension_name, String base_name, List<String> new_methods) {
        logger.info("Executing extend");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Get all methods for class.
     */
    public String get_methods(String class_name) {
        logger.info("Executing get_methods");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Open Closed");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        None result = algo.define_base("", null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
