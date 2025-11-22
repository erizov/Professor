// package semester_04.lecture_19_distributed_patterns.leader_election;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Leader Election implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Elect leader (highest ID wins).
     */
    public int elect_leader() {
        logger.info("Executing elect_leader");
        return -1;
    }

    /**
     * Check if this node is leader.
     */
    public boolean is_leader() {
        logger.info("Executing is_leader");
        return false;
    }

    /**
     * Get current leader.
     */
    public int get_leader() {
        logger.info("Executing get_leader");
        return -1;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Leader Election");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo.elect_leader();
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
