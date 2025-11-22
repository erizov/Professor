package semester_09.lecture_55_advanced_os.exokernel_design;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Exokernel Design implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Allocate resource.
     */
    public String allocate_resource(String resource_type, Object amount) {
        logger.info("Executing allocate_resource");
        String result = "RES-" + len(self.resources) + "";
        return "";
    }

    /**
     * Register library.
     */
    public Object register_library(String lib_name, Object resource_handler) {
        logger.info("Executing register_library");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        logger.info("=".repeat(70));
        logger.info("Exokernel Design");
        logger.info("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Optional[str] result = algo.allocate_resource("", null);
        logger.info("Result: " + result);
        logger.info("=".repeat(70));
    }
}
