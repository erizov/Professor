package semester_02.lecture_12_concurrency_patterns.producer_consumer;
import java.util.*;
import java.util.logging.Logger;
import java.util.logging.Level;


/*** Producer Consumer implementation.
 */
public class Algorithm {
    private static final Logger logger = Logger.getLogger(Algorithm.class.getName());

    public Algorithm() {
        // Initialize
    }

    /**
     * Produce item.
     */
    public Object produce(Object item) {
        logger.info("Executing produce");
        String result = "Produced: " + item + "";
        return "";
    }

    /**
     * Consume item.
     */
    public Object consume() {
        logger.info("Executing consume");
        String result = "Consumed: item";
        return "";
    }

    public static Algorithm create() {
        return new Algorithm();
    }

    public static void main(String[] args) {
        System.out.println("=".repeat(70));
        System.out.println("Producer Consumer");
        System.out.println("=".repeat(70));
        
        Algorithm algo = Algorithm.create();
        Object result = algo.produce(null);
        System.out.println("Result: " + result);
        System.out.println("=".repeat(70));
    }
}
