import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Naive Bayes implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Naive Bayes");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        System.out.println("=".repeat(70));
    }
}
