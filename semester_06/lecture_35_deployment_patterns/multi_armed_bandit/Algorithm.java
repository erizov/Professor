import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Multi Armed Bandit implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Select arm using epsilon-greedy.
     */
    public int select_arm(Object epsilon) {
        logger.info("Executing select_arm");
        return null;
    }

    /**
     * Update arm value.
     */
    public Object update(Object arm, Object reward) {
        logger.info("Executing update");
        return null;
    }

    /**
     * Upper Confidence Bound selection.
     */
    public int ucb(Object c) {
        logger.info("Executing ucb");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Multi Armed Bandit");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo.select_arm(null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
