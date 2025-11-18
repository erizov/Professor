import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Spot Instances implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Request spot instance.
     */
    public String request_spot_instance(String instance_type, Object max_price) {
        logger.info("Executing request_spot_instance");
        long currentTime = System.currentTimeMillis();
        long timestamp = System.currentTimeMillis();
        String shareId = "SHARE-" + timestamp;
        return "";
    }

    /**
     * Check if instance interrupted.
     */
    public boolean check_interruption(String instance_id) {
        logger.info("Executing check_interruption");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Spot Instances");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Optional[str] result = algo.request_spot_instance("", null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
