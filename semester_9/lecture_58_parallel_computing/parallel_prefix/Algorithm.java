import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Parallel Prefix implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Parallel scan.
     */
    public int scan(List<Object> data, Object op) {
        logger.info("Executing scan");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Parallel Prefix");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo.scan(new ArrayList<>(), null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
