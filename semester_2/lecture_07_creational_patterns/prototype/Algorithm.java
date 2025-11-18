import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Prototype implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Clone prototype.
     */
    public Object clone() {
        logger.info("Executing clone");
        return null;
    }

    /**
     *   Str  
     */
    public String __str__() {
        logger.info("Executing __str__");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Prototype");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.clone();
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
