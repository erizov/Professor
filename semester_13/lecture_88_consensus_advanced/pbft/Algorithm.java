import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Pbft implementation.
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
     * Prepare phase.
     */
    public Object prepare(String proposal_id, String node_id) {
        logger.info("Executing prepare");
        return null;
    }

    /**
     * Commit phase.
     */
    public boolean commit(String proposal_id, String node_id) {
        logger.info("Executing commit");
        return false;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Pbft");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.add_node("");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
