package semester_02.lecture_06_solid_principles.single_responsibility;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Single Responsibility implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Validates user data.
     */
    public Map<String, Object> get_user(String user_id) {
        logger.info("Executing get_user");
        return null;
    }

    /**
     * Orchestrates user operations.
     */
    public boolean validate(String user) {
        logger.info("Executing validate");
        return false;
    }

    /**
     * Get Validated User
     */
    public Map<String, Object> get_validated_user(String user_id) {
        logger.info("Executing get_validated_user");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Single Responsibility");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.get_user("");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
