import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
package semester_02.lecture_09_behavioral_patterns.chain_of_responsibility;
 * Chain Of Responsibility implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Set next handler.
     */
    public Object set_next(Object handler) {
        logger.info("Executing set_next");
        return null;
    }

    /**
     * Handle request.
     */
    public String handle(String request) {
        logger.info("Executing handle");
        return null;
    }

    /**
     * Concrete handler B.
     */
    public String handle2(String request) {
        logger.info("Executing handle");
        return null;
    }

    /**
     * Handle
     */
    public String handle3(String request) {
        logger.info("Executing handle");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Chain Of Responsibility");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.set_next(null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
