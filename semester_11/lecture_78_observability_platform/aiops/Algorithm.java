// package semester_11.lecture_78_observability_platform.aiops;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Aiops implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Collect metric.
     */
    public Object collect_metrics(String metric_name, Object value) {
        logger.info("Executing collect_metrics");
        return null;
    }

    /**
     * Detect anomalies in metric.
     */
    public boolean detect_anomalies(String metric_name, Object threshold) {
        logger.info("Executing detect_anomalies");
        return false;
    }

    /**
     * Predict future metric values.
     */
    public int predict_metric(String metric_name, Object steps) {
        logger.info("Executing predict_metric");
        return -1;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Aiops");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.collect_metrics("", null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
