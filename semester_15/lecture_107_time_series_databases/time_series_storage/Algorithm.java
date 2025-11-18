import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Time Series Storage implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Write data point.
     */
    public Object write(String series_id, Object timestamp, Object value) {
        logger.info("Executing write");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Read time range.
     */
    public List<Object> read(String series_id, Object start_time, Object end_time) {
        logger.info("Executing read");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Time Series Storage");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.write("", null, null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
