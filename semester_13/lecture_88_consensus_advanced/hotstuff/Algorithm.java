import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Hotstuff implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Add node.
     */
    public Object add_node(String node_id) {
        logger.info("Executing add_node");
        return null;
    }

    /**
     * Propose value.
     */
    public Object propose(String proposal_id, Object value) {
        logger.info("Executing propose");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Vote on proposal.
     */
    public Object vote(String proposal_id, String node_id, Object vote) {
        logger.info("Executing vote");
        return null;
    }

    /**
     * Decide on proposal.
     */
    public boolean decide(String proposal_id) {
        logger.info("Executing decide");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Hotstuff");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        None result = algo.add_node("");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
