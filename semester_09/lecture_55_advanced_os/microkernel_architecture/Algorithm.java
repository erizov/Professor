package semester_09.lecture_55_advanced_os.microkernel_architecture;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Microkernel Architecture implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Register kernel service.
     */
    public Object register_kernel_service(String service_name, Object service) {
        logger.info("Executing register_kernel_service");
        return null;
    }

    /**
     * Register user service.
     */
    public Object register_user_service(String service_name, Object service) {
        logger.info("Executing register_user_service");
        return null;
    }

    /**
     * Call service.
     */
    public Object call_service(String service_name, Object *args, Object **kwargs) {
        logger.info("Executing call_service");
        return null;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("Microkernel Architecture");
        logger.info("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.register_kernel_service("", null);
        logger.info("Result: " + result);
        logger.info("=".repeat(70));
    }
}
