import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Load Balancing implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Add server.
     */
    public Object add_server(String server_id, Object capacity) {
        logger.info("Executing add_server");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Select server based on algorithm.
     */
    public String select_server() {
        logger.info("Executing select_server");
        return null;
    }

    /**
     * Route request to server.
     */
    public String route_request(Object request) {
        logger.info("Executing route_request");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Load Balancing");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        None result = algo.add_server("", null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
