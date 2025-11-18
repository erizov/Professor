import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Template Method implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Template method.
     */
    public String template_method() {
        logger.info("Executing template_method");
        return null;
    }

    /**
     * Primitive operation 1.
     */
    public String operation1() {
        logger.info("Executing operation1");
        return null;
    }

    /**
     * Primitive operation 2 (hook).
     */
    public String operation2() {
        logger.info("Executing operation2");
        return null;
    }

    /**
     * Primitive operation 3.
     */
    public String operation3() {
        logger.info("Executing operation3");
        return null;
    }

    /**
     * Override operation 2.
     */
    public String operation2() {
        logger.info("Executing operation2");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Template Method");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        str result = algo.template_method();
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
