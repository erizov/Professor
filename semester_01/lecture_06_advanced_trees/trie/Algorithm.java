import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Trie implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Insert word into trie.
     */
    public Object insert(String word) {
        logger.info("Executing insert");
        return null;
    }

    /**
     * Search for word in trie.
     */
    public boolean search(String word) {
        logger.info("Executing search");
        return false;
    }

    /**
     * Check if any word starts with prefix.
     */
    public boolean starts_with(String prefix) {
        logger.info("Executing starts_with");
        return false;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Trie");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.insert("");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
