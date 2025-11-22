// package semester_16.lecture_117_ml_ops_advanced.a_b_testing_ml;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** A B Testing Ml implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Add result for model A.
     */
    public Object add_result_a(Object metric) {
        logger.info("Executing add_result_a");
        return null;
    }

    /**
     * Add result for model B.
     */
    public Object add_result_b(Object metric) {
        logger.info("Executing add_result_b");
        return null;
    }

    /**
     * Calculate statistical significance.
     */
    public int statistical_significance() {
        logger.info("Executing statistical_significance");
        return -1;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("A B Testing Ml");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.add_result_a(null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
