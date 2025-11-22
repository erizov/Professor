package semester_01.lecture_07_heaps_priority.binary_heap;

import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Binary Heap implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Get parent index.
     */
    public int parent(Object i) {
        logger.info("Executing parent");
        return -1;
    }

    /**
     * Get left child index.
     */
    public int left_child(Object i) {
        logger.info("Executing left_child");
        return -1;
    }

    /**
     * Get right child index.
     */
    public int right_child(Object i) {
        logger.info("Executing right_child");
        return -1;
    }

    /**
     * Insert value into heap.
     */
    public Object insert(Object val) {
        logger.info("Executing insert");
        return null;
    }

    /**
     * Extract minimum value.
     */
    public int extract_min() {
        logger.info("Executing extract_min");
        return -1;
    }

    /**
     * Maintain heap property upward.
     */
    public Object _heapify_up(Object i) {
        logger.info("Executing _heapify_up");
        return null;
    }

    /**
     * Maintain heap property downward.
     */
    public Object _heapify_down(Object i) {
        logger.info("Executing _heapify_down");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Binary Heap");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo.parent(null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
