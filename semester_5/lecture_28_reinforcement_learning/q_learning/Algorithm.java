import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Q Learning implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Convert state to key.
     */
    public Object get_state_key(List<Object> state) {
        logger.info("Executing get_state_key");
        return null;
    }

    /**
     * Get Q-values for state.
     */
    public int get_q_values(List<Object> state) {
        logger.info("Executing get_q_values");
        return null;
    }

    /**
     * Choose action using epsilon-greedy.
     */
    public int choose_action(List<Object> state) {
        logger.info("Executing choose_action");
        return null;
    }

    /**
     * Update Q-value.
     */
    public Object update(List<Object> state, Object action, Object reward, List<Object> next_state, Object done) {
        logger.info("Executing update");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Q Learning");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        tuple result = algo.get_state_key(null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
