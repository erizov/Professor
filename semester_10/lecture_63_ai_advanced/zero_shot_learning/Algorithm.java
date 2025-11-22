// package semester_10.lecture_63_ai_advanced.zero_shot_learning;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

/**
 * Zero-Shot Learning implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());
    
    public static Object train(List<String> seenClasses, String descriptions, String[] testClasses) {
        List<Object> result = new ArrayList<>();
        result.add("seen_classes");
        result.add(seenClasses);
        result.add("descriptions");
        result.add(descriptions);
        result.add("test_classes");
        result.add(java.util.Arrays.asList(testClasses));
        return result;
    }
    
    public static void main(String[] args) {
        logger.info("Zero-Shot Learning");
        logger.info("==================================================");
        
        List<String> seenClasses = new ArrayList<>();
        seenClasses.add("cat");
        seenClasses.add("dog");
        
        String[] testClasses = {"bird", "fish"};
        Object result = train(seenClasses, "animal descriptions", testClasses);
        logger.info("Training result: " + result);
    }
}