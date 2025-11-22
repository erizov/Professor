import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
package semester_05.lecture_28_reinforcement_learning.dqn;
 * Dqn implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Get Q-values for state.
     */
    public int get_q_values(List<Object> state) {
        logger.info("Executing get_q_values");
        return -1;
    }

    /**
     * Choose action using epsilon-greedy.
     */
    public int choose_action(List<Object> state, Object epsilon) {
        logger.info("Executing choose_action");
        return -1;
    }

    /**
     * Store transition in replay buffer.
     */
    public Object store_transition(List<Object> state, Object action, Object reward, List<Object> next_state, Object done) {
        logger.info("Executing store_transition");
        return null;
    }

    /**
     * Train DQN.
     */
    public Object train(Object batch_size, Object gamma) {
        logger.info("Executing train");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Dqn");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo.get_q_values(new ArrayList<>());
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
