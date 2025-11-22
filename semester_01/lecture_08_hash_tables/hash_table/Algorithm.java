// package semester_01.lecture_08_hash_tables.hash_table;

import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Hash Table implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Hash function.
     */
    public int _hash(Object key) {
        logger.info("Executing _hash");
        return key != null ? key.hashCode() : 0;
    }

    /**
     * Insert key-value pair.
     */
    public Object insert(Object key, Object value) {
        logger.info("Executing insert");
        return null;
    }

    /**
     * Get value by key.
     */
    public Object get(Object key) {
        logger.info("Executing get");
        return null;
    }

    /**
     * Delete key-value pair.
     */
    public boolean delete(Object key) {
        logger.info("Executing delete");
        return false;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Hash Table");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo._hash(null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
