import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Sha256 implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Hash data.
     */
    public String hash(String data) {
        logger.info("Executing hash");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Sha256");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        String result = algo.hash("");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
