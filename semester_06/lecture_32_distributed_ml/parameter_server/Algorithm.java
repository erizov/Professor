package semester_06.lecture_32_distributed_ml.parameter_server;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Parameter Server implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Initialize parameters.
     */
    public Object initialize_parameters(String param_name, List<Object> shape) {
        logger.info("Executing initialize_parameters");
        return null;
    }

    /**
     * Get parameters.
     */
    public int get_parameters(String param_name) {
        logger.info("Executing get_parameters");
        return -1;
    }

    /**
     * Update parameters with gradients.
     */
    public Object update_parameters(String param_name, List<Object> gradients, Object learning_rate) {
        logger.info("Executing update_parameters");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Parameter Server");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.initialize_parameters("", new ArrayList<>());
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
