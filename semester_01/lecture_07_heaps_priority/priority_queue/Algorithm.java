package semester_01.lecture_07_heaps_priority.priority_queue;

import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Priority Queue implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Add item with priority.
     */
    public Object push(Object item, Object priority) {
        logger.info("Executing push");
        return null;
    }

    /**
     * Remove and return highest priority item.
     */
    public Object pop() {
        logger.info("Executing pop");
        return null;
    }

    /**
     * Return highest priority item without removing.
     */
    public Object peek() {
        logger.info("Executing peek");
        return null;
    }

    /**
     * Check if queue is empty.
     */
    public boolean is_empty() {
        logger.info("Executing is_empty");
        return false;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Priority Queue");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.push(null, null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
