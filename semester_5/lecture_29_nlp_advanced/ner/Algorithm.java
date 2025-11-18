import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;

/**
 * Ner implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Extract named entities.
     */
    public List<Object> extract_entities(String text) {
        logger.info("Executing extract_entities");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    /**
     * Tag text with entities.
     */
    public List<Object> tag(String text) {
        logger.info("Executing tag");
        Map<String, Object> result = new HashMap<>();
        return result;
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Ner");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        List<Object> result = algo.extract_entities("");
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
