// package semester_09.lecture_55_advanced_os.exokernel_design;

import java.util.Optional;
import java.util.logging.Logger;

/**
 * Exokernel Design implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    
    public static class Exokernel {
        public Optional<String> allocateResource(String resource, String config) {
            if (resource != null && !resource.isEmpty()) {
                return Optional.of("Resource allocated: " + resource);
            }
            return Optional.empty();
        }
    }
    
    public static void main(String[] args) {
        logger.info("Exokernel Design");
        logger.info("==================================================");
        
        Exokernel algo = new Exokernel();
        Optional<String> result = algo.allocateResource("memory", null);
        if (result.isPresent()) {
            logger.info(result.get());
        }
    }
}