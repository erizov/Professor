package semester_06.lecture_34_edge_ai.tflite;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Tflite implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Convert model to TFLite.
     */
    public Map<String, Object> convert_model(String model_id, Object model) {
        logger.info("Executing convert_model");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Quantize model.
     */
    public Map<String, Object> quantize(String model_id) {
        logger.info("Executing quantize");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Run inference.
     */
    public int inference(String model_id, List<Object> input_data) {
        logger.info("Executing inference");
        return -1;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Tflite");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.convert_model("", null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
