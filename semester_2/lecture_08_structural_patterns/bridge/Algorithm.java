import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Bridge implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Concrete implementor A.
     */
    public String operation_impl() {
        logger.info("Executing operation_impl");
        return null;
    }

    /**
     * Concrete implementor B.
     */
    public String operation_impl() {
        logger.info("Executing operation_impl");
        return null;
    }

    /**
     * Abstraction.
     */
    public String operation_impl() {
        logger.info("Executing operation_impl");
        return null;
    }

    /**
     * Refined abstraction.
     */
    public String operation() {
        logger.info("Executing operation");
        String result = "Abstraction(" + self.implementor.operation_impl() + ")";
        return "";
    }

    /**
     * Operation
     */
    public String operation() {
        logger.info("Executing operation");
        String result = "RefinedAbstraction(" + self.implementor.operation_impl() + ")";
        return "";
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Bridge");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        str result = algo.operation_impl();
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
