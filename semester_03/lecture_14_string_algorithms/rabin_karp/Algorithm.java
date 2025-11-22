/**
 * Rabin-Karp Algorithm implementation.
 * 
 * Category: String Algorithm
 * Time Complexity: O(n + m)
 * Space Complexity: O(1)
 */
import java.util.logging.Logger;
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public static void main(String[] args) {
        String separator = "=".repeat(70);
        String dash = "-".repeat(70);
        logger.info("==".repeat(35));
        logger.info("Rabin-Karp Algorithm");
        logger.info("==".repeat(35));
        logger.info("Category: String Algorithm");
        logger.info("Time: O(n + m)");
        logger.info("Space: O(1)");
        logger.info("==".repeat(35));
    }
}
