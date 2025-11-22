// package semester_06.lecture_33_model_optimization.nas;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

/**
 * Neural Architecture Search (NAS) implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    
    public static Object defineSearchSpace(String space, List<Object> layers) {
        List<Object> searchSpace = new ArrayList<>();
        searchSpace.add(space);
        searchSpace.addAll(layers);
        return searchSpace;
    }
    
    public static void main(String[] args) {
        logger.info("Neural Architecture Search");
        logger.info("==================================================");
        
        List<Object> layers = new ArrayList<>();
        layers.add("conv");
        layers.add("pool");
        layers.add("fc");
        
        Object space = defineSearchSpace("resnet", layers);
        logger.info("Search space: " + space);
    }
}