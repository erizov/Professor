import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Io Scheduling implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Set scheduling algorithm.
     */
    public Object set_algorithm(String algorithm) {
        logger.info("Executing set_algorithm");
        return null;
    }

    /**
     * Enqueue I/O request.
     */
    public Object enqueue_request(Object request) {
        logger.info("Executing enqueue_request");
        return null;
    }

    /**
     * Schedule next I/O request.
     */
    public Map<String, Object> schedule() {
        logger.info("Executing schedule");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Io Scheduling");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.set_algorithm("");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
