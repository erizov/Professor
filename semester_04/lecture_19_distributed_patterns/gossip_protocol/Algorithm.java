// package semester_04.lecture_19_distributed_patterns.gossip_protocol;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Gossip Protocol implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Update local state.
     */
    public Object update_state(String key, Object value) {
        logger.info("Executing update_state");
        return null;
    }

    /**
     * Gossip with target node.
     */
    public Object gossip(String target_node) {
        logger.info("Executing gossip");
        return null;
    }

    /**
     * Merge received state.
     */
    public Object merge_states(String other_state, Object any) {
        logger.info("Executing merge_states");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("Gossip Protocol");
        logger.info("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.update_state("", null);
        logger.info("Result: " + result);
        logger.info("=".repeat(70));
    }
}
