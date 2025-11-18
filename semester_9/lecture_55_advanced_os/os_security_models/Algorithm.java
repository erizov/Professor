import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Os Security Models implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Create security subject.
     */
    public Object create_subject(String subject_id, Object level) {
        logger.info("Executing create_subject");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Create security object.
     */
    public Object create_object(String object_id, Object level) {
        logger.info("Executing create_object");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Check access using Bell-LaPadula model.
     */
    public boolean check_access(String subject_id, String object_id, String permission) {
        logger.info("Executing check_access");
        return false;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Os Security Models");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.create_subject("", null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
