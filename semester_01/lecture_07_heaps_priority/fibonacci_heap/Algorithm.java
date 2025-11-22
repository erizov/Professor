// package semester_01.lecture_07_heaps_priority.fibonacci_heap;

import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Fibonacci Heap implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Insert key into heap.
     */
    public Object insert(Object key) {
        logger.info("Executing insert");
        return null;
    }

    /**
     * Extract minimum key.
     */
    public int extract_min() {
        logger.info("Executing extract_min");
        return -1;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Fibonacci Heap");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.insert(null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
