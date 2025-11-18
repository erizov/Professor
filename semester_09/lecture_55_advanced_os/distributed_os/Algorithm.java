import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Distributed Os implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Register node.
     */
    public Object register_node(String node_id, Object resources) {
        logger.info("Executing register_node");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Allocate resource.
     */
    public String allocate_resource(String resource_type, Object amount) {
        logger.info("Executing allocate_resource");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Distributed Os");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.register_node("", null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
