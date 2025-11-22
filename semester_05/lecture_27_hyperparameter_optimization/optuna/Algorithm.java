package semester_05.lecture_27_hyperparameter_optimization.optuna;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Optuna implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Suggest float parameter.
     */
    public int suggest_float(String name, Object low, Object high) {
        logger.info("Executing suggest_float");
        return -1;
    }

    /**
     * Suggest int parameter.
     */
    public int suggest_int(String name, Object low, Object high) {
        logger.info("Executing suggest_int");
        return -1;
    }

    /**
     * Suggest categorical parameter.
     */
    public Object suggest_categorical(String name, List<Object> choices) {
        logger.info("Executing suggest_categorical");
        return null;
    }

    /**
     * Optimize hyperparameters.
     */
    public Map<String, Object> optimize(Object objective, Object n_trials) {
        logger.info("Executing optimize");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Optuna");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        int result = algo.suggest_float("", null, null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
