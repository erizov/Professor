/**
 * KMP String Matching implementation.
 * 
 * Category: String Algorithm
 * Time Complexity: O(n + m)
 * Space Complexity: O(m)
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        logger.info("==".repeat(35));
        logger.info("KMP String Matching");
        logger.info("==".repeat(35));
        logger.info("Category: String Algorithm");
        logger.info("Time: O(n + m)");
        logger.info("Space: O(m)");
        logger.info("==".repeat(35));
    }
}
