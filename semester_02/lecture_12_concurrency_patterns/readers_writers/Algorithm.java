// package semester_02.lecture_12_concurrency_patterns.readers_writers;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Readers Writers implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Read data.
     */
    public int read() {
        logger.info("Executing read");
        return -1;
    }

    /**
     * Write data.
     */
    public Object write(Object value) {
        logger.info("Executing write");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Readers Writers");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo.read();
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
