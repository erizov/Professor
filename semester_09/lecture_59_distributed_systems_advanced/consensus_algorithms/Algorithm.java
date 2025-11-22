package semester_09.lecture_59_distributed_systems_advanced.consensus_algorithms;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Consensus Algorithms implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Propose value (to be implemented by subclasses).
     */
    public boolean propose(Object value) {
        logger.info("Executing propose");
        return false;
    }

    /**
     * Get consensus value (to be implemented by subclasses).
     */
    public Object get_consensus() {
        logger.info("Executing get_consensus");
        return null;
    }

    /**
     * Propose value (only leader can propose).
     */
    public boolean propose2(Object value) {
        logger.info("Executing propose");
        return false;
    }

    /**
     * Get committed value.
     */
    public Object get_consensus2() {
        logger.info("Executing get_consensus");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("Consensus Algorithms");
        logger.info("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        boolean result = algo.propose(null);
        logger.info("Result: " + result);
        logger.info("=".repeat(70));
    }
}
