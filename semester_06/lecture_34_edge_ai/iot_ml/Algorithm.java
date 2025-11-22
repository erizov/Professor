// package semester_06.lecture_34_edge_ai.iot_ml;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Iot Ml implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Register IoT device.
     */
    public Object register_device(String device_id, String device_type) {
        logger.info("Executing register_device");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Stream data from device.
     */
    public Object stream_data(String device_id, Object data) {
        logger.info("Executing stream_data");
        return null;
    }

    /**
     * Deploy ML model to device.
     */
    public boolean deploy_model(String device_id, Object model) {
        logger.info("Executing deploy_model");
        return false;
    }

    /**
     * Run prediction on device.
     */
    public int predict(String device_id) {
        logger.info("Executing predict");
        return -1;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Iot Ml");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.register_device("", "");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
