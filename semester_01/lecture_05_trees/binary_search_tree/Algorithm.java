import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Binary Search Tree implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Insert value into BST.
     */
    public Object insert(Object val) {
        logger.info("Executing insert");
        return null;
    }

    /**
     *  Insert
     */
    public Object _insert(Object root, Object val) {
        logger.info("Executing _insert");
        return null;
    }

    /**
     * Search for value in BST.
     */
    public boolean search(Object val) {
        logger.info("Executing search");
        return false;
    }

    /**
     *  Search
     */
    public boolean _search(Object root, Object val) {
        logger.info("Executing _search");
        return false;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Binary Search Tree");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.insert(null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
