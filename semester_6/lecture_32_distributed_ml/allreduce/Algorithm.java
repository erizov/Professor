import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Allreduce implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Reduce gradients across workers.
     */
    public int reduce(List<Object> gradients, String operation) {
        logger.info("Executing reduce");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Allreduce");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo.reduce(new ArrayList<>(), "");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
