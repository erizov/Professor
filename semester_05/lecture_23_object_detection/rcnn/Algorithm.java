import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
package semester_05.lecture_23_object_detection.rcnn;
 * Rcnn implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Detect regions.
     */
    public List<Object> detect_regions(List<Object> image) {
        logger.info("Executing detect_regions");
        Map<String, Object> result = new HashMap<>();
        return null; // TODO: Implement RCNN logic
    }

    /**
     * Classify region.
     */
    public int classify_region(Object region) {
        logger.info("Executing classify_region");
        return -1;
    }

    /**
     * Train RCNN.
     */
    public Object train(List<Object> images, List<Object> annotations) {
        logger.info("Executing train");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Rcnn");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        List<Object> result = algo.detect_regions(new ArrayList<>());
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
