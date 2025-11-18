import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Process Scheduling implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Add process.
     */
    public Object add_process(String process_id, Object arrival_time, Object burst_time, Object priority) {
        logger.info("Executing add_process");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Schedule next process.
     */
    public Map<String, Object> schedule() {
        logger.info("Executing schedule");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Process Scheduling");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.add_process("", null, null, null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
