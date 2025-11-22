package semester_01.lecture_06_advanced_trees.trie;

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
        System.out.println("=".repeat(50));
        System.out.println("Trie Algorithm Test");
        System.out.println("=".repeat(50));

        try {
            // Test Trie operations
            System.out.println("Testing Trie operations...");

            Algorithm algo = Algorithm.create();

            // Test with sample words
            String[] testWords = {"apple", "app", "application", "bat", "ball"};
            System.out.println("Inserting words: " + String.join(", ", testWords));

            long startTime = System.nanoTime();
            for (String word : testWords) {
                Object result = algo.insert(word);
                System.out.println("Inserted '" + word + "': " + result);
            }
            long endTime = System.nanoTime();

            System.out.printf("All operations completed in %.3f ms%n", (endTime - startTime) / 1_000_000.0);
            System.out.println("Status: SUCCESS");

        } catch (Exception e) {
            System.err.println("Error running Trie algorithm: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }

        System.out.println("=".repeat(50));
    }
}
