import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Ppo implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Select action.
     */
    public Object select_action(List<Object> state) {
        logger.info("Executing select_action");
        return null;
    }

    /**
     * Compute advantage.
     */
    public int compute_advantage(List<Object> rewards, List<Object> values) {
        logger.info("Executing compute_advantage");
        return null;
    }

    /**
     * Update policy using PPO.
     */
    public Object update_policy(List<Object> states, List<Object> actions, List<Object> advantages) {
        logger.info("Executing update_policy");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Ppo");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        tuple result = algo.select_action(null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
