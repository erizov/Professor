// package semester_08.lecture_52_nosql_advanced.nosql_sharding;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Nosql Sharding implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Get shard for key.
     */
    public int _get_shard(String key) {
        logger.info("Executing _get_shard");
        return -1;
    }

    /**
     * Put data in shard.
     */
    public Object put(String key, Object value) {
        logger.info("Executing put");
        return null;
    }

    /**
     * Get data from shard.
     */
    public Object get(String key) {
        logger.info("Executing get");
        return null;
    }

    /**
     * Rebalance shards.
     */
    public Object rebalance() {
        logger.info("Executing rebalance");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Nosql Sharding");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo._get_shard("");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
