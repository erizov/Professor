package semester_10.lecture_63_ai_advanced.zero_shot_learning;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Zero Shot Learning implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Train on seen classes.
     */
    public Object train(List<String> seen_classes, String descriptions, String str]) {
        logger.info("Executing train");
        return null;
    }

    /**
     * Predict unseen class.
     */
    public String predict(List<Object> input_data, List<String> unseen_classes) {
        logger.info("Executing predict");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("Zero Shot Learning");
        logger.info("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.train(new ArrayList<>(), "", "");
        logger.info("Result: " + result);
        logger.info("=".repeat(70));
    }
}
