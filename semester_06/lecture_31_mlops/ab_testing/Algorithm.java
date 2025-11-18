import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Ab Testing implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Add result to group A.
     */
    public Object add_result_a(Object value) {
        logger.info("Executing add_result_a");
        return null;
    }

    /**
     * Add result to group B.
     */
    public Object add_result_b(Object value) {
        logger.info("Executing add_result_b");
        return null;
    }

    /**
     * Calculate mean.
     */
    public int mean(List<Object> group) {
        logger.info("Executing mean");
        return null;
    }

    /**
     * Calculate standard deviation.
     */
    public int std_dev(List<Object> group) {
        logger.info("Executing std_dev");
        return null;
    }

    /**
     * Perform t-test.
     */
    public int t_test() {
        logger.info("Executing t_test");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Ab Testing");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.add_result_a(null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
